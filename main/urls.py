from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^serve/journal/list/$', views.serve_journal_list),
    url(r'^serve/purpose/of/trees/$', views.serve_purpose_of_trees),
    url(r'^store/subscriber/$', views.store_subscriber),
    url(r'^get/user/type/$', views.get_user_type),
    url(r'^update/need/pdf/$', views.update_need_pdf),
    url(r'^get/user/detail/$', views.get_user_detail),
    url(r'^$', views.admin_login),
]
