import matplotlib.pyplot as plt
from front.decorate.graphcontroller import graphController
import io
import urllib, base64

class lineGraphController(graphController):
    def __init__(self,title,xlabel,ylabel):
        super().__init__(title,xlabel,ylabel)

    def getBase64LineChart(self,x,y):
        plt.plot(x, y)

#         plt.imshow(wc, interpolation='bilinear')
#         plt.show()
#         plt.axis("off")

        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image.close()
        plt.close()
        return string
