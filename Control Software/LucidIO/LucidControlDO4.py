"""
LucidControl Digital Output USB Module DO4 implementation
@author: Klaus Ummenhofer
"""

from LucidControl import LucidControl
from Cmd import Cmd
from lucidIo.Values import ValueDI1
from lucidIo import IoReturn
import struct

class LCDO4Mode(object):
    """Module Operation Mode values
    
    This class contains integer values representing the Operation
    Modes. They are supposed to be used with setParamMode and
    getParamMode commands. 
    """
    INACTIVE        = 0x00
    REFLECT_VALUE   = 0x01
    ON_OFF          = 0x08
    CYCLE           = 0x0A


class LCDO4DeviceType(object):
    DO_NONE     = (0x0000, "Not identified")
    DO_SSR      = (0x1000, "SOLID STATE 24 V")
    DO_SPDT     = (0x1100, "SPDT RELAY")
    DO_OC       = (0x1200, "OPEN COLLECTOR")
    

class _LCDO4ParamAddress(object):
    VALUE       = 0x1000
    MODE        = 0x1100
    FLAGS       = 0x1101
    CYCLE_TIME  = 0x1110
    DUTY_CYCLE  = 0x1111
    ON_DELAY    = 0x1112
    ON_HOLD     = 0x1113

    
class _LCDO4Flag(object):
    CAN_RETRIGGER   = 0x01
    CAN_CANCEL      = 0x02
    INVERTED        = 0x04


class LucidControlDO4(LucidControl):
    """LucidControl Digital Output USB Module DO4 class
    """
    
    def getIo(self, channel, value):
        """Get the value or state of one digital output channel.
            
        This method calls the GetIo function of the module and returns
        the value or state of the digital output channel.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(value, ValueDI1):
            raise TypeError('Expected value as ValueDI1, got %s' %
                (type(value)))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        cmd = Cmd(self.com)
        return cmd.getIo(channel, value)
        

    def getIoGroup(self, channels, values):
        """Get the values or states of a group of digital output
            channels.
            
        This method calls the GetIoGroup function of the module and
            returns the values or states of a group of output channels.
        
        Args:
            channels: Tuple with 4 boolean values (one for each channel).
                A channel is only read if the corresponding channel is
                true.
            values: Digital values.
                A tuple with 4 digital value objects. The function fills
                the objects with read data.
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channels, tuple):
            raise TypeError('Expected channels as tuple with 4 channels \
                 (bools), got %s' % (type(channels)))
        
        if (len(channels) < 4):
            raise TypeError('Expected 4 channels, got %d' % (len(channels)))
        
        for x in range(4):
            if not isinstance(channels[x], int):
                raise TypeError('Expected channel as bool, got %s' %
                     (type(channels[x])))    
            
        if not isinstance(values, tuple):
            raise TypeError('Expected values as tuple with 4 values, got %s' 
                % (type(values)))
        
        if (len(values) < 4):
            raise TypeError('Expected 4 values, got %d' % (len(values)))
            
        for x in range(4):
            if not isinstance(values[x], ValueDI1):
                raise TypeError('Expected value as ValueDI1, got %s' %
                    (type(values[x])))
            
        cmd = Cmd(self.com)
        return cmd.getIoGroup(channels, values)
            
 
   
    def setIo(self, channel, value):
        """Write the value or state of one digital output channel.
        
        This method calls the SetIo function of the module and writes
            the value or state of the digital output channel.
            
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            value: Digital value object of type ValueDI1, initialized
                with the updated data.
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(value, ValueDI1):
            raise TypeError('Expected value as ValueDI1, got %s'
                % (type(value)))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        cmd = Cmd(self.com)
        return cmd.setIo(channel, value)



    def setIoGroup(self, channels, values):
        """Write values or states of a group of output channels.
        
        This method calls the SetIoGroup function of the module and
            writes the values or states of a group of output channels.
            
        Args:
            channels: Tuple with 4 boolean values (one for each channel).
                A channel is only written if the corresponding channel is
                true.
            values: Digital values.
                A tuple with 4 digital value objects. The values of the
                objects are written to the output channels.
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channels, tuple):
            raise TypeError('Expected channels as tuple with 4 channels \
                (bools), got %s' % (type(channels)))
        
        if (len(channels) < 4):
            raise TypeError('Expected 4 channels, got %d' % (len(channels)))
        
        for x in range(4):
            if not isinstance(channels[x], int):
                raise TypeError('Expected channel as bool, got %s' %
                    (type(channels[x])))
            
        if not isinstance(values, tuple):
            raise TypeError('Expected values as tuple with 4 values, got %s' %
                (type(values)))
        
        if (len(values) < 4):
            raise TypeError('Expected 4 values, got %d' % (len(values)))
        
        for x in range(4):
            if not isinstance(values[x], ValueDI1):
                raise TypeError('Expected values as ValueDI1, got %s' %
                    (type(values[x])))
            
        cmd = Cmd(self.com)
        return cmd.setIoGroup(channels, values)
    
    
    def getParamValue(self, channel, value):
        """Get the Configuration Parameter "Value" of a digital
            output channel.
            
        This method calls the GetParam function of the module and returns
        the value of the Configuration Parameter "Value".
        
        The Configuration Parameter "Value" contains the current value
        or state of the output channel.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(value, ValueDI1):
            raise TypeError('Expected value as ValueDI1, got %s' %
                (type(value)))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.VALUE, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            value._setData(data)
        return ret

    
    def setParamValueDefault(self, channel, persistent):
        """Set the Configuration Parameter "Value" of a digital
            output to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Value" to the default value.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
               
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.VALUE,
            channel, persistent)

    
    def setParamValue(self, channel, persistent, value):
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(value, ValueDI1):
            raise TypeError('Expected value as ValueDI1, got %s' %
                (type(value)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        data = bytearray()
        cmd = Cmd(self.com)
        
        value._getData(data)
        return cmd.setParam(_LCDO4ParamAddress.VALUE, channel, persistent, data)


    
    def getParamMode(self, channel, mode):
        """Get the Configuration Parameter "Mode" of the digital output
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Mode".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            mode: Operation Mode as a list with one LCDO4Mode integer value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
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
        ret = cmd.getParam(_LCDO4ParamAddress.MODE, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] == LCDO4Mode.INACTIVE:
                mode[0] = LCDO4Mode.INACTIVE
            elif data[0] == LCDO4Mode.REFLECT_VALUE:
                mode[0] = LCDO4Mode.REFLECT_VALUE
            elif data[0] == LCDO4Mode.ON_OFF:
                mode[0] = LCDO4Mode.REFLECT_VALUE
            elif data[0] == LCDO4Mode.CYCLE:
                mode[0] = LCDO4Mode.CYCLE
            else:
                mode[0] = LCDO4Mode.INACTIVE
        
        return ret
        

    def setParamModeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Mode" of a digital
            output channel to the default value.
            
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.MODE, channel, persistent)
    
    
    def setParamMode(self, channel, persistent, mode):
        """Set the Configuration Parameter "Mode" of a digital
            output channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Mode".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            mode: Operation Mode as LCDO4Mode integer value
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range    
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(mode, int):
            raise TypeError('Expected mode as int, got %s' % (type(mode)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        data = bytearray([mode])
        
        cmd = Cmd(self.com)
        return cmd.setParam(_LCDO4ParamAddress.MODE, channel, persistent, data)

    

    def setParamFlagsDefault(self, channel, persistent):
        """Set the Configuration Parameter "Flags" of a digital
            output to the default value.
            
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.FLAGS,
            channel, persistent)

    
    def getParamFlagCanCancel(self, channel, canCancel):
        """Get the Configuration Parameter Flag "Can Cancel".
        
        This method calls the GetParam function of the module and
        returns the Configuration Flag "Can Cancel".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            canCancel: Parameter Flag "Can Cancel" as a list containing
                one boolean value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(canCancel, list):
            raise TypeError('Expected canCancel as list, got %s' %
                type(canCancel))
            
        if len(canCancel) < 1:
            raise TypeError('Expected canCancel as list with 1 bool, got %d' %
                len(canCancel))
        
        if not isinstance(canCancel[0], int):
            raise TypeError('Expected canCancel[0] as bool, got %s' %
                type(canCancel[0]))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] & _LCDO4Flag.CAN_CANCEL:
                canCancel[0] = True
            else:
                canCancel[0] = False
        return ret         
        
    
    def setParamFlagCanCancel(self, channel, persistent, canCancel):
        """Set the Configuration Parameter Flag "Can Cancel".
        
        This method calls the SetParam function of the module and
        sets the Configuration Flag "Can Cancel".
        
         Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            canCancel: Parameter Flag "Can Cancel" as boolean
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(canCancel, bool):
            raise TypeError('Expected canCancel as bool, got %s' %
                (type(canCancel)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')          
        
        # Read current flags
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            data[0] &= ~_LCDO4Flag.CAN_CANCEL
            if (canCancel == True):
                data[0] |= _LCDO4Flag.CAN_CANCEL
                
            ret = cmd.setParam(_LCDO4ParamAddress.FLAGS, channel,
                persistent, data)
        
        return ret
            
        
    
    def getParamFlagCanRetrigger(self, channel, canRetrigger):
        """Get the Configuration Parameter Flag "Can Retrigger".
        
        This method calls the GetParam function of the module and
        returns the Configuration Flag "Can Retrigger".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            canRetrigger: Parameter Flag "Can Retrigger" as a list containing
                one boolean value
                
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(canRetrigger, list):
            raise TypeError('Expected canRetrigger as list, got %s' %
                type(canRetrigger))
            
        if len(canRetrigger) < 1:
            raise TypeError('Expected canRetrigger as list with 1 bool, got %d' %
                len(canRetrigger))
        
        if not isinstance(canRetrigger[0], int):
            raise TypeError('Expected canRetrigger[0] as bool, got %s' %
                type(canRetrigger[0]))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] & _LCDO4Flag.CAN_RETRIGGER:
                canRetrigger[0] = True
            else:
                canRetrigger[0] = False
        return ret         


    
    def setParamFlagCanRetrigger(self, channel, persistent, canRetrigger):
        """Set the Configuration Parameter Flag "Can Retrigger".
        
        This method calls the SetParam function of the module and
        sets the Configuration Flag "Can Retrigger".
        
         Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            canRetrigger: Parameter Flag "Can Retrigger" as boolean
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(canRetrigger, bool):
            raise TypeError('Expected canRetrigger as bool, got %s' %
                (type(canRetrigger)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')          
        
        # Read current flags
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            data[0] &= ~_LCDO4Flag.CAN_RETRIGGER
            if (canRetrigger == True):
                data[0] |= _LCDO4Flag.CAN_RETRIGGER
        
        ret = cmd.setParam(_LCDO4ParamAddress.FLAGS, channel, persistent, data)
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
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
        ret = cmd.getParam(_LCDO4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] & _LCDO4Flag.INVERTED:
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(inverted, bool):
            raise TypeError('Expected inverted as bool, got %s' %
                (type(inverted)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')          
        
        # Read current flags
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.FLAGS, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            data[0] &= ~_LCDO4Flag.INVERTED
            if (inverted == True):
                data[0] |= _LCDO4Flag.INVERTED
        
        ret = cmd.setParam(_LCDO4ParamAddress.FLAGS, channel, persistent, data)
        return ret


    
    def getParamCycleTime(self, channel, cycleTime):
        """Get the Configuration Parameter "Cycle Time" of the digital output
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Cycle Time".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            cycleTime: Parameter "Cycle Time" as a list containing one integer
                value in microseconds
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(cycleTime, list):
            raise TypeError('Expected cycleTime as list, got %s' %
                type(cycleTime))
        
        if len(cycleTime) < 1:
            raise TypeError('Expected cycleTime as list with 1 int, got %d' %
                len(cycleTime))
        
        if not isinstance(cycleTime[0], int):
            raise TypeError('Expected cycleTime[0] as int, got %s' %
                type(cycleTime[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.CYCLE_TIME, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            cycleTime[0] = struct.unpack("<I", buffer(data))[0]
        else:
            cycleTime[0] = 0
            
        return ret
        
    
    def setParamCycleTimeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Cycle Time" of a digital
            output to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Cycle Time" to the default value.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.CYCLE_TIME,
            channel, persistent)
    
    
    
    def setParamCycleTime(self, channel, persistent, cycleTime):
        """Set the Configuration Parameter "Cycle Time" of a digital
            output channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Cycle Time".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            cycleTime: Parameter "Cycle Time" in microseconds
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or cycleTime value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(cycleTime, int):
            raise TypeError('Expected cycleTime as int, got %s' %
                (type(cycleTime)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (cycleTime < 0) | (cycleTime >= pow(2, 32)):
            raise ValueError('Cycle Time out of range')

        data = bytearray(struct.pack("<I", cycleTime))
        cmd = Cmd(self.com)
        
        return cmd.setParam(_LCDO4ParamAddress.CYCLE_TIME, channel,
            persistent, data) 


        
    
    def getParamDutyCycle(self, channel, dutyCycle):
        """Get the Configuration Parameter "Duty Cycle" of the digital output
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Duty Cycle".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            dutyCycle: Parameter "Duty Cycle" as a list containing one integer
                value  (Duty Cycle as 1/1000)
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(dutyCycle, list):
            raise TypeError('Expected dutyCycle as list, got %s' %
                type(dutyCycle))
        
        if len(dutyCycle) < 1:
            raise TypeError('Expected dutyCycle as list with 1 int, got %d' %
                len(dutyCycle))
        
        if not isinstance(dutyCycle[0], int):
            raise TypeError('Expected dutyCycle[0] as int, got %s' %
                type(dutyCycle[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.DUTY_CYCLE, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            dutyCycle[0] = struct.unpack("<H", buffer(data))[0]
        else:
            dutyCycle[0] = 0
        return ret
        
        
    
    def setParamDutyCycleDefault(self, channel, persistent):
        """Set the Configuration Parameter "Duty Cycle" of a digital
            output to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Duty Cycle" to the default value.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.DUTY_CYCLE, channel,
            persistent)
    
    
    
    def setParamDutyCycle(self, channel, persistent, dutyCycle):
        """Set the Configuration Parameter "Duty Cycle" of a digital
            output channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Duty Cycle".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            dutyCycle: Parameter "Duty Cycle" in 1/1000
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or dutyCycle value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(dutyCycle, int):
            raise TypeError('Expected dutyCycle as int, got %s' %
                (type(dutyCycle)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (dutyCycle < 0) | (dutyCycle > 1000):
            raise ValueError('DutyCycle out of range')
        
        data = bytearray(struct.pack("<H", dutyCycle))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCDO4ParamAddress.DUTY_CYCLE, channel,
            persistent, data) 
    
    
    
    def getParamOnHold(self, channel, onHold):
        """Get the Configuration Parameter "On Hold" of the digital output
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "On Hold".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            onHold: Parameter "On Hold" as a list containing one integer
                value in microseconds
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(onHold, list):
            raise TypeError('Expected onHold as list, got %s' %
                type(onHold))
        
        if len(onHold) < 1:
            raise TypeError('Expected onHold as list with 1 int, got %d' %
                len(onHold))
        
        if not isinstance(onHold[0], int):
            raise TypeError('Expected onHold[0] as int, got %s' %
                type(onHold[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.ON_HOLD, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            onHold[0] = struct.unpack("<I", buffer(data))[0]
        else:
            onHold[0] = 0
        return ret    



    def setParamOnHoldDefault(self, channel, persistent):
        """Set the Configuration Parameter "On Hold" of a digital
            output to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "On Hold" to the default value.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.ON_HOLD,
            channel, persistent)
    
    
    
    def setParamOnHold(self, channel, persistent, onHold):
        """Set the Configuration Parameter "On Hold" of a digital
            output channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "On Hold".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            onHold: Parameter "On Hold" in microseconds
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or onHold value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(onHold, int):
            raise TypeError('Expected onHold as int, got %s' % (type(onHold)))
    
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (onHold < 0) | (onHold >= pow(2, 32)):
            raise ValueError('On Hold out of range')
        
        data = bytearray(struct.pack("<I", onHold))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCDO4ParamAddress.ON_HOLD, channel,
            persistent, data) 
    
    
    
    def getParamOnDelay(self, channel, onDelay):
        """Get the Configuration Parameter "On Delay" of the digital output
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "On Delay".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            onDelay: Parameter "On Delay" as a list containing one integer
                value in microseconds
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
            
        if not isinstance(onDelay, list):
            raise TypeError('Expected onDelay as list, got %s' %
                type(onDelay))
        
        if len(onDelay) < 1:
            raise TypeError('Expected onDelay as list with 1 int, got %d' %
                len(onDelay))
        
        if not isinstance(onDelay[0], int):
            raise TypeError('Expected onDelay[0] as int, got %s' %
                type(onDelay[0])) 
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCDO4ParamAddress.ON_DELAY, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            onDelay[0] = struct.unpack("<I", buffer(data))[0]
        else:
            onDelay[0] = 0
        return ret



    def setParamOnDelayDefault(self, channel, persistent):
        """Set the Configuration Parameter "On Delay" of a digital
            output to the default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "On Delay" to the default value.
        
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
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')   
        
        cmd = Cmd(self.com)
        return cmd.setParamDefault(_LCDO4ParamAddress.ON_DELAY, channel,
            persistent)

    
    def setParamOnDelay(self, channel, persistent, onDelay):
        """Set the Configuration Parameter "On Delay" of a digital
            output channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "On Delay".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            onDelay: Parameter "On Delay" in microseconds
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or onDelay value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % (type(channel)))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                (type(persistent)))
        
        if not isinstance(onDelay, int):
            raise TypeError('Expected onDelay as int, got %s' % (type(onDelay)))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        if (onDelay < 0) | (onDelay >= pow(2, 32)):
            raise ValueError('On Delay out of range')

        data = bytearray(struct.pack("<I", onDelay))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCDO4ParamAddress.ON_DELAY, channel,
            persistent, data) 
    
    
    
    def getDeviceTypeName(self):
        """Get device type name as string.
        
        Returns:
            String of the device type name
        
        Raises:
            ValueError: ID data not valid
        """
        if self.id.validData == True:
            if (self.id.deviceType == LCDO4DeviceType.DO_SSR[0]):
                return LCDO4DeviceType.DO_SSR[1]
            elif (self.id.deviceType == LCDO4DeviceType.DO_OC[0]):
                return LCDO4DeviceType.DO_OC[1]
            elif (self.id.deviceType == LCDO4DeviceType.DO_SPDT[0]):
                return LCDO4DeviceType.DO_SPDT[1]
            else:
                return "Not Identified"
        else:
            raise ValueError('ID data structure not valid')
    
    
    def getDeviceType(self):
        """Get device type.
        
        Returns:
            Device type
        """
        if (self.id.validData == True):
            return self.id.deviceType
        else:
            return LCDO4DeviceType.DO_NONE
    
    def __init__(self, portName):
        """
        Constructor of LucidControl Digital Output USB Module class
        """
        LucidControl.__init__(self, portName)
        self.nrOfChannels = 4
        
        