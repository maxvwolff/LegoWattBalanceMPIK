'''
Created on 15.06.2013
LucidControl RTD Input USB Module RT4 implementation
@author: Klaus Ummenhofer
'''
from LucidControl import LucidControl
from Cmd import Cmd
from lucidIo import IoReturn
import struct
from lucidIo.Values import ValueRMU2, ValueTMS2, ValueTMS4

class LCRT4Mode(object):
    """Module Operation Mode values
    
    This class contains integer values representing the Operation
    Modes. They are supposed to be used with setParamMode and
    getParamMode commands. 
    """
    INACTIVE            = 0x00
    STANDARD            = 0x01

class LCRT4CalMode(object):
    OPEN                = 0x10
    SHORT               = 0x00
    

class LCRT4DeviceType(object):
    RT_NONE             = (0x1000, "Not identified")
    RT_PT1000           = (0x1000, "PT 1000")
    RT_PT1000_0C360C    = (0x1001, "PT 1000 0C-360C")
    RT_PT100            = (0x1010, "PT 100")

    
class _LCRT4ParamAddress(object):
    VALUE           = 0x1000
    MODE            = 0x1100
    FLAGS           = 0x1101
    SCAN_INTERVAL   = 0x1111
    SETUP_TIME      = 0x1112
    OFFSET          = 0x1120
    CAL_UM          = 0x1130
    CAL_URS         = 0x1131
    


class LucidControlRT4(LucidControl):
    """""LucidControl RTD Input USB Module RT4 class
    """
    
    def getIo(self, channel, value):
        """Get the value or state of a RTD input channel.
            
        This method calls the GetIo function of the module and returns
        the value or of the RTD input channel.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            value: Value object. Must be either ValueTMS4, ValueTMS2 or
                ValueRMU2
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance (channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance (value, (ValueRMU2, ValueTMS2, ValueTMS4)):
            raise TypeError('Expected value as ValueRMU or ValueTM2 or \
                ValueTMS4, got %s' % type(value))
         
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        cmd = Cmd(self.com)
        return cmd.getIo(channel, value)
   
    
    def getIoGroup(self, channels, values):
        """Get the values of a group of RTD input channels.
            
        This method calls the GetIoGroup function of the module and
            returns the values of a group of RTD input channels.
        
        Args:
            channels: Tuple with 4 boolean values (one for each channel).
                A channel is only read if the corresponding channel is
                true.
            values: Value objects
                A tuple with 4 value objects. The value objects must be
                either ValueTMS4, ValueTMS2 or ValueRMU2. The function fills
                the objects with read data.
            
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
            raise TypeError('Expected values as a tuple with 4 value objects, \
                got %s' % type(values))

        if (len(values) < 4):
            raise TypeError('Expected 4 value objects, got %d' % len(values))

        for x in range(4):
            if not isinstance(values[x], (ValueRMU2, ValueTMS2, ValueTMS4)):
                raise TypeError('Expected value as ValueRMU2 or ValueTMS2 or \
                    ValueTMS4, got %s' % type(values[x]))

        cmd = Cmd(self.com)
        return cmd.getIoGroup(channels, values)
    
    
    def calibrateIo(self, channel, persistent, calMode):
        """Calibration of the RTD input channels.
            
        This method calls the CalibIo function of the module which executes
            open and short calibration of the RTD input channels.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store calibration parameter permanently if true
            calMode: Short or open calibration mode as integer (LCRT4CalMode)
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance (channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' %
                type(persistent))
            
        if not isinstance (calMode, int):
            raise TypeError('Expected calMode as int, got %s' % type(calMode))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')

        cmd = Cmd(self.com)
        return cmd.calibrateIo(channel, calMode, persistent)
    
    
    def getParamValue(self, channel, value):
        """Get the Configuration Parameter "Value" of a RTD input channel.
            
        This method calls the GetParam function of the module and returns
            the value of the Configuration Parameter "Value".
        
            The Configuration Parameter "Value" contains the current
            value of the input channel.
        
        It is recommended to call getIo instead of this method.
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            value: Value object of ValueRMU2 class
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """
        if not isinstance (channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))

        if not isinstance(value, ValueRMU2):
            raise TypeError('Expected value as ValueRMU2, got %s' %
                type(value))

        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCRT4ParamAddress.VALUE, channel, data)
        
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            value._setData(data)
        return ret

    
    def getParamMode(self, channel, mode):
        """Get the Configuration Parameter "Mode" of the RTD input channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Mode".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            mode: Operation Mode as a list with one LCRT4Mode integer value
            
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
        ret = cmd.getParam(_LCRT4ParamAddress.MODE, channel, data)

        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            if data[0] == LCRT4Mode.INACTIVE:
                mode[0] = LCRT4Mode.INACTIVE
            elif data[0] == LCRT4Mode.STANDARD:
                mode[0] = LCRT4Mode.STANDARD
            else:
                mode[0] = LCRT4Mode.INACTIVE
        return ret


    def setParamModeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Mode" of a RTD input channel
            to the default value.
            
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
        return cmd.setParamDefault(_LCRT4ParamAddress.MODE, channel, persistent)

    
    def setParamMode(self, channel, persistent, mode):
        """Set the Configuration Parameter "Mode" of a RTD input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Mode".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            mode: Operation Mode as LCRT4Mode integer value
        
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
        return cmd.setParam(_LCRT4ParamAddress.MODE, channel, persistent, data)

    
    def setParamFlagsDefault(self, channel, persistent):
        """Set the Configuration Parameter "Flags" of a RTD input to the
            default value.
            
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
        return cmd.setParamDefault(_LCRT4ParamAddress.FLAGS, channel, persistent)


    def getParamScanInterval(self, channel, scanInterval):
        """Get the Configuration Parameter "Scan Interval" of the RTD input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Scan Interval".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            scanInterval: Scan Interval as a list containing one integer value
                in milliseconds
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """        
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(scanInterval, list):
            raise TypeError('Expected scanInterval as list, got %s' %
                type(scanInterval))
        
        if len(scanInterval) < 1:
            raise TypeError('Expected scanInterval as list with 1 int, got %d' %
                len(scanInterval))
        
        if not isinstance(scanInterval[0], int):
            raise TypeError('Expected scanInterval[0] as int, got %s' %
                type(scanInterval[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCRT4ParamAddress.SCAN_INTERVAL, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            scanInterval[0] = struct.unpack("<H", buffer(data))[0]
        else:
            scanInterval[0] = 0
        return ret


    
    def setParamScanIntervalDefault(self, channel, persistent):
        """Set the Configuration Parameter "Scan Interval" of a RTD input to the
            default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Scan Interval" to the default value.
        
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
        return cmd.setParamDefault(_LCRT4ParamAddress.SCAN_INTERVAL, channel,
            persistent)


    def setParamScanInterval(self, channel, persistent, scanInterval):
        """Set the Configuration Parameter "Scan Interval" of a RTD
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Scan Interval".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            scanInterval: Parameter "Scan Interval" in milliseconds.
                Value range 0 ... 0xFFFF
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or scanInterval value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if not isinstance(scanInterval, int):
            raise TypeError('Expected scanInterval as int, got %s' %
                type(scanInterval))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (scanInterval < 0) | (scanInterval > 0xFFFF):
            raise ValueError('Scan Interval out of range')

        data = bytearray(struct.pack("<H", scanInterval))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCRT4ParamAddress.SCAN_INTERVAL, channel, persistent, data) 
    
 
 
    def getParamSetupTime(self, channel, setupTime):
        """Get the Configuration Parameter "Setup Time" of the RTD input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Setup Time".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            setupTime: Setup Time as a list containing one integer value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """        
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
            
        if not isinstance(setupTime, list):
            raise TypeError('Expected setupTime as list, got %s' %
                type(setupTime))
        
        if len(setupTime) < 1:
            raise TypeError('Expected setupTime as list with 1 int, got %d' %
                len(setupTime))
        
        if not isinstance(setupTime[0], int):
            raise TypeError('Expected setupTime[0] as int, got %s' %
                type(setupTime[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCRT4ParamAddress.SETUP_TIME, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            setupTime[0] = struct.unpack("<H", buffer(data))[0]
        else:
            setupTime[0] = 0
        return ret


    
    def setParamSetupTimeDefault(self, channel, persistent):
        """Set the Configuration Parameter "Setup Time" of a RTD input to the
            default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Setup Time" to the default value.
        
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
        return cmd.setParamDefault(_LCRT4ParamAddress.SETUP_TIME, channel,
            persistent)


    def setParamSetupTime(self, channel, persistent, setupTime):
        """Set the Configuration Parameter "Setup Time" of a RTD
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Setup Time".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            setupTime: Parameter "Setup Time" in milliseconds.
                Value range 0 ... 0xFFFF
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or setupTime value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if not isinstance(setupTime, int):
            raise TypeError('Expected setupTime as int, got %s' %
                type(setupTime))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (setupTime < 0) | (setupTime > 0xFFFF):
            raise ValueError('Setup Time out of range')

        data = bytearray(struct.pack("<H", setupTime))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCRT4ParamAddress.SETUP_TIME, channel, persistent, data) 
 
 
    def getParamOffset(self, channel, offset):
        """Get the Configuration Parameter "Offset" of the RTD input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "Offset".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            offset: Offset as a list containing one integer value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """        
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
            
        if not isinstance(offset, list):
            raise TypeError('Expected offset as list, got %s' %
                type(offset))
        
        if len(offset) < 1:
            raise TypeError('Expected offset as list with 1 int, got %d' %
                len(offset))
        
        if not isinstance(offset[0], int):
            raise TypeError('Expected offset[0] as int, got %s' %
                type(offset[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCRT4ParamAddress.OFFSET, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            offset[0] = struct.unpack("<h", buffer(data))[0]
        else:
            offset[0] = 0
        return ret

    
    def setParamOffsetDefault(self, channel, persistent):
        """Set the Configuration Parameter "Offset" of a RTD input to the
            default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "Offset" to the default value.
        
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
        return cmd.setParamDefault(_LCRT4ParamAddress.OFFSET, channel, persistent)
    
    
    def setParamOffset(self, channel, persistent, offset):
        """Set the Configuration Parameter "Offset" of a RTD
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "Offset".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            offset: Parameter "Offset" 
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or offset value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if not isinstance(offset, int):
            raise TypeError('Expected offset as int, got %s' %
                type(offset))
        
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')
        
        if (offset < (-pow(2, 15))) | (offset >= pow(2, 16)):
            raise ValueError('Offset out of range')

        data = bytearray(struct.pack("<h", offset))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCRT4ParamAddress.OFFSET, channel, persistent,
            data) 
 
    
    def getParamCalUm(self, channel, calUm):
        """Get the Configuration Parameter "CalUm" of the RTD input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "CalUm".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            calUm: Calibration value UM as a list containing one integer value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """        
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
            
        if not isinstance(calUm, list):
            raise TypeError('Expected calUm as list, got %s' %
                type(calUm))
        
        if len(calUm) < 1:
            raise TypeError('Expected calUm as list with 1 int, got %d' %
                len(calUm))
        
        if not isinstance(calUm[0], int):
            raise TypeError('Expected calUm[0] as int, got %s' %
                type(calUm[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCRT4ParamAddress.CAL_UM, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            calUm[0] = struct.unpack("<H", buffer(data))[0]
        else:
            calUm[0] = 0
        return ret


    def setParamCalUmDefault(self, channel, persistent):
        """Set the Configuration Parameter "CalUm" of a RTD input to the
            default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "CalUm" to the default value.
        
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
        return cmd.setParamDefault(_LCRT4ParamAddress.CAL_UM, channel, persistent)

    
    def setParamCalUm(self, channel, persistent, calUm):
        """Set the Configuration Parameter "CalUm" of a RTD
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "CalUm".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            calUm: Calibration Parameter "CalUm" 
                    
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or calUm value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if not isinstance(calUm, int):
            raise TypeError('Expected calUm as int, got %s' %
                type(calUm))
        
        if (calUm < 0) | (calUm >= (pow(2, 16))):
            raise ValueError('CalUm out of range')
        
        data = bytearray(struct.pack("<H", calUm))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCRT4ParamAddress.CAL_UM, channel, persistent,
            data) 
 
    
    def getParamCalUrs(self, channel, calUrs):
        """Get the Configuration Parameter "CalUrs" of the RTD input
            channel.
            
        This method calls the GetParam function of the module and returns
            the Configuration Parameter "CalUrs".
          
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            calUrs: Calibration value URS as a list containing one integer value
            
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel value is out of range
        """        
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
            
        if not isinstance(calUrs, list):
            raise TypeError('Expected calUrs as list, got %s' %
                type(calUrs))
        
        if len(calUrs) < 1:
            raise TypeError('Expected calUrs as list with 1 int, got %d' %
                len(calUrs))
        
        if not isinstance(calUrs[0], int):
            raise TypeError('Expected calUrs[0] as int, got %s' %
                type(calUrs[0]))
            
        if (channel >= self.nrOfChannels):
            raise ValueError('Channel out of range')     
        
        data = bytearray()
        cmd = Cmd(self.com)
        ret = cmd.getParam(_LCRT4ParamAddress.CAL_URS, channel, data)
    
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            calUrs[0] = struct.unpack("<h", buffer(data))[0]
        else:
            calUrs[0] = 0
        return ret


    def setParamCalUrsDefault(self, channel, persistent):
        """Set the Configuration Parameter "CalUrs" of a RTD input to the
            default value.
            
        This method calls the SetParam function of the module and sets
        the Configuration Parameter "CalUrs" to the default value.
        
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
        return cmd.setParamDefault(_LCRT4ParamAddress.CAL_URS, channel, persistent)

    
    def setParamCalUrs(self, channel, persistent, calUrs):
        """Set the Configuration Parameter "calUrs" of a RTD
            input channel.
            
        This method calls the SetParam function of the module and sets the
        Configuration Parameter "calUrs".
        
        Args:
            channel: IO channel number. Must be in the range 0 ... 3
            persistent: Store parameter permanently if true
            calUrs: Calibration Parameter "calUrs" 
        
        Returns:
            IO_RETURN_OK in case of success, otherwise detailed IoReturn
            error code.
        
        Raises:
            TypeError: Passed argument types are wrong
            ValueError: Channel or scanInterval value is out of range
        """
        if not isinstance(channel, int):
            raise TypeError('Expected channel as int, got %s' % type(channel))
        
        if not isinstance(persistent, bool):
            raise TypeError('Expected persistent as bool, got %s' % 
                type(persistent))
        
        if not isinstance(calUrs, int):
            raise TypeError('Expected calUrs as int, got %s' %
                type(calUrs))
        
        if (calUrs < (-pow(2, 15))) | (calUrs >= pow(2, 16)):
            raise ValueError('CalUrs out of range')
        
        data = bytearray(struct.pack("<h", calUrs))
        cmd = Cmd(self.com)
        return cmd.setParam(_LCRT4ParamAddress.CAL_URS, channel, persistent,
            data) 
    
    
    def getDeviceTypeName(self):
        """Get device type name as string.
        
        Returns:
            String of the device type name
        
        Raises:
            ValueError: ID data not valid
        """
        if self.id.validData == True:
            if (self.id.deviceType == LCRT4DeviceType.RT_PT100[0]):
                return LCRT4DeviceType.RT_PT100[1]
            elif (self.id.deviceType == LCRT4DeviceType.RT_PT1000[0]):
                return LCRT4DeviceType.RT_PT1000[1]
            elif (self.id.deviceType == LCRT4DeviceType.RT_PT1000_0C360C[0]):
                return LCRT4DeviceType.RT_PT1000_0C360C[1]
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
            return LCRT4DeviceType.RT_NONE


    def __init__(self, portName):
        """
        Constructor of LucidControl RTD Input USB Module class
        """
        LucidControl.__init__(self, portName)
        self.nrOfChannels = 4
        
