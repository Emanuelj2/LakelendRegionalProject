# Create your views here.


from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Cart
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required



# home page view
def home(request):
    return render(request, 'home.html')


# user login view
def login(request):
    if request.method == 'POST':
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard')
       else:
           return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


@login_required # only logged in users can access the dashboard
def dashboard(request):
    carts = Cart.objects.select_related('current_location').all() #the carts and their current locations
    return render(request, 'dashboard.html', {
        'carts': carts,
        'available_count':    carts.filter(status='available').count(),
        'in_use_count':       carts.filter(status='in_use').count(),
        'maintenance_count':  carts.filter(status='maintenance').count(),
    })


@login_required
def get_all_carts(request):
    carts = Cart.objects.select_related('current_location').all()
    return JsonResponse({'carts': [{
        'id': c.id,
        'name': c.name,
        'status': c.status,
        'location': c.current_location.name if c.current_location else 'Unknown',
        'last_seen': str(c.last_seen),
    } for c in carts]})

@login_required
def search(request):
    #TODO
    pass


@login_required
def filter():
    #TODO
    pass

