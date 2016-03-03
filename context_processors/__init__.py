#encoding:utf-8
from kstore_mail.models import MailMessage, MailContact

def num_unread_messages(request):
    if request.user.is_authenticated():
        num = MailMessage.objects.new_messages(request.user).count()
        return {'num_unread_messages': num}
    else:
        return {}

def return_contacts(request):
    if request.user.is_authenticated():
        contacts = MailContact.objects.filter(owner=request.user)
        return {'mail_contacts': contacts, 'num_mail_contacts': contacts.count()}
    else:
        return {}
