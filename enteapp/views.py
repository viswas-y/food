from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from .models import *


# 🔐 LOGIN
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_login = Login.objects.filter(email=email, password=password).first()

        if user_login:
            request.session["lid"] = user_login.pk

            if user_login.user_type == 'admin':
                return redirect('adminhome')

            elif user_login.user_type == 'user':
                u = User.objects.filter(LOGIN=user_login.pk).first()
                if u:
                    request.session["user_id"] = u.pk
                return redirect('home')

        messages.error(request, "Invalid email or password")

    return render(request, 'userlogin.html')


# 📝 REGISTER
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        login_obj = Login.objects.create(
            email=email,
            password=password,
            user_type='user'
        )

        User.objects.create(
            username=username,
            LOGIN=login_obj
        )

        return redirect('userlogin')

    return render(request, 'userregister.html')


# 🏠 HOME
def home(request):
    return render(request, "home.html")


# 📢 COMPLAINT
def complaint(request):
    lid = request.session.get("lid")

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        Complaint.objects.create(
            LOGIN_id=lid,
            subject=subject,
            message=message
        )
        return redirect("complaint")

    complaints = Complaint.objects.filter(LOGIN_id=lid).order_by("-created_at")

    return render(request, "complaints.html", {"complaints": complaints})


# 🍽️ TODAY MENU
def todaysmenu(request, type=None):
    today = date.today()

    if type:
        menu = Adminaddmenu.objects.filter(date=today, menu_type=type)
    else:
        menu = Adminaddmenu.objects.filter(date=today)

    return render(request, "menu.html", {"menus": menu})


# 👨‍💼 ADMIN HOME
def adminhome(request):
    return render(request, 'adminhome.html')


# ➕ ADD MENU
def addmenu(request):
    if request.method == "POST":
        date_val = request.POST.get("date")
        menu_type = request.POST.get("menu_type")
        items = request.POST.get("items")
        image = request.FILES.get("image")

        Adminaddmenu.objects.create(
            date=date_val,
            menu_type=menu_type,
            items=items,
            image=image
        )

        messages.success(request, "Menu Added Successfully!")
        return redirect("adminhome")

    return render(request, "addmenu.html")


# 🛒 PLACE ORDER (UPDATED - NO ROOM NUMBER)
def placeorder(request, menu_id):
    if request.method == "POST":

        lid = request.session.get("lid")

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        description = request.POST.get("description")

        Order.objects.create(
            LOGIN_id=lid,
            menu_id=menu_id,
            name=name,
            phone=phone,
            description=description,
            status="Pending"
        )

        return redirect("mybookings")

    return render(request, "orderconfirm.html")


# # 📦 MY BOOKINGS
def mybookings(request):
    lid = request.session.get("lid")

    orders = Order.objects.filter(LOGIN_id=lid).order_by('-order_date')

    return render(request, "mybookings.html", {"orders": orders})

# 💡 ADD SUGGESTION (UPDATED - NO DEPARTMENT)
def addsuggestion(request):
    if request.method == "POST":

        name = request.POST.get('name')
        meal = request.POST.get('meal')
        item = request.POST.get('item')
        description = request.POST.get('description')

        Suggestion.objects.create(
            name=name,
            meal_type=meal,
            preferred_item=item,
            description=description
        )

        return redirect('home')

    return render(request, 'addsuggestion.html')


# 👀 VIEW SUGGESTIONS (ADMIN)
def viewsuggestions(request):
    data = Suggestion.objects.all().order_by('-date')
    return render(request, 'adminsuggestionview.html', {'data': data})


# 📋 VIEW BOOKINGS (ADMIN)
def viewbookings(request):
    bookings = Order.objects.all()
    return render(request, 'adminviewbooking.html', {'bookings': bookings})


# ✅ MARK ORDER DONE
def bookingdone(request, id):
    order = Order.objects.get(id=id)
    order.status = "Done"
    order.save()
    return redirect('viewbookings')


# 👤 PROFILE
def profile(request):
    return render(request, 'profile.html')


# 🛠️ ADMIN COMPLAINT REPLY
def admincomplaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')

    if request.method == "POST":
        cid = request.POST.get('cid')
        reply = request.POST.get('reply')

        complaint = Complaint.objects.get(id=cid)
        complaint.reply = reply
        complaint.status = "Completed"
        complaint.save()

        return redirect('adminhome')

    return render(request, 'admincomplaint.html', {'complaints': complaints})