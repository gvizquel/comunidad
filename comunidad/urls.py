from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    url(r'^demografia/', include('demografia.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': reverse_lazy('login')}, name='logout'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]