"""
@ Author      : Troy Kelly
@ Date        : 23 Sept 2018
@ Description : Philips Dynalite Library - Unofficial interface for Philips Dynalite over RS485

@ Notes:        Requires a RS485 to IP gateway (Do not use the Dynalite one - use something cheaper)
"""

import asyncio
import logging
import json

LOG = logging.getLogger(__name__)


class DynetError(Exception):
    def __init__(self, message):
        self.message = message


class PacketError(Exception):
    def __init__(self, message):
        self.message = message


class DynetPacket(object):

    def __init__(self, msg=None):
        self.sync = None
        self.area = None
        self.data = []
        self.command = None
        self.join = None
        self.chk = None
        if msg is not None:
            self.fromMsg(msg)

    def toMsg(self, sync=28, area=0, command=0, data=[0, 0, 0], join=255):
        bytes = []
        bytes.append(sync)
        bytes.append(area)
        bytes.append(data[0])
        bytes.append(command)
        bytes.append(data[1])
        bytes.append(data[2])
        bytes.append(join)
        bytes.append(self.calcsum(bytes))
        self.fromMsg(bytes)

    def fromMsg(self, msg):
        bytes = []
        for byte in msg:
            bytes.append(int(byte))
        self._msg = bytes
        if(len(self._msg) > 8):
            self.excess = self._msg[7:]
            self._msg = self._msg[:7]
        if self.calcsum(self._msg) != self._msg[7]:
            raise PacketError("Failed checksum %s" % self._msg)
        self.sync = self._msg[0]
        self.area = self._msg[1]
        self.data = [self._msg[2], self._msg[4], self._msg[5]]
        self.command = self._msg[3]
        self.join = self._msg[6]
        self.chk = self._msg[7]
        if self.sync == 28:
            if self.command < 4 or (self.command > 9 and self.command < 14):
                if self.command > 3:
                    self.preset = self.command - 6
                else:
                    self.preset = self.command
                self.preset = (self.preset + (self.data[2] * 8)) + 1
                self.fade = (self.data[0] + (self.data[1] * 256)) * 0.02
            if self.command == 101:
                self.preset = self.data[0] + 1
                self.fade = (self.data[1] + (self.data[2] * 256)) * 0.02

    def toJson(self):
        return json.dumps(self.__dict__)

    def calcsum(self, msg):
        msg = msg[:7]
        return (-(sum(ord(c) for c in "".join(map(chr, msg))) % 256) & 0xFF)


class DynetEvent(object):

    def __init__(self, eventType=None, message=None, data={}, direction=None):
        self.eventType = eventType.upper() if eventType else None
        self.msg = message
        self.data = data
        self.direction = direction

    def toJson(self):
        return json.dumps(self.__dict__)


class DynetConnection(asyncio.Protocol):

    def __init__(self, connectionMade=None, connectionLost=None, receiveHandler=None, connectionPause=None, connectionResume=None, loop=None):
        self._transport = None
        self._paused = False
        self._loop = loop
        self.connectionMade = connectionMade
        self.connectionLost = connectionLost
        self.receiveHandler = receiveHandler
        self.connectionPause = connectionPause
        self.connectionResume = connectionResume

    def connection_made(self, transport):
        self._transport = transport
        self._paused = False
        if self.connectionMade is not None:
            if self._loop is None:
                self.connectionMade(transport)
            else:
                self._loop.create_task(self.connectionMade(transport))

    def connection_lost(self, exc=None):
        self._transport = None
        if self.connectionLost is not None:
            if self._loop is None:
                self.connectionLost(exc)
            else:
                self._loop.create_task(self.connectionLost(exc))

    def pause_writing(self):
        self._paused = True
        if self.connectionPause is not None:
            if self._loop is None:
                self.connectionPause()
            else:
                self._loop.create_task(self.connectionPause())

    def resume_writing(self):
        self._paused = False
        if self.connectionResume is not None:
            if self._loop is None:
                self.connectionResume()
            else:
                self._loop.create_task(self.connectionResume())

    def data_received(self, data):
        LOG.debug("Data Received: %s" % data)
        if self.receiveHandler is not None:
            if self._loop is None:
                self.receiveHandler(data)
            else:
                self._loop.create_task(self.receiveHandler(data))

    def eof_received(self):
        LOG.debug("EOF Received")


class DynetControl(object):

    def __init__(self, dynet, loop, areaDefinition=None):
        self._dynet = dynet
        self._loop = loop
        self._area = areaDefinition

    def areaPreset(self, area, preset, fade=2):
        self._loop.create_task(self._areaPreset(area=area,preset=preset,fade=fade))

    @asyncio.coroutine
    def _areaPreset(self, area, preset, fade):
        packet = DynetPacket()
        preset = preset - 1
        bank = int((preset)/8)
        opcode = preset-(bank*8)
        if opcode > 3:
            opcode = opcode + 6
        fadeLow = int(fade / 0.02) - (int((fade / 0.02) / 256) * 256)
        fadeHigh = int((fade / 0.02) / 256)
        packet.toMsg(sync=28, area=area, command=opcode, data=[fadeLow, fadeHigh, bank], join=255)
        self._dynet.write(packet)

    def areaOff(self, area, fade=2):
        self._loop.create_task(self._areaOff(area=area,fade=fade))

    @asyncio.coroutine
    def _areaOff(self, area, fade):
        packet = DynetPacket()
        if fade > 25.5:
            fade = 25.5
        if fade < 0:
            fade = 0
        packet.toMsg(sync=28, area=area, command=104, data=[255, 0, int(fade*10)], join=255)
        self._dynet.write(packet)



class Dynet(object):

    def __init__(self, host=None, port=None, broadcaster=None, onConnect=None, onDisconnect=None, loop=None):
        if host is None or port is None or loop is None:
            raise DynetError(
                'Must supply a host, port and loop for Dynet connection')
        self._host = host
        self._port = port
        self._loop = loop
        self.broadcast = broadcaster
        self._onConnect = onConnect
        self._onDisconnect = onDisconnect
        self._conn = lambda: DynetConnection(connectionMade=self._connection, connectionLost=self._disconnection,
                                             receiveHandler=self._receive, connectionPause=self._pause, connectionResume=self._resume, loop=self._loop)
        self._transport = None
        self._handlers = {}
        self._connection_retry_timer = 1
        self._paused = False
        self._inBuffer = []
        self._outBuffer = []
        self._timeout = 30

    def cleanup(self):
        self._connection_retry_timer = 1
        self._inBuffer = []
        self._outBuffer = []
        self._transport = None

    def connect(self, onConnect=None):
        asyncio.ensure_future(self._connect())

    async def _connect(self):
        LOG.debug("Connecting to Dynet on %s:%d" % (self._host, self._port))
        try:
            await asyncio.wait_for(self._loop.create_connection(self._conn, host=self._host, port=self._port), timeout=self._timeout)
        except (ValueError, OSError, asyncio.TimeoutError) as err:
            LOG.warning("Could not connect to Dynet (%s). Retrying in %d seconds",
                        err, self._connection_retry_timer)
            self._loop.call_later(self._connection_retry_timer, self.connect)
            self._connection_retry_timer = 2 * \
                self._connection_retry_timer if self._connection_retry_timer < 32 else 60

    @asyncio.coroutine
    def _receive(self, data):
        packet = DynetPacket(data)
        if hasattr(packet, 'preset'):
            event = DynetEvent(eventType='AREAPRESET', message=("Area %d Preset %d Fade %d seconds." % (packet.area, packet.preset, packet.fade)), data={'area':packet.area,'preset':packet.preset,'fade':packet.fade,'join':packet.join}, direction="IN")
            self.broadcast(event)
        else:
            LOG.debug("Dynet Inbound: %s" % packet.toJson())

    @asyncio.coroutine
    def _pause(self):
        LOG.debug("Pausing Dynet on %s:%d" % (self._host, self._port))
        # Need to schedule a resend here
        self._paused = True

    @asyncio.coroutine
    def _resume(self):
        LOG.debug("Resuming Dynet on %s:%d" % (self._host, self._port))
        # Need to schedule a resend here
        self._paused = False

    @asyncio.coroutine
    def _connection(self, transport=None):
        LOG.debug("Connected to Dynet on %s:%d" % (self._host, self._port))
        self.cleanup()
        if not transport is None:
            self._transport = transport
            if self._onConnect is not None:
                self._loop.create_task(self._onConnect(dynet=self,transport=transport))
        else:
            raise DynetError("Connected but not transport channel provided")

    @asyncio.coroutine
    def _disconnection(self, exc=None):
        LOG.debug("Disconnected from Dynet on %s:%d" %
                  (self._host, self._port))
        self.cleanup()
        if self._onDisconnect is not None:
            self._loop.create_task(self._onDisconnect(dynet=self))

        if exc is not None:
            LOG.error(exc)

    def write(self, packet=None):
        self._loop.create_task(self._write(packet))

    @asyncio.coroutine
    def _write(self, newPacket=None):
        if self._transport is None:
            raise DynetError("Must be connected to write/send messages")

        if newPacket is not None:
            self._outBuffer.append(newPacket)

        if self._paused:
            LOG.info("Connection paused - queuing packet")
            self._loop.call_later(1, self.updateLocations)

        for idx, packet in enumerate(self._outBuffer):
            msg = bytearray()
            msg.append(packet.sync)
            msg.append(packet.area)
            msg.append(packet.data[0])
            msg.append(packet.command)
            msg.append(packet.data[1])
            msg.append(packet.data[2])
            msg.append(packet.join)
            msg.append(packet.chk)
            try:
                self._transport.write(msg)
                LOG.debug("Dynet Sent: %s" % msg)
            except:
                self._logger.error("Unable to write data: %s" % msg)
            del self._outBuffer[idx]
            #self._loop.create_task(self._receive(msg))
