class DefectAnalysis:

    # Усредняет значение по каждому из массивов (Когда массивов с данными по колесу > 1)
    @classmethod
    def getMiddle(cls, args: list[list[int]]) -> list[int]:

        resultList: list[int] = []
        iterator: int = 0 
        while (iterator <= len(args) -1):

            accumuletor: int = 0
            for i in args[iterator]:
                accumuletor += i

            resultList.append(accumuletor/len(args[iterator]))
            iterator+= 1  

        return resultList

    # Оценка трендов (Данная ф-ция позволяет определить наличие изъяна "Выщерблена" на колесе состава)
    @classmethod
    def trendAssessment(cls, middleRes: list[int]) -> list[int]:
        result: list[int] = [0 if middleRes[i]<middleRes[i+1] else 1 for i in range(len(middleRes)-1)]
        return result
    
    def __init__(self, signalArguments: list[list[int]]) -> None:
        self.__signalArguments = DefectAnalysis.trendAssessment(DefectAnalysis.getMiddle(signalArguments))

    # Анализ подготовленных данных на наличие дефектов 
    def defectDetection(self) -> str:

        counter: int = 0
        while(counter < len(self.__signalArguments)):
            if(self.__signalArguments[counter] == 1):
                break
            counter += 1

        result: str = "Wheel has no defects"

        for element in range(counter, len(self.__signalArguments)):
            if(self.__signalArguments[element] == 0):
                result = "Wheel has a defect"
                break

        return result

