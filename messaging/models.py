from django.db import models
from django.utils import timezone

# Create your models here.


class Chat(models.Model):
    chat_profile = models.ForeignKey('dating.profile', related_name='chat_profile', on_delete=models.CASCADE)
    chat_recipient = models.ForeignKey('dating.profile', related_name='chat_recipient', on_delete=models.CASCADE)
    preview = models.CharField(max_length=20, blank=False, null=False)
    unread_message_count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.chat_profile) + ' - ' + str(self.chat_recipient)


class Message(models.Model):
    message_text = models.TextField('Message', max_length=500, blank=False, null=False)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    is_outbox = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.chat) + ' - ' + str(self.id)