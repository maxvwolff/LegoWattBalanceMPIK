'''
Created on 13.06.2013
LucidControl Digital Input USB Module DI4 implementation
@author: Klaus Ummenhofer
'''
from LucidControl import LucidControl
from Cmd import Cmd
from lucidIo.Values import ValueDI1, ValueCNT2
from lucidIo import IoReturn
import struct

class LCDI4Mode(object):
    """Module Operation Mode values
    
    This class contains integer values representing the Operation
    Modes. They are supposed to be used with setParamMode and
    getParamMode commands. 
    """
    INACTIVE            = 0x00
    REFLECT_VALUE       = 0x01
    RISING_EDGE         = 0x10
    FALLING_EDGE        = 0x11
    COUNT               = 0x20


class LCDI4DeviceType(object):
    DI_NONE             = (0x0000, "Not identified")
    DI_5                = (0x1000, "5 V")
    DI_10               = (0x1001, "10 V")
    DI_12               = (0x1002, "12 V")
    DI_15               = (0x1003, "15 V")
    DI_20               = (0x1004, "20 V")
    DI_24               = (0x1005, "24 V")

    
class _LCDI4ParamAddress(object):
    VALUE       = 0x1000
    MODE        = 0x1100
    FLAGS       = 0x1101
    SCAN_TIME   = 0x1111
    COUNT_TIME  = 0x1112

    
class _LCDI4Flag(object):
    ADD_COUNTER          = 0x01
    RESET_COUNTER_READ   = 0x02
    INVERTED             = 0x04


class LucidControlDI4(LucidControl):
    """LucidControl Digital Input USB Module DI4 class
    """

    def getIo(self, channel, value):
        """Get the value or state of one digital input channel.
            
        This method calls the GetIo function of the module and returns
        the value or of the digital input channel.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            value: Digital value object of type ValueDI1 or ValueCNT2.
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(value, (ValueDI1, ValueCNT2)):
            raise TypeError('Expected value as ValueDI1 or ValueCNT2, \
                got %s' % type(value))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        cmd = Cmd(self.com)
        return cmd.getIo(channel, value)


    def getIoGroup(self, channels, values):
        """Get the values of a group of digital input channels.
            
        This method calls the GetIoGroup function of the module and
            returns the values of a group of input channels.
        
        Args:
            channels: Tuple with 4 boolean values (one for each channel).
                A channel is only read if the corresponding channel is
                true.
            values: Digital values.
                A tuple with 4 digital value objects of type ValueDI1 or
                ValueCNT2. The function fills the objects with read data.
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channels, tuple):
            raise TypeError('Expected channels as a tuple with 4 channels \
                (bools), got %s' % type(channels))

        if (len(channels) < 4):
            raise TypeError('Expected 4 channels, got %d' % len(channels))
        
        for x in range(4):
            if not isinstance(channels[x], int):
                raise TypeError('Expected channel as bool, got %s' %
                    type(channels[x]))

        if not isinstance(values, tuple):
            raise TypeError('Expected values as a tuple with 4 values, got %s'
                 % type(values))

        if (len(values) < 4):
            raise TypeError('Expected 4 values, got %d' % len(values))

        for x in range(4):
            if not isinstance(values[x], (ValueDI1, ValueCNT2)):
                raise TypeError('Expected value as ValueDI1 or ValueCNT2, \
                    got %s' % type(values[x]))

        cmd = Cmd(self.com)
        return cmd.getIoGroup(channels, values)



    def getParamValue(self, channel, value):
        """Get the Configuration Parameter "Value" of a digital
            input channel.
            
        This method calls the GetParam function of the module and returns
            the value of the Configuration Parameter "Value".
        
            The Configuration Parameter "Value" contains the current
            value of the input channel.
        
        It is recommended to call getIo instead of this method.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            value: Digital value object of type ValueDI1.
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(value, ValueDI1):
            raise TypeError('Expected value as ValueDI1, got %s' %
                type(value))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.VALUE, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            value._setData(data)
        return ret


    def getParamMode(self, channel, mode):
        """Get the Configuration Parameter "Mode" of the digital input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Mode".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            mode: Operation Mode as a list with one LCDI4Mode integer value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(mode, list):
            raise TypeError('Expected mode as list, got %s' % type(mode))
        
        if len(mode) < 1:
            raise TypeError('Expected mode as list with 1 int, got %d' %
                len(mode))
        
        if not isinstance(mode[0], int):
            raise TypeError('Expected mode[0] as int, got %s' % type(mode[0]))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     

        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.MODE, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] == LCDI4Mode.INACTIVE:
                mode[0] = LCDI4Mode.INACTIVE
            elif data[0] == LCDI4Mode.REFLECT_VALUE:
                mode[0] = LCDI4Mode.REFLECT_VALUE
            elif data[0] == LCDI4Mode.RISING_EDGE:
                mode[0] = LCDI4Mode.RISING_EDGE
            elif data[0] == LCDI4Mode.FALLING_EDGE:
                mode[0] = LCDI4Mode.FALLING_EDGE
            elif data[0] == LCDI4Mode.COUNT:
                mode[0] = LCDI4Mode.COUNT
            else:
                mode[0] = LCDI4Mode.INACTIVE

        return ret


    def setParamModeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Mode" of a digital
            input channel to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Mode" to the default value.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   

        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDI4ParamAddress.MODE, channel, persistent)



    def setParamMode(self, channel, persistent, mode):
        """Set the Configuration Parameter "Mode" of a digital
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Mode".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            mode: Operation Mode as LCDI4Mode integer value
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range    
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))

        if not isinstance(mode, int):
            raise TypeError('Expected mode as int, got %s' % type(mode))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        data = bytearray([mode])

        cmd = Cmd(self.com)
        return cmd.setParam(_LCDI4ParamAddress.MODE, channel, persistent, data)


    def setParamFlagsDefault(self, channel, persistent):
        """Set the Configuration Parameter "Flags" of a digital
            input to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Flags" to the default value.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   

        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDI4ParamAddress.FLAGS, channel, persistent)



    def getParamFlagAddCounter(self, channel, addCounter):
        """Get the Configuration Parameter Flag "Add Counter".
        
        This method calls the GetParam function of the module and
        returns the Configuration Flag "Add Counter".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            addCounter: Parameter Flag "Add Counter" as a list containing
                one boolean value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' %
                type(channel))

        if not isinstance(addCounter, list):
            raise TypeError('Expected addCounter as list, got %s' %
                type(addCounter))
            
        if len(addCounter) < 1:
            raise TypeError('Expected addCounter as list with 1 bool, got %d' %
                len(addCounter))
        
        if not isinstance(addCounter[0], int):
            raise TypeError('Expected addCounter[0] as bool, got %s' %
                type(addCounter[0]))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.FLAGS, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] & _LCDI4Flag.ADD_COUNTER:
                addCounter[0] = True
            else:
                addCounter[0] = False
        return ret


    def setParamFlagAddCounter(self, channel, persistent, addCounter):
        """Set the Configuration Parameter Flag "Add Counter".
        
        This method calls the SetParam function of the module and
        sets the Configuration Flag "Add Counter".
        
         Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            addCounter: Parameter Flag "Add Counter" as boolean
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))

        if not isinstance(addCounter, bool):
            raise TypeError('Expected addCounter as bool, got %s' %
                type(addCounter))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        # Read current flags
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.FLAGS, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            data[0] &= ~_LCDI4Flag.ADD_COUNTER
            if (addCounter == True):
                data[0] |= _LCDI4Flag.ADD_COUNTER

            ret = cmd.setParam(_LCDI4ParamAddress.FLAGS, channel, persistent, data)

        return ret


    
    def getParamFlagResetCounterRead(self, channel, resetCounterRead):
        """Get the Configuration Parameter Flag "Reset Counter on Read".
        
        This method calls the GetParam function of the module and
        returns the Configuration Flag "Reset Counter on Read".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            resetCounterRead: Parameter Flag "Reset Counter on Read"
                as a list containing one boolean value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(resetCounterRead, list):
            raise TypeError('Expected resetCounterRead as list, got %s' %
                type(resetCounterRead))
            
        if len(resetCounterRead) < 1:
            raise TypeError('Expected resetCounterRead as list with 1 bool, \
                got %d' % len(resetCounterRead))
        
        if not isinstance(resetCounterRead[0], int):
            raise TypeError('Expected resetCounterRead[0] as bool, got %s' %
                type(resetCounterRead[0]))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.FLAGS, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] & _LCDI4Flag.RESET_COUNTER_READ:
                resetCounterRead[0] = True
            else:
                resetCounterRead[0] = False
        return ret



    def setParamFlagResetCounterRead(self, channel, persistent,
        resetCounterRead):
        """Set the Configuration Parameter Flag "Reset Counter on Read".
        
        This method calls the SetParam function of the module and
        sets the Configuration Flag "Reset Counter on Read".
        
         Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            resetCounterRead: Parameter Flag 
                "Reset Counter on Read" as boolean
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))

        if not isinstance(resetCounterRead, bool):
            raise TypeError('Expected resetCounterRead as bool, got %s' %
                type(resetCounterRead))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')          

        # Read current flags
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.FLAGS, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            data[0] &= ~_LCDI4Flag.RESET_COUNTER_READ
            if (resetCounterRead == True):
                data[0] |= _LCDI4Flag.RESET_COUNTER_READ

        ret = cmd.setParam(_LCDI4ParamAddress.FLAGS, channel, persistent, data)
        return ret



    def getParamFlagInverted(self, channel, inverted):
        """Get the Configuration Parameter Flag "Inverted".
        
        This method calls the GetParam function of the module and
        returns the Configuration Flag "Inverted".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            inverted: Parameter Flag "Inverted" as a list containing
                one boolean value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(inverted, list):
            raise TypeError('Expected inverted as list, got %s' %
                type(inverted))
            
        if len(inverted) < 1:
            raise TypeError('Expected inverted as list with 1 bool, got %d' %
                len(inverted))
        
        if not isinstance(inverted[0], int):
            raise TypeError('Expected inverted[0] as bool, got %s' %
                type(inverted[0]))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] & _LCDI4Flag.INVERTED:
                inverted[0] = True
            else:
                inverted[0] = False
        return ret

 
    
    def setParamFlagInverted(self, channel, persistent, inverted):
        """Set the Configuration Parameter Flag "Inverted".
        
        This method calls the SetParam function of the module and
        sets the Configuration Flag "Inverted".
        
         Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            inverted: Parameter Flag "Inverted" as boolean
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))
        
        if not isinstance(inverted, bool):
            raise TypeError('Expected inverted as bool, got %s' %
                type(inverted))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        # Read current flags
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            data[0] &= ~_LCDI4Flag.INVERTED
            if (inverted == True):
                data[0] |= _LCDI4Flag.INVERTED
        
        ret = cmd.setParam(_LCDI4ParamAddress.FLAGS, channel, persistent, data)
        
        return ret


    def getParamScanTime(self, channel, scanTime):
        """Get the Configuration Parameter "Scan Time" of the digital input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Scan Time".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            scanTime: Parameter "Scan Time" as a list containing one integer
                value in microseconds
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
            
        if not isinstance(scanTime, list):
            raise TypeError('Expected scanTime as list, got %s' %
                type(scanTime))
        
        if len(scanTime) < 1:
            raise TypeError('Expected scanTime as list with 1 int, got %d' %
                len(scanTime))
        
        if not isinstance(scanTime[0], int):
            raise TypeError('Expected scanTimel[0] as int, got %s' %
                type(scanTime[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.SCAN_TIME, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            scanTime[0] = struct.unpack("<I", buffer(data))[0]
        else:
            scanTime[0] = 0
            
        return ret
        
    
    def setParamScanTimeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Scan Time" of a digital
            input to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Scan Time" to the default value.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDI4ParamAddress.SCAN_TIME, channel,
            persistent)
    
    
    
    def setParamScanTime(self, channel, persistent, scanTime):
        """Set the Configuration Parameter "Scan Time" of a digital
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Scan Time".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            scanTime: Parameter "Scan Time" in microseconds
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or cycleTime value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if not isinstance(scanTime, int):
            raise TypeError('Expected scanTime as int, got %s' % type(scanTime))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (scanTime < 0) | (scanTime >= pow(2, 32)):
            raise ValueError('Scan Time out of range')

        data = bytearray(struct.pack("<I", scanTime))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCDI4ParamAddress.SCAN_TIME,
            channel, persistent, data) 


    def getParamCountTime(self, channel, countTime):
        """Get the Configuration Parameter "Count Time" of the digital input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Count Time".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            countTime: Parameter "Count Time" as a list containing one
                integer value in microseconds
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """        
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % 
                type(channel))
            
        if not isinstance(countTime, list):
            raise TypeError('Expected countTime as list, got %s' %
                type(countTime))
        
        if len(countTime) < 1:
            raise TypeError('Expected countTime as list with 1 int, got %d' %
                len(countTime))
        
        if not isinstance(countTime[0], int):
            raise TypeError('Expected countTime[0] as int, got %s' %
                type(countTime[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDI4ParamAddress.COUNT_TIME, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            countTime[0] = struct.unpack("<I", buffer(data))[0]
        else:
            countTime[0] = 0
            
        return ret
        
    
    def setParamCountTimeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Count Time" of a digital
            input to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Count Time" to the default value.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDI4ParamAddress.COUNT_TIME, channel, persistent)
    
    
    
    def setParamCountTime(self, channel, persistent, countTime):
        """Set the Configuration Parameter "Count Time" of a digital
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Count Time".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            countTime: Parameter "Count Time" in microseconds
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or cycleTime value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistant as bool, got %s' % 
                type(persistent))
        
        if not isinstance(countTime, int):
            raise TypeError('Expected countTime as int, got %s' % 
                type(countTime))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (countTime < 0) | (countTime >= pow(2, 32)):
            raise ValueError('Count Time out of range')

        data = bytearray(struct.pack("<I", countTime))
        cmd = Cmd(self.com)
        
        return cmd.setParam(_LCDI4ParamAddress.COUNT_TIME, channel, persistent, data)         
    
   
    def getDeviceTypeName(self):
        """Get device type name as string.
        
        Returns:
            String of the device type name
        
        Raises:
            ValueError: ID data not valid
        """
        if self.id.validData == True:
            if (self.id.deviceType == LCDI4DeviceType.DI_5[0]):
                return LCDI4DeviceType.DI_5[1]
            elif (self.id.deviceType == LCDI4DeviceType.DI_10[0]):
                return LCDI4DeviceType.DI_10[1]
            elif (self.id.deviceType == LCDI4DeviceType.DI_12[0]):
                return LCDI4DeviceType.DI_12[1]
            elif (self.id.deviceType == LCDI4DeviceType.DI_15[0]):
                return LCDI4DeviceType.DI_15[1]
            elif (self.id.deviceType == LCDI4DeviceType.DI_20[0]):
                return LCDI4DeviceType.DI_20[1]    
            elif (self.id.deviceType == LCDI4DeviceType.DI_24[0]):
                return LCDI4DeviceType.DI_24[1]
            else:
                return "Not Identified"
            
    def getDeviceType(self):
        """Get device type.
        
        Returns:
            Device type
        """
        if (self.id.validData == True):
            return self.id.deviceType
        else:
            return LCDI4DeviceType.DI_NONE
            
                
    def __init__(self, portName):
        """
        Constructor of LucidControl Digital Input USB Module class
        """
        LucidControl.__init__(self, portName)
        self.nrOfChannels = 4
        
        