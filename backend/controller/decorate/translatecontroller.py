import requests,urllib

class translateController:
    def __init__(self,text,sourcela,targetla):
        self.text       =text
        self.sourcela   =sourcela
        self.targetla   =targetla
        self.url        ='https://script.google.com/macros/s/AKfycbz4kKcAHxHsNMHXdTXTF3cAdZQbHXBNXWCqJxWTpQ/exec?text={0}&source={1}&target={2}'.format(self.text,self.sourcela,self.targetla)

    def gettranslatecontent(self):
        content         =requests.get(self.url,timeout=10)
        return content.json()['text']