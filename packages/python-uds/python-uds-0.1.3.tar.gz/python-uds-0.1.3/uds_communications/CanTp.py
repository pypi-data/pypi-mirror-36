#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import can
from can.interfaces import pcan, vector

from uds_communications.iTp import iTp
from uds_communications.Utilities.ResettableTimer import ResettableTimer
from uds_communications.CanTpTypes import CanTpAddressingTypes, CanTpState, CanTpMessageType, CanTpFsTypes
from uds_communications.CanTpTypes import CANTP_MAX_PAYLOAD_LENGTH, SINGLE_FRAME_DL_INDEX, FIRST_FRAME_DL_INDEX_HIGH, \
    FIRST_FRAME_DL_INDEX_LOW, FC_BS_INDEX, FC_STMIN_INDEX, N_PCI_INDEX, FIRST_FRAME_DATA_START_INDEX, \
    SINGLE_FRAME_DATA_START_INDEX, CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX, \
    CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX, FLOW_CONTROL_BS_INDEX, FLOW_CONTROL_STMIN_INDEX
from uds_configuration.ConfigSingleton import get_config


def fillArray(data, length, fillValue=0):
    output = []
    for i in range(0, length):
        output.append(fillValue)
    for i in range(0, len(data)):
        output[i] = data[i]
    return output


##
# @class CanTp
# @brief This is the main class to support CAN transport protocol
#
# Will spawn a CanTpListener class for incoming messages
# depends on a bus object for communication on CAN
class CanTp(iTp):

    ##
    # @brief constructor for the CanTp object
    def __init__(self, reqId=None, resId=None):

        self.__config = get_config()

        self.__bus = self.createBusConnection()

        # there probably needs to be an adapter to deal with these parts as they couple to python-can heavily
        self.__listener = can.Listener()
        self.__listener.on_message_received = self.callback_onReceive
        self.__notifier = can.Notifier(self.__bus, [self.__listener], 0)

        self.__reqId = reqId
        self.__resId = resId

        self.__recvBuffer = []

        # this should probably be in the config file as well
        # this needs expanding to support the other addressing types
        self.__addressingType = CanTpAddressingTypes.NORMAL_FIXED

        if(self.__addressingType == CanTpAddressingTypes.NORMAL_FIXED):
            self.__maxPduLength = 7
            self.__pduStartIndex = 0
        else:
            self.__maxPduLength = 6
            self.__pduStartIndex = 1

        self.__N_AE = 0xFF
        self.__N_TA = 0xFF
        self.__N_SA = 0xFF


    ##
    # @brief connection method
    def createBusConnection(self):
        # check config file and load
        connectionType = self.__config['DEFAULT']['interface']

        if connectionType == 'virtual':
            connectionName = self.__config['virtual']['interfaceName']
            bus = can.interface.Bus(connectionName,
                                    bustype='virtual')
        elif connectionType == 'peak':
            channel = self.__config['peak']['device']
            baudrate = self.__config['connection']['baudrate']
            bus = pcan.PcanBus(channel,
                               bitrate=baudrate)
        elif connectionType == 'vector':
            channel = self.__config['vector']['channel']
            app_name = self.__config['vector']['app_name']
            baudrate = int(self.__config['connection']['baudrate']) * 1000
            bus = vector.VectorBus(channel,
                                   app_name=app_name,
                                   data_bitrate=baudrate)

        return bus

    ##
    # @brief send method
    # @param [in] payload the payload to be sent
    def send(self, payload, functionalReq=False):

        payloadLength = len(payload)
        payloadPtr = 0

        state = CanTpState.IDLE

        if payloadLength > CANTP_MAX_PAYLOAD_LENGTH:
            raise Exception("Payload too large for CAN Transport Protocol")

        if payloadLength < self.__maxPduLength:
            state = CanTpState.SEND_SINGLE_FRAME
        else:
            # we might need a check for functional request as we may not be able to service functional requests for
            # multi frame requests
            state = CanTpState.SEND_FIRST_FRAME

        txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        sequenceNumber = 1
        endOfMessage_flag = False

        blockList = []
        currBlock = []

        timeoutTimer = ResettableTimer(100)
        stMinTimer = ResettableTimer()

        self.clearBufferedMessages()

        while endOfMessage_flag is False:

            rxPdu = self.getNextBufferedMessage()

            if rxPdu is not None:
                N_PCI = (rxPdu[0] & 0xF0) >> 4
                if N_PCI == CanTpMessageType.FLOW_CONTROL:
                    fs = rxPdu[0] & 0x0F
                    if fs == CanTpFsTypes.WAIT:
                        raise Exception("Wait not currently supported")
                    elif fs == CanTpFsTypes.OVERFLOW:
                        raise Exception("Overflow received from ECU")
                    elif fs == CanTpFsTypes.CONTINUE_TO_SEND:
                        if state == CanTpState.WAIT_FLOW_CONTROL:
                            if fs == CanTpFsTypes.CONTINUE_TO_SEND:
                                bs = rxPdu[FC_BS_INDEX]
                                if(bs == 0):
                                    bs = 585
                                blockList = self.create_blockList(payload[payloadPtr:],
                                                                  bs)
                                stMin = self.decode_stMin(rxPdu[FC_STMIN_INDEX])
                                currBlock = blockList.pop(0)
                                state = CanTpState.SEND_CONSECUTIVE_FRAME
                                stMinTimer.timeoutTime = stMin
                                stMinTimer.start()
                                timeoutTimer.stop()
                        else:
                            raise Exception("Unexpected Flow Control Continue to Send request")
                    else:
                        raise Exception("Unexpected fs response from ECU")
                else:
                    raise Exception("Unexpected response from device")

            if state == CanTpState.SEND_SINGLE_FRAME:
                txPdu[N_PCI_INDEX] += (CanTpMessageType.SINGLE_FRAME << 4)
                txPdu[SINGLE_FRAME_DL_INDEX] += payloadLength
                txPdu[SINGLE_FRAME_DATA_START_INDEX:] = fillArray(payload, self.__maxPduLength)
                self.transmit(txPdu, functionalReq)
                endOfMessage_flag = True
            elif state == CanTpState.SEND_FIRST_FRAME:
                payloadLength_highNibble = (payloadLength & 0xF00) >> 8
                payloadLength_lowNibble  = (payloadLength & 0x0FF)
                txPdu[N_PCI_INDEX] += (CanTpMessageType.FIRST_FRAME << 4)
                txPdu[FIRST_FRAME_DL_INDEX_HIGH] += payloadLength_highNibble
                txPdu[FIRST_FRAME_DL_INDEX_LOW] += payloadLength_lowNibble
                txPdu[FIRST_FRAME_DATA_START_INDEX:] = payload[0:self.__maxPduLength-1]
                payloadPtr += self.__maxPduLength-1
                self.transmit(txPdu, functionalReq)
                timeoutTimer.start()
                state = CanTpState.WAIT_FLOW_CONTROL
            elif state == CanTpState.SEND_CONSECUTIVE_FRAME:
                if(stMinTimer.isExpired()):
                    txPdu[N_PCI_INDEX] += (CanTpMessageType.CONSECUTIVE_FRAME << 4)
                    txPdu[CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX] += sequenceNumber
                    txPdu[CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX:] = currBlock.pop(0)
                    payloadPtr += self.__maxPduLength
                    self.transmit(txPdu, functionalReq)
                    sequenceNumber = (sequenceNumber + 1) % 16
                    stMinTimer.restart()
                    if(len(currBlock) == 0):
                        if(len(blockList) == 0):
                            endOfMessage_flag = True
                        else:
                            timeoutTimer.start()
                            state = CanTpState.WAIT_FLOW_CONTROL

            txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            # timer / exit condition checks
            if(timeoutTimer.isExpired()):
                raise Exception("Timeout waiting for message")

    ##
    # @brief recv method
    # @param [in] timeout_ms The timeout to wait before exiting
    # @return a list
    def recv(self, timeout_s):

        timeoutTimer = ResettableTimer(timeout_s)

        payload = []
        payloadPtr = 0
        payloadLength = None

        sequenceNumberExpected = 1

        txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        endOfMessage_flag = False

        state = CanTpState.IDLE

        timeoutTimer.start()
        while endOfMessage_flag is False:

            rxPdu = self.getNextBufferedMessage()

            if rxPdu is not None:
                N_PCI = (rxPdu[N_PCI_INDEX] & 0xF0) >> 4
                if state == CanTpState.IDLE:
                    if N_PCI == CanTpMessageType.SINGLE_FRAME:
                        payloadLength = rxPdu[N_PCI_INDEX & 0x0F]
                        payload = rxPdu[SINGLE_FRAME_DATA_START_INDEX: SINGLE_FRAME_DATA_START_INDEX + payloadLength]
                        endOfMessage_flag = True
                    elif N_PCI == CanTpMessageType.FIRST_FRAME:
                        payload = rxPdu[FIRST_FRAME_DATA_START_INDEX:]
                        payloadLength = ((rxPdu[FIRST_FRAME_DL_INDEX_HIGH] & 0x0F) << 8) + rxPdu[FIRST_FRAME_DL_INDEX_LOW]
                        payloadPtr = self.__maxPduLength - 1
                        state = CanTpState.SEND_FLOW_CONTROL
                elif state == CanTpState.RECEIVING_CONSECUTIVE_FRAME:
                    if N_PCI == CanTpMessageType.CONSECUTIVE_FRAME:
                        sequenceNumber = rxPdu[CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX] & 0x0F
                        if sequenceNumber != sequenceNumberExpected:
                            raise Exception("Consecutive frame sequence out of order")
                        else:
                            sequenceNumberExpected = (sequenceNumberExpected + 1) % 16
                        payload += rxPdu[CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX:]
                        payloadPtr += (self.__maxPduLength)
                    else:
                        raise Exception("Unexpected PDU received")

            if state == CanTpState.SEND_FLOW_CONTROL:
                txPdu[N_PCI_INDEX] = 0x30
                txPdu[FLOW_CONTROL_BS_INDEX] = 0
                txPdu[FLOW_CONTROL_STMIN_INDEX] = 0x1E
                self.transmit(txPdu)
                state = CanTpState.RECEIVING_CONSECUTIVE_FRAME

            if payloadLength is not None:
                if payloadPtr >= payloadLength:
                    endOfMessage_flag = True

            if timeoutTimer.isExpired():
                raise Exception("Timeout in waiting for message")

        return list(payload[:payloadLength])

    ##
    # @brief clear out the receive list
    def clearBufferedMessages(self):
        self.__recvBuffer = []

    ##
    # @brief retrieves the next message from the received message buffers
    # @return list, or None if nothing is on the receive list
    def getNextBufferedMessage(self):
        length = len(self.__recvBuffer)
        if(length != 0):
            return self.__recvBuffer.pop(0)
        else:
            return None

    ##
    # @brief the listener callback used when a message is received
    def callback_onReceive(self, msg):
        if(msg.arbitration_id == self.__resId):
            # print("CanTp Instance received message")
            # print(unpack('BBBBBBBB', msg.data))
            self.__recvBuffer.append(msg.data[self.__pduStartIndex:])

    ##
    # @brief function to decode the StMin parameter
    @staticmethod
    def decode_stMin(val):
        if (val <= 0x7F):
            time = val / 1000
            return time
        elif (
                (val >= 0xF1) &
                (val <= 0xF9)
        ):
            time = (val & 0x0F) / 10000
            return time
        else:
            raise Exception("Unknown STMin time")

    def create_blockList(self, payload, blockSize):

        blockList = []
        currBlock = []
        currPdu = []

        payloadPtr = 0
        blockPtr = 0

        payloadLength = len(payload)
        pduLength = self.__maxPduLength
        blockLength = blockSize * pduLength

        working = True
        while(working):
            if (payloadPtr + pduLength) >= payloadLength:
                working = False
                currPdu = fillArray(payload[payloadPtr:], pduLength)
                currBlock.append(currPdu)
                blockList.append(currBlock)

            if working:
                currPdu = payload[payloadPtr:payloadPtr+pduLength]
                currBlock.append(currPdu)
                payloadPtr += pduLength
                blockPtr += pduLength

                if(blockPtr == blockLength):
                    blockList.append(currBlock)
                    currBlock = []
                    blockPtr = 0

        return blockList

    def transmit(self, data, functionalReq=False):

        # check functional request
        if functionalReq:
            raise Exception("Functional requests are currently not supported")
        else:
            canMsg = can.Message(arbitration_id=self.__reqId, extended_id=False)
            canMsg.dlc = 8

        canMsg.data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        if (
                (self.__addressingType == CanTpAddressingTypes.NORMAL) |
                (self.__addressingType == CanTpAddressingTypes.NORMAL_FIXED)
        ):
            canMsg.data = data
        elif self.__addressingType == CanTpAddressingTypes.MIXED:
            canMsg.data[0] = self.__N_AE
            canMsg.data[1:] = data
        else:
            raise Exception("Do not know how to deal with this type of addressing scheme")

        self.__bus.send(canMsg)


if __name__ == "__main__":
    pass
