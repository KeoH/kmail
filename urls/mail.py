#encoding:utf-8
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

from kstore_mail.views import MailView,TrashMailView,DeleteMailFromMessageView, SentMailView, DraftMailView, MessageMailView, ImportantMailView, ComposeMailView

urlpatterns = [
    url(r'^inbox/$', MailView.as_view(), name='inbox'),
    url(r'^create/$', ComposeMailView.as_view(), name='compose'),
    url(r'^important/$', ImportantMailView.as_view(), name='important'),
    url(r'^sent/$', SentMailView.as_view(), name='sent'),
    url(r'^draft/$', DraftMailView.as_view(), name='draft'),
    url(r'^trash/$', TrashMailView.as_view(), name='trash'),
    url(r'^message/(?P<slug>[-\w]+)/$', MessageMailView.as_view(), name='message'),
    url(r'^deletemessage/(?P<slug>[-\w]+)/$', DeleteMailFromMessageView.as_view(), name='del-message'),
]
