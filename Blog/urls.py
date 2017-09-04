from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from common.views import IndexView, VersionView
from common.sitemaps import sitemaps
from common.feeds import BlogFeed

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^article/', include('article.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^column/', include('column.urls')),
    url(r'^version/$', VersionView.as_view(), name='version'),
    url(r'^rss/$', BlogFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    handler400 = 'common.views.bad_request'
    handler403 = 'common.views.permission_denied'
    handler404 = 'common.views.page_not_found'
    handler500 = 'common.views.server_error'
