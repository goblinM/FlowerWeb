"""FlowerWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from flower import views as flower_view
from flower.view.house import house_view
from flower.view.stock import stock_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$',flower_view.index,name="index"),
    url(r'^flower/$',flower_view.flower, name="flower"),
    url(r'^collectData/$',house_view.collectData, name="collectData"),
    url(r'^exportData/$',house_view.exportData, name="exportData"),
    url(r'^workingData/$',house_view.workingData, name="workingData"),

    url(r'^forecasePlace/$',house_view.forecasePlace, name="forecasePlace"),
    url(r'^forecaseArea1/$',house_view.forecaseArea1, name="forecaseArea1"),
    url(r'^forecaseArea2/$',house_view.forecaseArea2, name="forecaseArea2"),

    url(r"^stock/$",stock_view.index, name="stock"),
    url(r"^addStock/$", stock_view.addStock, name="addStock"),
    url(r"^uploadStock/$", stock_view.uploadStock, name="uploadStock"),
    url(r"^showStock/$", stock_view.showStock, name="showStock"),
    url(r"^showStockInfo/$", stock_view.showStockInfo, name="showStockInfo"),
    url(r"^comparedData/$", stock_view.comparedData, name="comparedData"),
    url(r"^getInfoData/$", stock_view.getInfoData, name="getInfoData"),
    url(r'^exportInfoData/$',stock_view.exportInfoData, name="exportInfoData"),
    url(r'^workingInfoData/$',stock_view.workingInfoData, name="workingInfoData"),
    url(r"^forecaseInfoData/$", stock_view.forecaseInfoData, name="forecaseInfoData"),
    url(r'',house_view.house_index, name="house_index")

]
