import minimalmodbus
from typing import Union

class PollMbsSlave:
  
    @classmethod
    def mbsPortInit(cls,
            portName: str, 
            slvAddress: int, 
            baudrate: int, 
            bytesize: int, 
            parityBit: str, 
            countStopBits: int, 
            timeout: int
        ) -> minimalmodbus.Instrument:
        
        # absolute file path to the file that represents the ModbusRTU port,
        # slvAddress int value represents adrdress ModbusRTU Slave 

        instrument = minimalmodbus.Instrument(portName, slvAddress)

        instrument.serial.baudrate = baudrate              # Speed Send/Recive
        instrument.serial.bytesize = bytesize              # count bit in one "Word"
        instrument.serial.parity   = parityBit             # 1 Without paruty byt
        instrument.serial.stopbits = countStopBits         # 1 Stop Bit
        instrument.serial.timeout  = timeout               # Установка между запросами 20 мСек


        return instrument
    
    
    def __init__(self, portName, slvAddress, baudrate, bytesize, parityBit, countStopBits, timeout):
        self.__slaveAddress = slvAddress
        self.__portName = portName,
        self.__mbsPort: minimalmodbus.Instrument = PollMbsSlave.mbsPortInit(
            portName, 
            slvAddress, 
            baudrate, 
            bytesize, 
            parityBit, 
            countStopBits, 
            timeout
        )

    def readMbsPortInfo(self):
        print("Baudrate: "+ str(self.__mbsPort.serial.baudrate) + "\n"+ "Port: " + 
              str(self.__portName) + "\n" + "Slave Addr. :" + str(self.__slaveAddress))
    
    def readDiscreteInput(self, addressReg: int, functionCode: int) -> int:
        return self.__mbsPort.read_bit(addressReg, functionCode)


    def readingAnalogInput(self, firstRegister: int, countRegisters: int, functionCode: int) -> Union[list[int], str]:
        return self.__mbsPort.read_registers(firstRegister, countRegisters, functionCode)


