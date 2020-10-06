from matplotlib.pyplot import xlabel
import matplotlib.pyplot as plt
from kabu_beta.settings import base

class graphController:
    def __init__(self,title,xlabel,ylabel):
        plt.title(title,fontname=base.BASE_DIR +"/Font/Osaka.ttc")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)