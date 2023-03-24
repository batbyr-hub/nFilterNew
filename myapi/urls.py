# myapi/urls.py

from django.conf.urls import include, url #path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'^/sms', views.ReceiveSmsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url('', include(router.urls)),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^prepaid', views.receive_sms_prepaid),
    url(r'^postpaid', views.receive_sms_postpaid),
    # url(r'^api/tutorials$', views.tutorial_list),
    # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    # url(r'^api/tutorials/published$', views.tutorial_list_published)

    #url('path/to/my/view/', MySimpleView.as_view())
]