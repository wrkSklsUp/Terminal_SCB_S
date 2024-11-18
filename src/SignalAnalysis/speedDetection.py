# Ф-ция позволяет определить текущую скорость состава
def speedDetect(wheelData: list[list[int]]) -> int:

    ACTIVE_SENSOR_AREA = 1000 / 421 # Количество участков дистанции учета прохождения колеса над датчиком на 1 метр
    ONE_HOUR_SCONDS = 3600 # Количество секунд в 1-ном часе

    mSecCount = (len(wheelData) * len(wheelData[0])) * ACTIVE_SENSOR_AREA
    return round(ONE_HOUR_SCONDS / mSecCount) # Возвращаемое значение соответствует скорости км/ч
