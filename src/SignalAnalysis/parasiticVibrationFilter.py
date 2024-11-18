# Функция позволяет отсеять паразитные преобразования
def parasiticConversionChecker(array: list[int]) -> int:
   
    PARASITIC_CONVERSION_VALUE = 10 # 50 Значение которое может быть полученно в результате паразитного преобразования (Установленно опытным путем)

    oneMoreCounter: int = 0
    for arg in array:
        if(arg > PARASITIC_CONVERSION_VALUE): 
            oneMoreCounter += 1
            break
    return oneMoreCounter