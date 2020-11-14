from django.shortcuts import render, get_object_or_404, redirect, reverse, Http404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator

from dating.decorators import client_required
from dating.models import Profile

from .forms import MessageForm
from .models import Message, Chat
# Create your views here.


@client_required
def inbox(request):
    profile = request.user.profile
    inbox_messages = Message.objects.filter(is_outbox=False)

    if profile.unread_message_count:
        profile.unread_message_count = 0
    return render(request, 'messaging/inbox.html', {'inbox': inbox_messages})


@client_required
def chat(request, profile_number):
    profile = request.user.profile
    friend = get_object_or_404(Profile, profile_number=profile_number)
    form = MessageForm()
    message_list = None
    friend_chat = Chat.objects.filter(chat_recipient=friend, chat_profile=profile).first()
    if friend_chat:
        messages_query = Message.objects.filter(chat=friend_chat).all()
        page = request.GET.get('page')
        paginator = Paginator(messages_query, 5)
        message_list = paginator.get_page(page)


    return render(request, 'messaging/chat.html', {'friend': friend,
                                                   'form': form,
                                                   'message_list': message_list,
                                                   'friend_chat': friend_chat})


@client_required
def send_message(request, profile_number):
    if request.method == 'POST':
        profile = request.user.profile
        friend = get_object_or_404(Profile, profile_number=profile_number)

        is_friend = friend.friends.filter(id=profile.id).exists()
        if is_friend:
                form = MessageForm(request.POST)
                if form.is_valid():
                    msg_text = form.cleaned_data['message_text']
                    timestamp = timezone.now()
                    # Save for recipient
                    friend_chat, created = Chat.objects.get_or_create(chat_profile=friend, chat_recipient=profile)
                    msg = Message(chat=friend_chat, message_text=msg_text)
                    msg.save()
                    friend_chat.unread_message_count += 1
                    friend_chat.timestamp = timestamp
                    friend_chat.preview = (profile.user.username + ': ' + msg_text)[0:50]
                    friend_chat.save()
                    friend.unread_message_count += 1
                    friend.save()
                    # save for sender
                    my_chat, created = Chat.objects.get_or_create(chat_profile=profile, chat_recipient=friend)
                    msg = Message(chat=my_chat, message_text=msg_text, is_outbox=True)
                    msg.save()
                    my_chat.timestamp = timestamp
                    my_chat.preview = ('Me: ' + msg_text)[0:50]
                    my_chat.save()
                    messages.success(request, 'Message sent..')
                else:
                    messages.success(request, 'Unable to send message...')

        else:
            raise Http404('You are not friends')

    return redirect(reverse('messaging:chat', args=[profile_number, ]))
