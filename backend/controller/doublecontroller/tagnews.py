from backend.model.news import NEWS
from backend.model.tag import TAG
from django.shortcuts import render
from plotly.offline import plot
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from django.db import connection
import numpy as np
from plotly.graph_objs import Scatter
from backend.controller.decorate.wordcloud import wordCloud


class tagnews:
        #show tag detail
    def showtagnews(request,tag_id):
        tag                =TAG.objects.filter(tag_id=tag_id)
        newslist           = NEWS.objects.filter(tag=tag_id)

        infotxt             =''
        for news in newslist:
            infotxt+=news.detail+news.title

        wordcloudobj    =wordCloud()
        wc_img          =wordcloudobj.word_cloud(infotxt)

        context ={
            'infolist'        :newslist,
            'tagname'         :tag[0].tag_name if(tag.count()>0) else '',
            'wc_img'          :wc_img

        }
        return render(request, 'tag_news.html', context)

    #x    date
    #y    news_count
    def showNewsAggregateViatag(request,tag_id):
        tag                 =TAG.objects.filter(tag_id=tag_id)
        cursor              = connection.cursor()
        cursor.execute("""
           SELECT count(backend_news.news_id) count,create_date FROM backend_news
           left join backend_news_tag on backend_news_tag.news_id = backend_news.news_id
           where backend_news_tag.tag_id ={0} GROUP BY create_date
        """.format(tag_id))
        final_result={}
        final_result["x"] =[]
        final_result["y"] =[]

        results = cursor.fetchall()

        for temp in results:
                print(temp[1])
                final_result["x"].append(temp[1])
                final_result["y"].append(temp[0])

        x = np.array(final_result["x"])
        y = np.array(final_result["y"])
        plot_div = plot([
                        Scatter(x=x, y=y,
                                mode='lines',
                                name=tag[0].tag_name,
                                opacity=0.8,
                                marker_color='green')],
               output_type='div')
        context={
                'plot_div': plot_div,
                'tag_name':tag[0].tag_name,
                }
        return render(request, "newstag/index.html",context)

