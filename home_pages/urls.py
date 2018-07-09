"""portfolio_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from home_pages import views as homepage_views

urlpatterns = [
    url(r'^about/$', homepage_views.home_view, name='homepage'),
    url(r'^home-mobile/$', homepage_views.home_m_view, name='homepage-mobile'),
    url(r'^contact/$', homepage_views.contact_view, name='contact_page'),
    url(r'^contact-mobile/$', homepage_views.contact_m_view, name='contact_page-mobile'),
    url(r'^resume/$', homepage_views.resume_view, name='resume_page'),
    url(r'^resume-mobile/$', homepage_views.resume_m_view, name='resume_page-mobile'),
    url(r'^projects/$', homepage_views.projects_view, name="projects_page"),
    url(r'^projects-mobile/$', homepage_views.projects_m_view, name="projects_page-mobile"),
    url(r'^projects/toronto_sky/$', homepage_views.toronto_sky_view, name="toronto_sky_page"),
    url(r'^projects/toronto_sky-mobile/$', homepage_views.toronto_sky_m_view, name="toronto_sky_page-mobile"),
    url(r'^projects/react-app/$', homepage_views.react_test, name='test page for react/webpack configuration'),
]
