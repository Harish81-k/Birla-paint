from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegister(models.Model):

    name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)

    mobile = models.CharField(max_length=15)

    password = models.CharField(max_length=200)

    is_admin = models.BooleanField(default=False)

    def __str__(self):

        return self.name


from django.db import models


class Paint(models.Model):

    name = models.CharField(max_length=200)

    image = models.ImageField(upload_to='paints/')

    price = models.IntegerField()

    category = models.CharField(max_length=200)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name

# CART
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paint = models.ForeignKey(Paint, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


# WISHLIST
class Wishlist(models.Model):

    user_id = models.IntegerField(
        null=True,
        blank=True
    )

    paint = models.ForeignKey(
        Paint,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )




class Order(models.Model):

    user = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE
    )

    paint = models.ForeignKey(
        Paint,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    total_price = models.IntegerField()

    address = models.TextField()

    payment_method = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.paint.name
