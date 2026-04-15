# Create your views here.


from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Cart, Location
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.utils import timezone
from datetime import timedelta


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

def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required # only logged in users can access the dashboard
def dashboard(request):
    carts = Cart.objects.select_related('current_location').all() #the carts and their current locations

    return render(request, 'dashboard.html', {
        'carts': carts,
        'locations': Location.objects.all(),
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


#Emanuel
@login_required
def filter_carts(request):
    filter = request.GET.get('filter')

    print(f"Filter: {filter}")

    carts = Cart.objects.select_related('current_location').all()

    if filter == '30':
        carts = carts.filter(last_seen__gte=timezone.now() - timedelta(minutes=30))
    elif filter == '60':
        carts = carts.filter(last_seen__gte=timezone.now() - timedelta(hours=1))
    elif filter:
        carts = carts.filter(current_location__name=filter)
    
    """if filter == 'asc':
        carts = carts.order_by('name')
    elif filter == 'desc':
        carts = carts.order_by('-name')"""

    return JsonResponse({
        'carts': [{
            'id':               c.id,
            'name':             c.name,
            'location_raw':     c.current_location.name if c.current_location else 'Unknown',
            'location_label': c.current_location.get_name_display() if c.current_location else 'Unknown',
            'last_seen':        c.last_seen.isoformat() if c.last_seen else None,
        } for c in carts]
    })