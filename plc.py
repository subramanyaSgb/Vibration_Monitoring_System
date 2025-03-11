import minimalmodbus
import serial
import time
from icecream import ic
ic.disable()
class PLC():
    """
    Class representing the connection and communication with a Programmable Logic Controller (PLC).

    Attributes:
    - isPLCConnected (bool): Indicates whether the connection to the PLC is established.
    - door_open (int): PLC address for door open status (x0).
    - slab_status (int): PLC address for slab movement status (x1).
    - roller_status (int): PLC address for roller movement status (x2).

    Methods:
    - __init__(): Initializes the PLC object and attempts to connect to the PLC using the connectToPLC() method.
    - connectToPLC(): Connects to the PLC using minimalmodbus library with specified parameters.
    - read_bit(address): Reads the value of a specified address in the PLC.

    """
    def __init__(self):
        """
        Initializes the PLC object and attempts to connect to the PLC using the connectToPLC() method.
        """
        self.isPLCConnectecd = False
        self.connectToPLC()


    def convert_ma_to_percentage(self, ma):
        # Define the input range
        input_min = -12
        input_max = 20
        
        # Define the output range
        output_min = 0
        output_max = 100
        
        # Check if the input is within the expected range
        if ma < input_min or ma > input_max:
            raise ValueError(f"Input value {ma} mA is out of range. Must be between {input_min} and {input_max} mA.")
        
        # Perform the conversion
        output = ((ma - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min
        return output

    def connectToPLC(self):
        """
        Connects to the PLC using minimalmodbus library with specified parameters.

        Raises:
        - SerialException: If a SerialException occurs during connection, the function attempts to close the serial port and reconnect.
        - Exception: For any other unexpected errors during connection, the function attempts to close the serial port and reconnect.

        """
        try:
            self.instrument = minimalmodbus.Instrument('COM7', 1, minimalmodbus.MODE_ASCII) #, debug = True) ## check com port in your system for me its "COM6"
            self.instrument.serial.port                                     # this is the serial port name
            self.instrument.serial.baudrate = 9600                          # Baudrate
            self.instrument.serial.bytesize = 7
            self.instrument.serial.parity   = serial.PARITY_EVEN
            self.instrument.serial.stopbits = serial.STOPBITS_ONE
            self.instrument.serial.timeout  = 2.0                           # seconds
            self.instrument.address                                         # this is the slave address number
            self.instrument.mode = minimalmodbus.MODE_ASCII               # rtu or ascii mode
            self.instrument.clear_buffers_before_each_transaction = True

            print("parameter setting: ",self.instrument)

            self.isPLCConnectecd = True

        except serial.serialutil.SerialException:
            print("Coud Not Connect to PLC")
            try:
                self.instrument.serial.close()
                print("3 connect To PLC Called")
                self.connectToPLC()
            except Exception as e:
                print("Connect to PLC Error:- {}".format(e))
                self.isPLCConnectecd = False
                
        except Exception as e:
            print("Connect to PLC Error:- {}".format(e))
            try:
                self.instrument.serial.close()
                print("4 connect To PLC Called")
                self.connectToPLC()
            except Exception as e:
                print("Connect to PLC Error:- {}".format(e))
                self.isPLCConnectecd = False


    def read_bit(self,adress):
        try:
            val = self.instrument.read_register(adress)
            # if adress == 4196 or adress == 4296:
            #     val = self.convert_ma_to_percentage(val)
            
            print(f"The Value in {adress} is : {val}")
            
            return val
        except minimalmodbus.NoResponseError:
            try:
                print("1 connect To PLC Called")
                self.instrument.serial.close()
                self.connectToPLC()
            except:
                self.isPLCConnectecd = False
        except:
            self.isPLCConnectecd = False
            return "PLC Not Connected"
    
    def write_bit(self,adress,data):
        try:
            ic(adress,data)
            self.instrument.write_register(adress,data)
        except minimalmodbus.NoResponseError:
            try:
                print("[INFO] 1 connect To PLC Called")
                self.instrument.serial.close()
                self.connectToPLC()
            except:
                self.isPLCConnectecd = False
        except:
            self.isPLCConnectecd = False
        return True
    
    
if __name__ == "__main__":

    plc = PLC()
    while True:
        DI1 = 4106
        # DI2 = 4107
        # DI3 = 4108
        # DI4 = 4109
        # DI5 = 4110
        # DI6 = 4111
        # DI7 = 4112
        # DI8 = 4113
        # DI9 = 4116
        # DI10 = 4115
        # DI11 = 4116
        # DI12 = 4117
        # DI13 = 4118
        # DI14 = 4119
        # DI15 = 4120
        # DI16 = 4121
        # DI17 = 4122
        # DI18 = 4123
        # DI19 = 4196
        # DI20 = 4296

        # print(plc.read_bit(DI2))
        # print(plc.read_bit(DI1))
        # print(plc.read_bit(DI3))
        # print(plc.read_bit(DI4))
        ic(f"D10 : {plc.read_bit(DI1)}")
        plc.write_bit(DI1, 100) # To on Y0
        time.sleep(5)
        plc.write_bit(DI1, 200) # To off Y0
        time.sleep(5)
        
        ic("-------------------")
       