from urllib import response
from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import QuesModel
from django.http import HttpResponse
import requests
import json
 
# Create your views here.
def home(request):
    if request.method == 'POST':
        print(request.POST)
        questions=QuesModel.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'main/result.html',context)
    else:
        questions=QuesModel.objects.all()
        context = {
            'questions':questions
        }
        return render(request,'main/home.html',context)

class AuthRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('main/login.html') # or http response
        return None
 
def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'main/addQuestion.html',context)
    else: 
        return redirect('home') 
 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form = createuserform()
        if request.method=='POST':
            form = createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'main/register.html',context)
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'main/login.html',context)
 
def logoutPage(request):
    logout(request)
    return redirect('/')
    
def apiPage(request):
    if request.method == "POST":
        user_search=request.POST.get("subject")
        S = requests.get("https://en.wikipedia.org/w/api.php", params={
            "action" : "opensearch",
            "namespace" : "0",
            "search" : user_search,
            "limit" : "5",
            "format" : "json"
        })
    else:
        S = requests.get("https://en.wikipedia.org/w/api.php", params={
            "action" : "opensearch",
            "namespace" : "0",
            "search" : "Biology",
            "limit" : "5",
            "format" : "json"
        })
    DATA = json.loads(S.content)

    return render(request, 'main/api.html',{'s':DATA})