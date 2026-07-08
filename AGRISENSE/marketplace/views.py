from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, CropListingForm
from .models import CropListing, PriceHistory, User
from django.http import JsonResponse
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, CropListingForm
from .models import CropListing, PriceHistory, User
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db import DatabaseError

def home(request):
    """Home page - public landing page"""
    try:
        listings_count = CropListing.objects.count()
        sellers_count = User.objects.filter(is_seller=True).count()
        recent_listings = CropListing.objects.all()[:6]
    except (DatabaseError, Exception) as e:
        # If database connection fails, show default values
        print(f"Database error in home view: {e}")
        listings_count = 0
        sellers_count = 0
        recent_listings = []
        messages.warning(request, 'Database connection issue. Please ensure MongoDB is running.')
    
    context = {
        'listings_count': listings_count,
        'sellers_count': sellers_count,
        'recent_listings': recent_listings,
    }
    return render(request, 'marketplace/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful, and you are now logged in!')
            if user.is_seller:
                return redirect('seller_dashboard')
            return redirect('marketplace')
        else:
            # show form errors (duplicate username/email, role not selected, etc.)
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = UserRegistrationForm()
    return render(request, 'marketplace/register.html', {'form': form})

def login_view(request):
    error_message = None
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')
                if next_url:
                    return redirect(next_url)
                if user.is_seller:
                    return redirect('seller_dashboard')
                return redirect('marketplace')
            # User not found or due to invalid password:
            if User.objects.filter(username=username).exists():
                error_message = 'Invalid password. Please try again.'
            else:
                error_message = 'Account not registered. Please register first.'
            messages.error(request, error_message)
        except Exception as exc:
            error_message = 'Database connection error. Ensure MongoDB is running and restart the server.'
            messages.error(request, error_message)
            print('Login DB exception:', exc)
    return render(request, 'marketplace/login.html', {'error_message': error_message, 'next': next_url})

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('marketplace')
    listings = CropListing.objects.filter(seller=request.user)
    if request.method == 'POST':
        form = CropListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('seller_dashboard')
    else:
        form = CropListingForm()
    return render(request, 'marketplace/seller_dashboard.html', {'form': form, 'listings': listings})

@login_required(login_url='login')
def marketplace(request):
    """Marketplace view - shows all listings"""
    try:
        listings = CropListing.objects.all().order_by('-created_at')
    except (DatabaseError, Exception) as e:
        print(f"Database error in marketplace view: {e}")
        listings = []
        messages.warning(request, 'Database connection issue. Please ensure MongoDB is running.')
    
    is_seller = request.user.is_seller if request.user.is_authenticated else False
    context = {
        'listings': listings,
        'is_seller': is_seller,
    }
    return render(request, 'marketplace/marketplace.html', context)



@login_required
def price_trend(request, listing_id):
    listing = CropListing.objects.get(id=listing_id)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    prices = PriceHistory.objects.filter(
        commodity=listing.crop_name,
        variety=listing.variety,
        date__range=[start_date, end_date]
    ).order_by('date')
    data = {}
    for p in prices:
        if p.date not in data:
            data[p.date] = []
        data[p.date].append(float(p.price))
    chart_data = {
        'labels': [str(d) for d in sorted(data.keys())],
        'prices': [sum(prices_list)/len(prices_list) if prices_list else 0 for prices_list in data.values()]
    }
    all_prices = [float(p.price) for p in prices]
    if all_prices:
        min_price = min(all_prices)
        max_price = max(all_prices)
        avg_price = sum(all_prices) / len(all_prices)
    else:
        min_price = max_price = avg_price = 0
    return JsonResponse({
        'chart_data': chart_data,
        'min_price': min_price,
        'max_price': max_price,
        'avg_price': avg_price
    })

@login_required
def contact_seller(request, listing_id):
    listing = CropListing.objects.get(id=listing_id)
    return JsonResponse({
        'phone': listing.seller.phone_number,
        'email': listing.seller.email
    })
