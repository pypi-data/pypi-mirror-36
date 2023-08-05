import logging

import aiosasl
import sys
import asyncio
from hashlib import md5
from threading import Thread, Event

import aioxmpp
import aioxmpp.ibr as ibr
from aioxmpp.dispatcher import SimpleMessageDispatcher

from spade.message import Message
from spade.presence import PresenceManager
from spade.trace import TraceStore
from spade.web import WebApp

logger = logging.getLogger('spade.Agent')


class AuthenticationFailure(Exception):
    pass


class Agent(object):
    def __init__(self, jid, password, verify_security=False, loop=None):
        """
        Creates an agent
        :param jid: The identifier of the agent in the form username@server
        :type jid: str
        :param password: The password to connect to the server
        :type password: str
        :param verify_security: Wether to verify or not the SSL certificates
        :type verify_security: bool
        :param loop: the event loop if it was already created (optional)
        :type loop: an asyncio event loop
        """
        self.jid = aioxmpp.JID.fromstr(jid)
        self.password = password
        self.verify_security = verify_security

        self.behaviours = []
        self._values = {}

        self.traces = TraceStore(size=1000)

        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.new_event_loop()
        self.aiothread = AioThread(self, self.loop)
        self._alive = Event()

        # obtain an instance of the service
        self.message_dispatcher = self.client.summon(SimpleMessageDispatcher)

        # Presence service
        self.presence = PresenceManager(self)

        # Web service
        self.web = WebApp(agent=self)

    def start(self, auto_register=True):
        """
        Starts the agent. This fires some actions:
            - if auto_register: register the agent in the server
            - runs the event loop
            - connects the agent to the server
            - runs the registered behaviours
        :param auto_register: register the agent in the server
        :type auto_register: bool
        """
        if auto_register:
            self.register()

        self.aiothread.connect()
        self.aiothread.start()
        self._alive.set()
        self.aiothread.event.wait()

        # register a message callback here
        self.message_dispatcher.register_callback(
            aioxmpp.MessageType.CHAT,
            None,
            self._message_received,
        )

        self.setup()

    def register(self):  # pragma: no cover
        """
        Register the agent in the XMPP server.
        """
        metadata = aioxmpp.make_security_layer(None, no_verify=not self.verify_security)
        _, stream, features = self.loop.run_until_complete(aioxmpp.node.connect_xmlstream(self.jid, metadata))
        query = ibr.Query(self.jid.localpart, self.password)
        self.loop.run_until_complete(ibr.register(stream, query))

    def setup(self):
        """
        setup agent before startup.
        this method may be overloaded.
        """
        pass

    @property
    def name(self):
        return self.jid.localpart

    @property
    def client(self):
        return self.aiothread.client

    @property
    def stream(self):
        return self.aiothread.stream

    @property
    def avatar(self):
        """
        Generates a unique avatar for the agent based on its JID.
        Uses Gravatar service with MonsterID option.
        :return: the url of the agent's avatar
        :rtype: :class:`str`
        """
        return self.build_avatar_url(self.jid.bare())

    @staticmethod
    def build_avatar_url(jid):
        """
        Static method to build a gravatar url with the agent's JID
        :param jid: an XMPP identifier
        :type jid: aioxmpp.JID
        :return: an URL for the gravatar
        :rtype: str
        """
        digest = md5(str(jid).encode("utf-8")).hexdigest()
        return "http://www.gravatar.com/avatar/{md5}?d=monsterid".format(md5=digest)

    def submit(self, coro):
        """
        runs a coroutine in the event loop of the agent.
        this call is not blocking.
        :param coro: the coroutine to be run
        :type coro: coroutine
        """
        return asyncio.run_coroutine_threadsafe(coro, loop=self.loop)

    def add_behaviour(self, behaviour, template=None):
        """
        Adds and starts a behaviour to the agent.
        If template is not None it is used to match
        new messages and deliver them to the behaviour.
        :param behaviour: the behaviour to be started
        :type behaviour: :class:`spade.behaviour.CyclicBehaviour`
        :param template: the template to match messages with
        :type template: :class:`spade.template.Template`
        """
        behaviour.set_agent(self)
        behaviour.set_template(template)
        self.behaviours.append(behaviour)
        behaviour.start()

    def remove_behaviour(self, behaviour):
        """
        Removes a behaviour from the agent.
        The behaviour is first killed.
        :param behaviour: the behaviour instance to be removed
        :type behaviour: :class:`spade.behaviour.CyclicBehaviour`
        """
        if not self.has_behaviour(behaviour):
            raise ValueError("This behaviour is not registered")
        index = self.behaviours.index(behaviour)
        self.behaviours[index].kill()
        self.behaviours.pop(index)

    def has_behaviour(self, behaviour):
        """
        Checks if a behaviour is added to an agent.
        :param behaviour: the behaviour instance to check
        :type behaviour: :class:`spade.behaviour.CyclicBehaviour`
        :return: a boolean that indicates wether the behaviour is inside the agent.
        :rtype: bool
        """
        return behaviour in self.behaviours

    def stop(self):
        """
        Stops an agent and kills all its behaviours.
        """
        self.presence.set_unavailable()
        for behav in self.behaviours:
            behav.kill()
        if self.web.server:
            self.web.server.close()
            self.submit(self.web.app.shutdown())
            self.submit(self.web.handler.shutdown(60.0))
            self.submit(self.web.app.cleanup())
        self.aiothread.finalize()
        self._alive.clear()

    def is_alive(self):
        """
        checks if the agent is alive
        :return: wheter the agent is alive or not
        :rtype: :class:`bool`
        """
        return self._alive.is_set()

    def set(self, name, value):
        """
        Stores a knowledge item in the agent knowledge base.
        :param name: name of the item
        :type name: :class:`str`
        :param value: value of the item
        :type value: :class:`object`
        """
        self._values[name] = value

    def get(self, name):
        """
        Recovers a knowledge item from the agent's knowledge base.
        :param name: name of the item
        :type name: :class:`str`
        :return: the object retrieved or None
        :rtype: :class:`object`
        """
        if name in self._values:
            return self._values[name]
        else:
            return None

    def _message_received(self, msg):
        """
        Callback run when an XMPP Message is reveived.
        This callback delivers the message to every behaviour
        that is waiting for it using their templates match.
        the aioxmpp.Message is converted to spade.message.Message
        :param msg: the message just received.
        :type msg: aioxmpp.Messagge
        """
        logger.debug(f"Got message: {msg}")

        msg = Message.from_node(msg)
        futures = []
        matched = False
        for behaviour in (x for x in self.behaviours if x.match(msg)):
            futures.append(self.submit(behaviour.enqueue(msg)))
            logger.debug(f"Message enqueued to behaviour: {behaviour}")
            self.traces.append(msg, category=str(behaviour))
            matched = True
        if not matched:
            logger.warning(f"No behaviour matched for message: {msg}")
            self.traces.append(msg)
        return futures


class AioThread(Thread):
    def __init__(self, agent, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = agent
        self.jid = agent.jid
        self.event = Event()
        self.conn_coro = None
        self.stream = None
        self.loop = loop

        asyncio.set_event_loop(self.loop)

        self.client = aioxmpp.PresenceManagedClient(agent.jid,
                                                    aioxmpp.make_security_layer(agent.password,
                                                                                no_verify=not agent.verify_security),
                                                    loop=self.loop,
                                                    logger=logging.getLogger(agent.jid.localpart))

    def connect(self):  # pragma: no cover
        try:
            self.conn_coro = self.client.connected()
            aenter = type(self.conn_coro).__aenter__(self.conn_coro)
            self.stream = self.loop.run_until_complete(aenter)
            logger.info(f"Agent {str(self.jid)} connected and authenticated.")
        except aiosasl.AuthenticationFailure:
            raise AuthenticationFailure(
                "Could not authenticate the agent. Check user and password or use auto_register=True")

    def run(self):
        self.loop.call_soon(self.event.set)
        self.loop.run_forever()

    def finalize(self):
        if self.agent.is_alive():
            self.client.stop()
            aexit = self.conn_coro.__aexit__(*sys.exc_info())
            future = asyncio.run_coroutine_threadsafe(aexit, loop=self.loop)
            try:
                asyncio.wait_for(future, timeout=5)
            except asyncio.TimeoutError:  # pragma: no cover
                print('The client took too long to disconnect, cancelling the task...')
                future.cancel()
            except Exception as e:  # pragma: no cover
                logger.error("Could not disconnect from server: {!r}.".format(e))
            else:
                logger.info("Client disconnected.")
        self.loop.call_soon_threadsafe(self.loop.stop)
