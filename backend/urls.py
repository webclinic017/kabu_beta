from django.conf.urls import  url
from backend.controller.tradersnewsscrapy import Trade
from backend.controller.showjpinfo import showjpinfo
from backend.controller.simplecontroller.tagcontroller import tagcontroller
from backend.controller.simplecontroller.tagkubuncontroller import tagkubuncontroller
from backend.controller.simplecontroller.labelcontroller import labelcontroller
from backend.controller.simplecontroller.companycontroller import companycontroller
from backend.controller.simplecontroller.newscontroller import newscontroller
from backend.controller.simplecontroller.correlationcontroller import CorrelationController
from backend.controller.simplecontroller.eventcontroller import eventcontroller
from backend.controller.weiboinfoflow import weiboInfoFlow

from backend.controller.decorate.wordcloud import wordCloud

from backend.controller.doublecontroller.companynews import companynews
from backend.controller.doublecontroller.labelnews import labelnews
from backend.controller.doublecontroller.tagnews import tagnews
from backend.controller.doublecontroller.companytag import companyTag

urlpatterns = [
    url('getjpkabuinfo',Trade.getjapaninfo,name='getjpkabuinfo'),
    #news
    url('showweeknewsinfo/',newscontroller.getWeekNews,name='showweeknewsinfo'),
    url('showmonthnewsinfo/',newscontroller.getMonthNews,name='showmonthnewsinfo'),
    url('showsearchnews/',newscontroller.searchnews,name='searchnews'),
    url(r'^showdetail/(?P<newsid>[0-9]+)/$',newscontroller.shownewsdetail,name='showdetail'),
    #tag
    url(r'^addtag/$',tagcontroller.add,name='addtag'),
    url(r'^removetag/$',tagcontroller.removetag,name='removetag'),
    url(r'^showtaglist',tagcontroller.showtaglist,name='showtaglist'),
    url(r'^showtaginfo/(?P<tag_id>[0-9]+)/$',tagcontroller.showtaginfo,name='showtaginfo'),
    url(r'^updatetaginfo/$',tagcontroller.updatetaginfo,name='updatetaginfo'),
    #label
    url(r'^addlabel/$',labelcontroller.add,name='addlabel'),
    url(r'^showLabellist',labelcontroller.showLabellist,name='showLabellist'),
    #tagkubun
    url(r'^addkubuninfo/$',tagkubuncontroller.add,name='addkubuninfo'),
    url(r'^showtagkubunlist',tagkubuncontroller.showtagkubunlist,name='showtagkubunlist'),
    #company
    url(r'^showcompanylist/$',companycontroller.showcompanylist,name='showcompanylist'),
    url(r'^addnewcompany/$',companycontroller.addNewCompany,name='addNewCompany'),
    #event
    url(r'^addevent/$',eventcontroller.add,name='addevent'),
    url(r'^showeventlist/$',eventcontroller.showeventlist,name='showeventlist'),

    url('showjpinfo',showjpinfo.list,name='getjpkabuinfo'),
    url(r'^check/(?P<newsid>[0-9]+)$',showjpinfo.check,name='check'),


    url(r'^addcompany/$',companynews.add,name='addcompany'),
    url(r'^removecompany/$',companynews.removecompany,name='removecompany'),

    url(r'^showtagnews/(?P<tag_id>[0-9]+)/$',tagnews.showtagnews,name='showtagnews'),
    url(r'^showNewsAggregateViatag/(?P<tag_id>[0-9]+)/$',tagnews.showNewsAggregateViatag,name='showNewsAggregateViatag'),
    url(r'^showNewsAggregateVialabel/(?P<label_id>[0-9]+)/$',labelnews.showNewsAggregateVialabel,name='showNewsAggregateVialabel'),

    url(r'^showcompanynewsViacompanycode/(?P<company_code>[0-9]+)/$',companynews.showcompanynewsViacompanycode,name='showcompanynewsViacompanycode'),
    url(r'^showcompanyviatag/(?P<tag_id>[0-9]+)/$',companyTag.showcompanyviatag,name='showcompanyviatag'),
    url(r'^showtagviaCompanycode/(?P<company_code>[0-9]+)/$',companyTag.showtagviaCompanycode,name='showtagviaCompanycode'),



    url(r'^showcorrelation/$',CorrelationController.showcorrelation,name='showcorrelation'),




    url(r'^getweiboinfo/(.+)/$',weiboInfoFlow.getweiboinfo,name='getweiboinfo'),

]
