from backend.model.label import LABEL
from django.db import connection
from plotly.graph_objs import Scatter
import numpy as np
from plotly.offline import plot
from django.shortcuts import render

class labelnews:
      #x    date
     #y    news_count
    def showNewsAggregateVialabel(request,label_id):
        label_news               =labelnews()
        labellist               = LABEL.objects.filter(label_id=label_id)
        final_result            = label_news.showNewsLabel(label_id)
        x = np.array(final_result["x"])
        y = np.array(final_result["y"])

        plot_div = plot([
                        Scatter(x=x, y=y,
                                mode='lines',
                                name=labellist[0].label_name,
                                opacity=0.8,
                                marker_color='green')
                        ],
               output_type='div')
        context={
                'plot_div': plot_div,
                'label_name':labellist[0].label_name,
                }
        return render(request, "labelnews/index.html",context)

    def showNewsLabel(self,label_id):
        cursor              = connection.cursor()
        results             =cursor.execute("""
           SELECT
           count(backend_news.news_id) count,
           create_date,
           label_id
           FROM backend_news
           WHERE LABEL_id={0}
            GROUP BY create_date
        """.format(label_id))
        final_result={}
        final_result["x"] =[]
        final_result["y"] =[]
        for temp in results:
                final_result["x"].append(temp[1])
                final_result["y"].append(temp[0])
        return final_result

