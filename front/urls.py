from django.conf.urls import  url
from front.views.getcompaywebinfo import CompanyInfo,getschedule,importtokyoone,importKabucodeViaTxt
from front.controller.canslimcontroller import canslimcontroller
from front.views.pages.kabuinfo import KabuInfo
from front.views.pages.companylist import CompanyDetail
from front.controller.companycontroller import companyController
from front.views.pages.worldinfo import getworldinfo
from front.controller.indicatorcontroller import indicatorController
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url('getnik225',CompanyInfo.getnik225,name='getnik225'),

    url(r'^getnik/(?P<code>[0-9]+)/$',CompanyInfo.getnikinfo,name='getnikinfo'),
    url('importtokyoone/',importtokyoone,name='importtokyoone'),
    url(r'rise_rate_company/',KabuInfo.rise_rate_company,name='rise_rate_company'),
    url('yeardata/get/',canslimcontroller.getyeardata,name='getyeardata'),
    url('importkabucodeviatxt/',importKabucodeViaTxt,name='importKabucodeViaTxt'),

    url('getdailyinfo/',CompanyInfo.getdailyinfostack,name="getpriceinfo"),
    url('calcutefiveweight',CompanyInfo.calcutefiveweight,name="calcutefiveweight"),

     url('deleteotherData',CompanyInfo.deleteotherData,name="deleteotherData"),

    re_path(r'^homepage',KabuInfo.homepage,name="homepage"),
    url('getsettlementdata',KabuInfo.getsettlementdata,name='getsettlementdata'),
    url('getdcflist',KabuInfo.getdcflist,name='getdcflist'),

    url('getkabusumnumber',CompanyInfo.getkabusumnumber,name='getkabusumnumber'),

#     re_path(r'^detail/(?P<pk>[0-9]+)$',CompanyDetail.as_view(),name='detail'),
    re_path(r'^companyinfo/(?P<code>[0-9]+)$',companyController.getCompanyinfo,name='detailinfo'),


    url('getworldinfo',getworldinfo,name='getworldinfo'),
    url('getnikeiindex',indicatorController.getnikeiindex,name='getnikeiindex'),
#     url('getGDP',indicatorController.getGDP,name='getGDP'),

    url('getschedule/(?P<_day>[0-9]+)$',getschedule,name='getschedule'),
    re_path(r'^getsrhomepage',KabuInfo.getsrhomepage,name='getsrhomepage'),
    re_path(r'^getsettleandsunny/',KabuInfo.getsettleandsunny,name='getsettleandsunny'),
    re_path(r'^deleteotherdate/',CompanyInfo.deleteotherData,name='deleteotherdate'),

    url(r'^addtofavorite/(?P<code>[0-9]+)$',CompanyInfo.addtofavorite,name='addtofavorite'),
    url(r'^removefavorite/(?P<code>[0-9]+)$',CompanyInfo.removefavorite,name='removefavorite'),
    url(r'^favoritelist/',companyController.getFavoriteCompanylist,name='addtofavorite'),

    url('savemapimage',CompanyInfo.savemapimage,name='savemapimage'),

    url('getDailySummary/',KabuInfo.getDailySummary,name='getDailySummary'),
    url('getnewhouseOpeninfo/',indicatorController.getHouseOpen,name='getNewHouseOpenInfo'),

    url('unusualamount/get/',KabuInfo.getUnusualAmount,name='getUnusualAmount'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),

]
