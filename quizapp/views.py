from django.shortcuts import render
from quizapp.forms import user_form,user_profile_form
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from quizapp.models import questions

# Create your views here.
@login_required(login_url='quizapp:user_login')
def index(request):
    return render(request,'index.html')


def register(request):
    registered = False
    if request.method == 'POST':
        userForm = user_form(request.POST)
        userProfileForm = user_profile_form(request.POST)
        if userForm.is_valid() and userProfileForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            profile = userProfileForm.save(commit=False)
            profile.user = user  #50% connection is done by this line
            profile.save()
            registered = True

    else:
        userForm = user_form()
        userProfileForm = user_profile_form()
    return render(request,'registration.html',{'userform':userForm,'userprofileform':userProfileForm,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('quizapp:index')
        else:
            return HttpResponse('Please check your creds!!!')

    return render(request,'login.html')

def quizpage(request):
    quizzes = questions.objects.all()
    print(quizzes)
    if request.method == 'POST':
        print(request.POST)
        score,wrong,correct,total=0,0,0,0
        for q in quizzes:
            total+=1
            print(request.POST.get(q.question))
            print(q.answer)
            print()
            if q.answer ==  request.POST.get(q.question):
                score+=1
                correct+=1
            else:
                wrong+=1
        percent = round(score/(total)*100,2)
        results = {
            'score':score,
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        print(results)
        return render(request,'results.html',{'results':results})
    else:
        return render(request,'viewquestion.html',{'quizzes':quizzes})
    

def user_logout(request):
    logout(request)
    return redirect('quizapp:user_login')