import datetime

from django.shortcuts import render

from collegegatepass.forms import StudentForm, LoginForm, PassRequestForm, DepartmentLoginForm
from collegegatepass.models import StudentModel,PassRequestModel

import smtplib
from datetime import  datetime
from collegegatepass.service import getadminpassrequests, getstudentpassrequests, getdepartmentpassrequests
from collegegatepass.service1 import finduser


def send_otp(email,otp):

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
        s.starttls()
        s.login("bhanujuluri17@gmail.com", "Amigoece@21")

        s.sendmail("sender_email", email, otp)
        s.quit()
        print("mail sent successfully")

    except Exception as e:
        print(e)
        print("Send OTP via Email","Please enter the valid email address OR check an internet connection")


def registration(request):

    # Get the posted form
    registrationForm = StudentForm(request.POST,request.FILES)

    print("in function")
    if registrationForm.is_valid():
        print("in if")
        regModel = StudentModel()

        regModel.name = registrationForm.cleaned_data["name"]
        regModel.email = registrationForm.cleaned_data["email"]
        regModel.mobile = registrationForm.cleaned_data["mobile"]
        regModel.rno = registrationForm.cleaned_data["rno"]
        regModel.password = registrationForm.cleaned_data["password"]
        regModel.year = registrationForm.cleaned_data["year"]
        regModel.section = registrationForm.cleaned_data["section"]
        regModel.branch = registrationForm.cleaned_data["branch"]
        regModel.photo = registrationForm.cleaned_data["photo"]

        user = StudentModel.objects.filter(rno=regModel.rno).first()

        if user is not None:
            return render(request, 'registration.html', {"message": "User All Ready Exist"})
        else:
            regModel.save()
            return render(request, 'registration.html', {"message": "Registred Sucessfully"})
    else:
        print("in else")
        return render(request, 'registration.html', {"message": "Invalid Form"})

def loginpage(request):
    return render(request,'login.html',{})

def login(request):

    if request.method == "GET":
        # Get the posted form
        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            if uname == "security" and upass == "security":
                request.session['role'] = "admin"
                request.session['username'] = "security"

                return render(request, "viewpassrequestes.html", {"passrequests":getadminpassrequests()})

            else:

                user = StudentModel.objects.filter(rno=uname, password=upass).first()

                if user is not None:
                    request.session['role'] = "student"
                    request.session['username'] =user.rno

                    return render(request, "viewpassrequestes.html", {"passrequests":getstudentpassrequests(user.rno)})

                else:
                    return render(request, 'index.html', {"message": "Invalid Credentials"})

        return render(request, 'index.html',  {"message": "Invalid Credentials"})

    return render(request, 'index.html',  {"message": "Invalid Credentials"})

def departmentloginaction(request):

    if request.method == "GET":
        # Get the posted form
        loginForm = DepartmentLoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]
            branch = loginForm.cleaned_data["branch"]

            if uname == "department" and upass == "department":
                request.session['role'] = "department"
                request.session['username'] = "department"
                request.session['branch'] =branch

                return render(request, "viewpassrequestes.html", {"passrequests":getdepartmentpassrequests(branch)})

            else:
                return render(request, 'index.html', {"message": "Invalid Credentials"})

        return render(request, 'index.html',  {"message": "Invalid Credentials"})

    return render(request, 'index.html',  {"message": "Invalid Credentials"})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})

#====================================================================================================

def addpassrequest(request):

    passrequestForm = PassRequestForm(request.POST)

    if passrequestForm.is_valid():

        date = passrequestForm.cleaned_data["date"]
        time = passrequestForm.cleaned_data["time"]
        reason = passrequestForm.cleaned_data["reason"]


        strdate=str(datetime.now()).split(" ")[0]

        isrequested=False

        for passrequest in getstudentpassrequests(request.session['username']):
            print("Date1:",str(passrequest.date),"Date2:",str(strdate))
            if str(passrequest.date)==str(strdate):
                isrequested=True

        if not isrequested:
            PassRequestModel(date=date,time=time,reason=reason,status="pending",studentid=request.session['username']).save()
        else:
            return render(request, 'addpassrequest.html', {"message": "You have Reached to Day Limit"})

        return render(request, 'addpassrequest.html', {"message": "PassRequest Posted SuccessFully"})

    return render(request, 'addpassrequest.html', {"message": "PassRequest Request Failed"})

def getpassrequests(request):

    role=request.session['role']

    if role=="student":
        return render(request, "viewpassrequestes.html", {"passrequests": getstudentpassrequests(request.session['username'])})

    elif role == "admin":
        return render(request, "viewpassrequestes.html",{"passrequests": getadminpassrequests()})

    elif role == "department":
        branch = request.session['branch']
        return render(request, "viewpassrequestes.html",{"passrequests": getdepartmentpassrequests(branch)})

def deletepassrequest(request):

    passrequestid= request.GET['passrequestid']
    PassRequestModel.objects.get(id=passrequestid).delete()

    role = request.session['role']

    if role == "student":
        return render(request, "viewpassrequestes.html",
                      {"passrequests": getstudentpassrequests(request.session['username'])})

    elif role == "admin":
        return render(request, "viewpassrequestes.html", {"passrequests": getadminpassrequests()})

    elif role == "department":
        branch = request.session['branch']
        return render(request, "viewpassrequestes.html", {"passrequests": getdepartmentpassrequests(branch)})

def approveorrejectrequest(request):

    rid=request.GET['rid']
    status=request.GET['status']

    PassRequestModel.objects.filter(id=rid).update(status=status)

    role = request.session['role']

    if role == "student":
        return render(request, "viewpassrequestes.html",
                      {"passrequests": getstudentpassrequests(request.session['username'])})

    elif role == "admin":
        return render(request, "viewpassrequestes.html", {"passrequests": getadminpassrequests()})

    elif role == "department":
        branch = request.session['branch']
        return render(request, "viewpassrequestes.html", {"passrequests": getdepartmentpassrequests(branch)})

def recognizeuser(request):

    finduser()

    role = request.session['role']

    if role == "student":
        return render(request, "viewpassrequestes.html",
                      {"passrequests": getstudentpassrequests(request.session['username'])})

    elif role == "admin":
        return render(request, "viewpassrequestes.html", {"passrequests": getadminpassrequests()})

    elif role == "department":
        branch = request.session['branch']
        return render(request, "viewpassrequestes.html", {"passrequests": getdepartmentpassrequests(branch)})