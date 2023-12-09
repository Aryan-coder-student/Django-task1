from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib import messages
from .models import UsersData, tag
from django.contrib.auth.decorators import login_required


def pushData(
    usertype, fname, lname, username, photo, mail, password, address, state, city, pin
):
    print(photo)
    user = User.objects.create_user(
        username=username,
        email=mail,
        password=password,
        first_name=fname.capitalize(),
        last_name=lname.capitalize(),
    )
    user.save()
    user = auth.authenticate(username=username, password=password)
    tg = tag.objects.get(tag_name=usertype)
    storeData = UsersData.objects.create(
        UserType=tg,
        username=username,
        profile_photo=photo,
        address=address,
        state=state,
        city=city,
        pin=pin,
    )
    storeData.save()
    return redirect("/home")


def checkemail(mail, UserName):
    try:
        user_name = User.objects.get(Q(username=UserName) | Q(email=mail))
        return False
    except:
        return True


def signupdoc(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        photo = request.FILES.get("ProfilePhoto")
        mail = request.POST.get("mail")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        address = request.POST.get("address")
        state = request.POST.get("state")
        city = request.POST.get("city")
        pin = request.POST.get("pin")

        if password != confirmpassword:
            messages.warning(request, "Passwords do not match")
        elif len(pin) != 6:
            messages.warning(request, "Invalid Pin")
        elif checkemail(mail, username):
            pushData(
                "doctor",
                fname,
                lname,
                username,
                photo,
                mail,
                password,
                address,
                state,
                city,
                pin,
            )
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            messages.success(request, "User Created successfully")
        else:
            messages.warning(request, "User Already Exists")
    return render(request, "sign.html")


def signupat(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        photo = request.FILES.get("ProfilePhoto")
        mail = request.POST.get("mail")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        address = request.POST.get("address")
        state = request.POST.get("state")
        city = request.POST.get("city")
        pin = request.POST.get("pin")
        if password != confirmpassword:
            messages.warning(request, "Passwords do not match")
        elif (not fname.isalpha()) or (not lname.isalpha()):
            messages.warning(request, "Enter Valid Name")
        elif len(pin) != 6:
            messages.warning(request, "Invalid Pin")
        elif checkemail(mail, username):
            pushData(
                "patient",
                fname,
                lname,
                username,
                photo,
                mail,
                password,
                address,
                state,
                city,
                pin,
            )
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            messages.success(request, "User Created successfully")
        else:
            messages.warning(request, "User Already Exists")
    return render(request, "sign.html")


def index(request):
    return render(request, "index.html")


@login_required(login_url="/")
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url="/")
def home(request):
    details = UsersData.objects.get(username=request.user.username)
    print(details.profile_photo)
    context = {"details": details}
    return render(request, "home.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check = auth.authenticate(username=username, password=password)
        if check is None:
            messages.warning(request, "Invalid Credentials")
        else:
            auth.login(request, check)
            return redirect("/home")
    return render(request, "login.html")
