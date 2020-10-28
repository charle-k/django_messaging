from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from dating.decorators import client_required

# Create your views here.


@login_required
def home(request):
    return render(request, 'dating/home.html')


@client_required
def dashboard_user(request):
    return render(request, 'dating/dashboard_user.html')



@client_required
def my_friends(request):
    return render(request, 'dating/my_friends.html')
