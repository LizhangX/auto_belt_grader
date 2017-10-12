from django.shortcuts import render, redirect
from .models import User
from .models import Belt
import os

# Create your views here.
def index(request):
    if 'errors' not in request.session:
        request.session['errors'] = []
    return render(request,'login_registration_app/index.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    current_user = User.objects.get(id = user_id)
    context = {
        'current_user': current_user,
        "uploads": Belt.objects.filter(user = current_user)
    }
    return render(request, 'login_registration_app/success.html', context)

def logout(request):
    request.session.pop('user_id')
    return redirect('/')

def reg(request):
    check = User.objects.register(request.POST)
    if check:
        print type(check)
        request.session['errors'] = check
        return redirect('/')

    user = User.objects.create(
        name=request.POST['name'], 
        email=request.POST['email'], 
        password=request.POST['password']
    )
    request.session['user_id'] = user.id
    request.session['errors'] = []
    request.session['status'] = 'registerted'
    return redirect('/success')

def login(request):
    log = User.objects.login(request.POST)
    if type(log) == type(User()):
        request.session['user_id'] = log.id
        request.session['errors'] = []   
        request.session['status'] = 'logged in'
        return redirect('/success')
    else:
        print log
        request.session['errors'] = log
    return redirect('/')

def upload(request):
    if request.method == "POST" and request.FILES:
        print request.FILES['upload']
        user = User.objects.get(id = request.session['user_id'])
        belt = Belt.objects.create(user=user, upload=request.FILES['upload'])
        return redirect('/success')

def delete_upload(request, upload_id):
    belt = Belt.objects.get(id=upload_id)
    belt.delete()
    if os.path.isfile("media/" + str(belt.upload)):
        os.remove("media/" + str(belt.upload))
        print "removed", belt.upload
    return redirect('/success')   