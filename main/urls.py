from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^serve/journal/list/$', views.serve_journal_list),
    url(r'^store/name/and/number/$', views.store_name_and_number),
    url(r'^serve/purpose/of/trees/$', views.serve_purpose_of_trees),
    url(r'^store/subscriber/$', views.store_subscriber),
    url(r'^get/user/type/$', views.get_user_type),
    url(r'^update/need/pdf/$', views.update_need_pdf),
    url(r'^get/user/detail/$', views.get_user_detail),
    url(r'^login/$', views.login),
    url(r'^serve/subscribers/list/$', views.serve_subscribers_list),
    url(r'^logout/$', views.logout),
    url(r'^store/email/$', views.store_email),
    # url(r'^/update/profile/$', views.update_profile),
    url(r'^serve/profile/data/$', views.serve_profile_data),
    url(r'^$', views.admin_login),
    url(r'^register/user/$', views.register_user),
    url(r'^update_user/$', views.update_user),
    url(r'^update_user_profile$', views.update_user_profile),
    url(r'^new/journal/$', views.new_journal),
    url(r'^remove_journal/$', views.remove_journal),
    url(r'^update/status/active/$', views.update_status_active),
    url(r'^update/status/inactive/$', views.update_status_inactive),
    url(r'^print/labels/$', views.print_labels),
    
    
]
