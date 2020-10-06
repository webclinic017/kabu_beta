from backend.model.company import COMPANY
import re

class ConpanyStrategy:

    def getResult(self,words):
        result =[]
        tempgroup=re.findall(r'\<\d+.T\>', words)

        if tempgroup is not None:
            for temp in tempgroup:
                result.append(temp[1:5])

        return result;