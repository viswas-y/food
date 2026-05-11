from django.db import models


class Login(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class User(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname


class Complaint(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )

    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Adminaddmenu(models.Model):

    MENU_TYPES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
    )

    date = models.DateField()
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES)
    items = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.menu_type} - {self.date}"


# ✅ UPDATED ORDER (room_number removed)
class Order(models.Model):

    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    menu = models.ForeignKey(Adminaddmenu, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, default="Pending")
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# ✅ UPDATED SUGGESTION (department removed)
class Suggestion(models.Model):

    MEAL_TYPES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Evening', 'Evening'),
    )

    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    preferred_item = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name