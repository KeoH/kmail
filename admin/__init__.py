#encoding:utf-8
from django.contrib import admin

from kstore_mail.models import MailMessage, MailContact

class MailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject','uuid','sended_at', 'sender', 'recipient', 'readed', 'sended', 'deleted']


admin.site.register(MailMessage, MailMessageAdmin)
admin.site.register(MailContact)
