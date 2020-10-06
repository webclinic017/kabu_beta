
from django.http.response import HttpResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.db import connection
# from IPython.display import Image

class CorrelationController:

    def showcorrelation(request):
        cursor              = connection.cursor()
        cursor.execute("""
           SELECT
            tag.tag_name,fr_com.company_name
            FROM
            backend_company company
            left join backend_news_company news_com on news_com.company_id=company.code
            left join backend_news news
            on news.news_id=news_com.news_id
            left join backend_news_tag news_tag on news_tag.news_id= news_com.news_id
            left join backend_tag tag on tag.tag_id=news_tag.tag_id
            left join front_company fr_com on fr_com.company_code=company.code
            order by company.code
        """)
        results = cursor.fetchall()
        comlist=[]
        for temp in results:
            com={}
            com['tag_name']=temp[0]
            com['company_name']=temp[0]
            comlist.append(com)
#         print(comlist)
        tips=pd.DataFrame.from_dict(comlist)
        tips.corr()
        sns.pairplot(tips,size=2.0)
        sns_plot.savefig("pairplot.png")
#         Image(filename='pairplot.png')
        return HttpResponse('success')