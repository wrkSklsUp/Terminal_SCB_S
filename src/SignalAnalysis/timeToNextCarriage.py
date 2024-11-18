# Функция определения время через которое должен пройти потенциальный следующий вагон
def timePassageNextCarriage(sygnalDataArr: list[list[int]]) -> int:
    SENSOR_ACTIVE_ZONE = 421                              # Протяженность зоны фикцасии магнито-индукц. датчиком проход. колеса 
    CARRIAGE_LENGTH = 19210                               # Длинна вагона
    FIXING_ARIES = (CARRIAGE_LENGTH / SENSOR_ACTIVE_ZONE) # Потенциально фиксируемя область
    ADC_TIME = 20  # 10 На новом устве при скорости 0.5   # Время выполнения преобразования АЦП для получ. 1-го массива 20 знач.
    TIME_DEVISION = 10
    return round((len(sygnalDataArr * ADC_TIME) * FIXING_ARIES)/TIME_DEVISION) # мСек
