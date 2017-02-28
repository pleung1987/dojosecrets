from django.shortcuts import render, redirect
from .models import User, Message
from django.db.models import Count
from django.contrib import messages

def index(request):
    if "id" in request.session:
        return redirect('/secret')
    return render (request,'login/index.html')

def secret(request):
    if "id" not in request.session:
        return redirect('/')
    user= User.objects.get(id=request.session["id"])
    secret= Message.objects.annotate(num_like=Count('likes'))
    context={
        "user": user,
        "secret": secret,
    }
    return render(request,'login/secrets.html',context)

def process(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        user_valid = User.objects.validation(request.POST)
        if user_valid[0]==True:
            request.session["id"]= user_valid[1].id
            return redirect('/secret')
        else:
            print "flashes", user_valid[1]
            for msg in user_valid[1]:
                messages.add_message(request,messages.INFO,msg)
            return redirect('/')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        user_valid= User.objects.authenticate(request.POST)
        if user_valid[0]==True:
            request.session["id"]=user_valid[1].id
            return redirect('/secret')
        else:
            messages.add_message(request,messages.INFO,user_valid[1])
            return redirect('/')

def createsecret(request):
    if request.method != 'POST':
        return redirect('/')
    if "id" not in request.session:
        return redirect('/')
    secret= Message.objects.validation(request.POST, request.session['id'])
    if secret[0]== True:
        return redirect('/secret')
    else:
        messages.error(request,secret[1])
        return redirect('/secret')

def like(request, message_id):
    liking = Message.objects.like(request.session["id"], message_id)
    return redirect('/secret')

def popular(request):
    if "id" not in request.session:
        return redirect('/')
    user= User.objects.get(id=request.session["id"])
    secret= Message.objects.annotate(numlikes=Count('likes')).order_by('-numlikes')
    context={
        "user": user,
        "secret": secret,
    }
    return render(request, 'login/popular.html', context)

def delete(request, id):
    try:
        target= Message.objects.get(id=id)
    except Message.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/secret')
    target.delete()
    return redirect('/secret')

def logout(request):
    if "id" in request.session:
        request.session.pop("id")
    return redirect('/')
