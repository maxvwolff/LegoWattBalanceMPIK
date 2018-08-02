from mcculw import ul
from mcculw.enums import ULRange, InfoType, BoardInfo, DigitalInfo, DigitalPortType, DigitalIODirection, FunctionType
from mcculw.ul import ULError

import sys
sys.path.insert(0, 'LucidIO')

from LucidControlAO4 import LucidControlAO4
from Values import ValueVOS4
import IoReturn

class Hardware(object):
    def __init__(self):
        # LucidIO
        self.ao4 = LucidControlAO4('COM16')

        # Open AO4 port
        if (self.ao4.open() == False):
            self.ao4.close()
            exit()

        ret = self.ao4.identify(0)
        if ret == IoReturn.IoReturn.IO_RETURN_OK:
            pass
        else:
            print ('Error while initializing LucidIO')
            self.ao4.close()
            exit()

        '''
        # MCC
        board_num = 0
        channel = 0
        ai_range = ULRange.BIP5VOLTS

        try:
            # Get a value from the device
            value = ul.a_in(board_num, channel, ai_range)
            # Convert the raw value to engineering units
            eng_units_value = ul.to_eng_units(board_num, ai_range, value)

            # Display the raw value
            print("Raw Value: " + str(value))
            # Display the engineering value
            print("Engineering Value: " + '{:.3f}'.format(eng_units_value))
        except ULError as e:
            # Display the error
            print("A UL error occurred. Code: " + str(e.errorcode)
                  + " Message: " + e.message)
        '''

    def setOutput(self, voltage):
        # Create a value object for value type VOS4
        # 4 bytes signed value
        value = ValueVOS4()
        
        value.setVoltage(voltage)

        # Write value to channel 0
        ret = self.ao4.setIo(0, value)

        # Check return value for success
        if (ret != IoReturn.IoReturn.IO_RETURN_OK):
            print ('Error setting CH0 voltage')
            self.ao4.close()
            return False

        return True

    def readChannel(self, ch):
        ai_range = ULRange.BIP5VOLTS
        value = ul.a_in(0, ch, ai_range)
        dec_value = ul.to_eng_units(0, ai_range, value)
        return dec_value * 2

    def readShuntVoltage(self):
        ai_range = ULRange.BIP1PT67VOLTS
        value = ul.a_in(0, 1, ai_range)
        dec_value = ul.to_eng_units(0, ai_range, value)
        return dec_value * 5.988

    def readFotodiode(self):
        ai_range = ULRange.BIPPT05VOLTS
        value = ul.a_in(0, 3, ai_range)
        dec_value = ul.to_eng_units(0, ai_range, value)
        return dec_value * 200

    def readInductionVoltage(self):
        ai_range = ULRange.BIPPT156VOLTS
        value = ul.a_in(0, 2, ai_range)
        dec_value = ul.to_eng_units(0, ai_range, value)
        return dec_value * 64.103

    def switchRelay(self, state):
        ul.d_config_port(0, 1, DigitalIODirection.OUT)
        if state == False:
            ul.d_out(0, 1, 0)
        else:
            ul.d_out(0, 1, 0x01)

