from SignalAnalysis.parasiticVibrationFilter import *
from ModbusRTU.PollMbsSlave import *
from workers.jsonWorker import *
from SignalAnalysis.defectAnalysis import DefectAnalysis
from SignalAnalysis.speedDetection import speedDetect
from SignalAnalysis.timeToNextCarriage import timePassageNextCarriage

import serial
from datetime import datetime
from termcolor import colored

def startProgram(
    file_name,
    sensorPoint,
    firstRegisterAddress, 
    countAnalogRegisters, 
    mbsSlave, 
    sygnalDataArr, 
    startWheel, 
    resetCarriageCounter, 
    oneCarriageWheelCounter, 
    carriageCounter, 
    logeJSONArr):

    timeToNextCarriage: float = 0.0
    timeCounter: int = 0


# Опрос Датчика для получения информации о занятости пути
    while(True):
        
        # Опрос Slave
        try:
            sygnalData: list[int] = mbsSlave.readingAnalogInput(firstRegisterAddress, countAnalogRegisters, 4)
        except Exception:
            print(colored("!!! The device is not responding. Check the connection or the Slave name is correct !!!!\n", "red", attrs=["bold"]))
            break

        # Установка переменной индикатора для Обнуления Счетчик вагонов
        if(str(datetime.now().time()).split(".")[0] == "09:39:00"): resetCarriageCounter = 1 #
        

        # Проверка: Если в массиве нет значений больше 1-ци (Паразитное значение преобразования), то такой массив не проходит
        status: int = parasiticConversionChecker(sygnalData)

# Условие характеризующее момент прохода вагона (Путь занят)!
        if(status >= 1): 

            startWheel = 1  
            sygnalDataArr.append(sygnalData)

# Условие характеризующее момент времени когда вагон только, что прошел (Путь только что был занят)!
        elif(status < 1 and startWheel == 1):

            timeCounter = 0
            timeToNextCarriage = timePassageNextCarriage(sygnalDataArr)

            startWheel = 0
            oneCarriageWheelCounter += 1 

            WHEELS_ON_ONE_CARRIAGE = 5 # Количество колес в 1-ном вагоне
            
            # Момент времени когда заключительное колесо вагона прошло над датчиком
            if(oneCarriageWheelCounter == WHEELS_ON_ONE_CARRIAGE):

                # Обнуление Счетчик вагонов
                if(resetCarriageCounter == 1):
                    carriageCounter = 1
                    oneCarriageWheelCounter = 1
                    resetCarriageCounter = 0

                else: 
                    oneCarriageWheelCounter = 1
                    carriageCounter += 1

            # Определение дефектов колеса 
            resultDef: str = DefectAnalysis(sygnalDataArr).defectDetection()

            # Определение скорости состава
            speed: str = str(speedDetect(sygnalDataArr)) + " k/h"

            date: str = str(datetime.now()).split(".")[0]

            # Формирование итоговой информации по проходящему вагону
            to_json: dict = {
                'Place': sensorPoint, 
                'Date':date, 
                'Defect': resultDef,
                'Wheel': oneCarriageWheelCounter,
                'Carriage': carriageCounter,
                'Speed': speed
            }
            
            finalOut: str = f'Place: {to_json.get('Place')}\nDate: {to_json.get('Date')}\nDefect: {to_json.get('Defect')}\nWheel: {to_json.get('Wheel')}\nCarriage: {to_json.get('Carriage')}\nSpeed: {to_json.get('Speed')}\n-------------------------------\n'
            print(colored(finalOut, 'white', attrs=["bold"]))

            # logeJSONArr.append(to_json)  #MAIN ACTION!!!

            # logeJSONArr.append(to_json_2) # TEST VARIANT

            # Сохранение итоговой информации по проходящему вагону в файл
            # try:
            #     jsonWriter(logeJSONArr, file_name)
            
            # except Exception:
            #     print(colored("!!! Error: The log file at the specified path cannot be created. Check that the file path is correct and restart the terminal !!!\n", "red", attrs=["bold"]))
                
            
            # Очистка массива перед проходом следующего колеса
            sygnalDataArr.clear()

# Условие характеризующее момент времени когда Вагон не идет (Путь свободен)!
        elif(status<1):

            if(timeCounter > 0 and timeCounter == timeToNextCarriage): 
                print(colored(f"** No train movement on the line: {sensorPoint} **\n", "green", attrs=["bold"]))

                timeCounter = 0
                timeToNextCarriage = 0

            if(timeToNextCarriage > 0):
                timeCounter += 1


def main():

    print(colored("\n<< Terminal for System of Control Passing Train. v 1.0.0 >>\n", 'white', attrs=["bold"]))


    # Настройки порта USB/RS-485
    BAUDRATE = 115200                       
    COUNT_BITS = 8                          
    PARITY_BIT = serial.PARITY_NONE         
    STOP_BIT = 1                            
    TIMEOUT = 0.20                          


    #               Для Консольного приложения (Linux)   
    fileName = input("** Enter Some name for log file with absolute path. (EXAMPLE: /home/UserName/TestLog) -> ")
    portPath = input("** Enter Absolute path to USB/RS-485 port. (EXAMPLE: /dev/ttyUSB0) -> ")                           
    addressSlave = input("** Enter Slave ModbusRTU Address. (EXAMPLE: 5) -> ")                                     
    sensorPoint = input("** Enter the name of the controlled path. (EXAMPLE: (1361 kilometers) Tekhnikum station) -> ")
    print("\n")
    
    try:
        mbsSlave = PollMbsSlave(str(portPath), int(addressSlave), BAUDRATE, COUNT_BITS, PARITY_BIT, STOP_BIT, TIMEOUT)
    except Exception:
        print(colored("!!! Error: Make sure the port name you enter is correct for USB/RS-485 and the address you enter for the Slave device is correct !!!\n", "red", attrs=["bold"]))
        raise SystemExit(1)

    firstRegisterAddress: int = 0
    countAnalogRegisters: int = 20
    sygnalDataArr: list[int] = [] # Нужно только для определения изъяна, и определения скорости
    startWheel: int = 0 # Метка прохода колеса над датчиком, как только колесо прошло метка устанавливается в 1-цу
    resetCarriageCounter: int = 0 # Метка указывающая, что значение переменной Счетчик вагонов должно быть Обнулено
    oneCarriageWheelCounter: int = 0 # Счетчик количества колес 1-го вагона
    carriageCounter: int = 1 # Счетчик вагонов
    logeJSONArr: list[dict] = [] # Временный массив фиксации проходящего состава

    print(colored(f"************ Started listening '{str(sensorPoint)}' path... ************\n", 'white', attrs=["bold"]))

    # Данный подход Обеспечивает постоянную работу программы т.к. программа опрашивает Slave до тех пор
    # пока тот не ответит
    while(True): 

        startProgram(
        str(fileName)+'.json',
        str(sensorPoint),
        firstRegisterAddress, 
        countAnalogRegisters, 
        mbsSlave, 
        sygnalDataArr, 
        startWheel,
        resetCarriageCounter, 
        oneCarriageWheelCounter, 
        carriageCounter, 
        logeJSONArr) 

    
if __name__ == '__main__':
    main()