import razorpay
from django.conf import settings
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from .forms import (
    SignupForm,
    LoginForm,
    PaintForm
)
from .models import (
    UserRegister,
    Paint,
    Cart,
    Wishlist,
    Order
)

# =========================================
# HOME PAGE
# =========================================
def home(request):
    paints = Paint.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'paints': paints
    })


# =========================================
# HOME AFTER LOGIN
# =========================================
def home_page(request):
    if not request.session.get('user_id'):
        return redirect('login')

    paints = Paint.objects.all().order_by('-id')
    return render(request, 'home.html', {
        'paints': paints
    })


# =========================================
# SIGNUP (RESTRICTED TO ADMIN ONLY)
# =========================================
def signup_view(request):
    # 1. SECURITY BLOCK: Logged-in user admin kakapothe page access blocked!
    if not request.session.get('is_admin'):
        return redirect('login')

    form = SignupForm()
    message = ''

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            if UserRegister.objects.filter(email=email).exists():
                message = 'Email already exists'
            else:
                form.save()
                # Account create chesaka Admin, Users list dashboard page ki return autaru
                return redirect('admin_users') 

    return render(request, 'signup.html', {
        'form': form,
        'message': message
    })


# =========================================
# LOGIN (STRICT EMAIL AUTHENTICATION MATCH)
# =========================================
def login_view(request):
    form = LoginForm()
    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Direct parameters checking on UserRegister custom model
                user = UserRegister.objects.get(
                    email=email,
                    password=password
                )

                # SESSION STORAGE DATA SETUP
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['is_admin'] = user.is_admin

                # ROUTING REDIRECT LOOP BASED ON PRIVILEGES
                if user.is_admin:
                    return redirect('admin_dashboard')
                
                return redirect('home_page')

            except UserRegister.DoesNotExist:
                message = 'Invalid Email or Password'

    return render(request, 'login.html', {
        'form': form,
        'message': message
    })


# =========================================
# LOGOUT
# =========================================
def logout_view(request):
    request.session.flush()
    return redirect('login')


# =========================================
# ADMIN DASHBOARD
# =========================================
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    users = UserRegister.objects.all().order_by('-id')[:5]
    paints = Paint.objects.all()

    context = {
        'user_count': UserRegister.objects.count(),
        'paint_count': Paint.objects.count(),
        'order_count': Cart.objects.count(),
        'users': users,
        'paint_list': paints,
        'orders': []
    }
    return render(request, 'admin_dashboard.html', context)


# =========================================
# UPLOAD PAINT
# =========================================
def upload_paint(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    form = PaintForm()
    if request.method == 'POST':
        form = PaintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')

    return render(request, 'upload_paint.html', {
        'form': form
    })


# =========================================
# DELETE PAINT
# =========================================
def delete_paint(request, paint_id):
    if not request.session.get('is_admin'):
        return redirect('login')

    paint = get_object_or_404(Paint, id=paint_id)
    paint.delete()
    return redirect('paint_list')


# =========================================
# PAINT LIST
# =========================================
def paint_list(request):
    paints = Paint.objects.all().order_by('-created_at')
    return render(request, 'paint_list.html', {
        'paints': paints
    })


# =========================================
# ADMIN USERS PANEL
# =========================================
def admin_users(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    users = UserRegister.objects.all().order_by('-id')
    return render(request, 'admin_users.html', {
        'users': users,
        'user_count': UserRegister.objects.count()
    })


# =========================================
# DELETE USER
# =========================================
def delete_user(request, user_id):
    if not request.session.get('is_admin'):
        return redirect('login')

    user = get_object_or_404(UserRegister, id=user_id)

    # SECURE PREVENT: KICK OUT TRAP FOR ACCIDENTAL ADMIN DELETION
    if user.is_admin:
        return redirect('admin_users')

    user.delete()
    return redirect('admin_users')


# =========================================
# COLOR LIST
# =========================================
def color_list(request):
    paints = Paint.objects.all()
    return render(request, 'colors.html', {
        'paints': paints,
        'selected_color': 'all'
    })


# =========================================
# COLOR FILTER + SEARCH
# =========================================
def color_paints(request, color_name):
    search = request.GET.get('search')

    if color_name == "all":
        paints = Paint.objects.all()
    else:
        paints = Paint.objects.filter(category__iexact=color_name)

    if search:
        paints = paints.filter(name__icontains=search)

    cart_count = 0
    user_id = request.session.get('user_id')
    if user_id:
        cart_count = Cart.objects.filter(user_id=user_id).count()

    return render(request, 'colors.html', {
        'paints': paints.order_by('-id'),
        'selected_color': color_name,
        'cart_count': cart_count
    })


# =========================================
# ADD TO CART
# =========================================
def add_to_cart(request, paint_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    paint = get_object_or_404(Paint, id=paint_id)
    cart_item = Cart.objects.filter(user_id=user_id, paint=paint).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            user_id=user_id,
            paint=paint,
            quantity=1
        )
    return redirect('cart')


# =========================================
# CART PAGE
# =========================================
def cart_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id)
    wishlist_items = Wishlist.objects.filter(user_id=user_id)

    total_price = 0
    for item in cart_items:
        total_price += (item.paint.price * item.quantity)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'total_price': total_price
    })


# =========================================
# REMOVE CART
# =========================================
def remove_cart(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    item = get_object_or_404(Cart, id=cart_id, user_id=user_id)
    item.delete()
    return redirect('cart')


# =========================================
# ADD TO WISHLIST
# =========================================
def add_to_wishlist(request, paint_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    paint = get_object_or_404(Paint, id=paint_id)
    exists = Wishlist.objects.filter(user_id=user_id, paint=paint).exists()

    if not exists:
        Wishlist.objects.create(
            user_id=user_id,
            paint=paint
        )
    return redirect('cart')


# =========================================
# PAINT DETAIL
# =========================================
def paint_detail(request, id):
    paint = get_object_or_404(Paint, id=id)
    return render(request, 'paint_detail.html', {
        'paint': paint
    })


# =========================================
# INCREASE QUANTITY
# =========================================
def increase_quantity(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    item = get_object_or_404(Cart, id=cart_id, user_id=user_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


# =========================================
# DECREASE QUANTITY
# =========================================
def decrease_quantity(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    item = get_object_or_404(Cart, id=cart_id, user_id=user_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


# =========================================
# BUY NOW PAGE (RAZORPAY INTEGRATION)
# =========================================
def buy_now(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    paint = get_object_or_404(Paint, id=id)
    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    payment = client.order.create({
        "amount": int(paint.price) * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "paint": paint,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    }
    return render(request, "buy.html", context)


# =========================================
# CHECKOUT PAGE
# =========================================
def checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id)
    total_price = 0
    for item in cart_items:
        total_price += (item.paint.price * item.quantity)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_amount': int(total_price) * 100
    }
    return render(request, 'checkout.html', context)


# =========================================
# PLACE ORDER
# =========================================
def place_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id)
    address = request.POST.get('address', 'Customer Address')
    payment = request.POST.get('payment', 'Cash On Delivery')

    for item in cart_items:
        Order.objects.create(
            user_id=user_id,
            paint=item.paint,
            quantity=item.quantity,
            total_price=(item.paint.price * item.quantity),
            address=address,
            payment_method=payment
        )

    cart_items.delete()
    return redirect('orders')


# =========================================
# ORDERS PAGE
# =========================================
def orders(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    orders_list = Order.objects.filter(user_id=user_id).order_by('-id')
    total_price = 0
    for item in orders_list:
        total_price += item.total_price

    return render(request, 'orders.html', {
        'orders': orders_list,
        'total_price': total_price
    })


# =========================================
# PAYMENT SUCCESS
# =========================================
def payment_success(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id)
    address = request.GET.get('address', 'Customer Address')

    for item in cart_items:
        Order.objects.create(
            user_id=user_id,
            paint=item.paint,
            quantity=item.quantity,
            total_price=(item.paint.price * item.quantity),
            address=address,
            payment_method='Online Payment'
        )

    cart_items.delete()
    request.session['success_msg'] = 'Order Placed Successfully'
    return redirect('orders')