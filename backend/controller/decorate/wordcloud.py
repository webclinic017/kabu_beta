import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
import matplotlib
from kabu_beta.settings import base
from janome.tokenizer import Tokenizer
from backend.model.wordmask import wordMask


class wordCloud:
    def word_cloud(self,text):
        string  = self.word_cloudbase64(text)
        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        return image_64
    #word_cloudのbase64
    def word_cloudbase64(self,text):
        if len(text)==0 :
            return
        obj         =wordCloud()
        text        =obj.clearsentenses(text)
        matplotlib.use('Agg')

        wc = WordCloud(font_path=base.BASE_DIR +"/Font/Osaka.ttc",background_color = 'white').generate(text)
        plt.imshow(wc, interpolation='bilinear')
        plt.show()
        plt.axis("off")

        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image.close()
        plt.close()
        return string

    #test
    def generatewordCloud(request):

        obj         =wordCloud()
        text        ="test,text,test"
        wordcloud   = obj.word_cloud(text)
        args        ={"image":wordcloud}
        return render(request, 'wordcloudgen/cloud_gen.html', args)

    def clearsentenses(self,text):
        if len(text)==0:
            return
        tokenizer   = Tokenizer()
        result      =""
        for token in tokenizer.tokenize(text):
            if "名詞" in token.part_of_speech:
                if wordMask.objects.filter(word=token.surface).count() == 0:
                    result+=" "+token.surface

        return result





