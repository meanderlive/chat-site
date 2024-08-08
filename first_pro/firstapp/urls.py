from django.urls import path
# from .views import accountapi,signupapi,accloginapi,fetchAccountapi,home,shop_profile,fetch_shop_profile,addProduct,fetch_addProduct,fetch_jobdetails,jobdetails,documents,fetch_documents,kdfeed,comments,likeapi,fetch_kdfeed,fetch_signupapi,fetch_signupapi,frthrServices,fetch_frthrServices,jobs,bidPrice,fetch_jobs,fetch_bidPrice,otp_loginApi,fetch_jobs_user, fetch_bidPrice_partner,accept_bidPrice,fetch_jobdetailspartner,fetch_Product_partner,register,login,addfarm,fetchfarm,addlatlog,fetchlatlog,bankaccount,AddquestionAPI
from .views import *
from .views import home

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path, re_path
from django.urls import path, re_path, include
#from firstapp import routing
# handler404 = custom_404



urlpatterns = [
                  path('business-home',business_home,name="business-home"),
                  #path('register',business_register,name="business_register"),
                  path('business-about',business_about , name="business-about"),
                  path('business-blog' , business_blog, name="business-blog"),
                  path('business-case-studies',business_case_studies,name="business-case-studies"),
                  path('business-contact',business_contact,name="business-contact"),
                  path('business-services', business_services,name="business-services"),
                  path('business-services-deatails',business_services_detail,name="business-services-details"),
                  path('home', home, name="home"),
                  path('', register_view, name='register'),
                  path('login/', login_view, name='login'),
                  path('profile',create_or_update_profile,name="profile"),
                  path('get-profile',get_profile ,name="get_profile"),
                  path('profile/delete/', delete_profile, name='profile_delete'),
                  path('user_list', user_list_view, name='user_list'),
                  path('chat/<str:username>/', chat_view, name='chat'),
                  path('new_chat/<str:room_name>/', chat_room, name='chat_room'),



              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
settings.DEBUG = True
