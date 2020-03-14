from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from store.models import Product, Cart
from .models import Order, Ordered

from .forms import OrderForm

# Create your views here.
@login_required
def orders_list(request):

    # User bez flagi is_staff widzi tylko swoje zamówienia
    if not request.user.is_staff:
        orders = Paginator(Order.objects.filter(user=request.user), 10)
    # User z flagą is_staff widzi wszystkie 
    else:
        orders = Paginator(Order.objects.all(), 10)
    
    # Stronnicowanie
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        if type(page) is not int:
            page = int(page)
    except:
        return HttpResponse('I see what you did there.')
    
    # Sprawdź czy numer strony jest za wysoki
    if page <= orders.num_pages:
        orders = orders.page(page)
    else:
        return HttpResponse("Page does not exist!")

    context = {
        'orders': orders,
    }
    return render(request, 'transactions/list.html', context)

# Wyświetlanie informacji o zamówieniu i zamówionych produktów
def order(request, access_code):
    # TODO: Zamówienia usera widoczne tylko dla niego (logowanie potrzebne)
    # TODO: Zamówienia bez usera po podaniu kodu (logowanie nie potrzebne)
    try:
        order = Order.objects.get(access_code=access_code)
    except Order.DoesNotExist:
        HttpResponse('Cant find this object')
    
    # Zamówione produkty
    ordered_products = Ordered.objects.filter(order=order)
    cart = Cart()

    # Dodanie produktów do klasy (wrappera) - Cart
    for p in ordered_products:
        cart.add_to_cart(Product.objects.get(id=p.product.id), p.amount)
    
    context = { 'order': order, 'cart': cart }
    return render(request, 'transactions/order.html', context)


# Edycja danych zamówienia
class OrderEditView(UpdateView):
    # TODO: Edycja tylko gdy należy do usera lub user ma flagę is_staff
    # TODO: Jeśli nie ma usera to edytować może tylko user z flagą is_staff
    form_class = OrderForm
    template_name = 'transactions/order_form.html'
    queryset = Order.objects.all()

    def form_valid(self, form):
        order = form.save()
        return redirect('transactions:order', order.access_code)
    
    def get_object(self):
        access_code = self.kwargs.get("access_code")
        return get_object_or_404(Order, access_code=access_code)
    
# Składanie zamówienia
def new_order(request): 
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Gdy user jest zalogowany przypisz mu zamówienie
            if request.user.is_authenticated:
                order = form.custom_save(request.user)
            # Gdy nie jest zalogowany to brak usera w zamówieniu
            else:
                order = form.save()
            cart = request.session['cart']

            # Znajdź przedmioty z kosza na zakupy
            ids = cart.keys()
            products = Product.objects.filter(id__in=ids)

            # Dodaj do bazy danych
            total = 0
            for product in products:
                Ordered.objects.create(
                    product=product,
                    order=order,
                    amount=cart[str(product.id)]
                )
                total = total + (cart[str(product.id)] * product.price)
            
            # Zaaktualizuj koszt całkowity zamówienia
            Order.objects.filter(id=order.id).update(total_price=total)
            # Wyczyść koszyk
            request.session['cart'] = {}

            # Strona z kodem zamówienia
            return redirect('transactions:new_order_created', order.access_code)
    
    # Wyswietlenie formularza
    form = OrderForm()
    context = {'form': form}
    return render(request, 'transactions/order_form.html', context)

def new_order_created(request, access_code):
    return render(request, 'transactions/new_order_created.html', {'access_code': access_code})


# Usuwanie zamówienia
class OrderDeleteView(DeleteView):
    # TODO: Usuwanie tylko gdy należy do usera lub user ma flagę is_staff
    # TODO: Jeśli nie ma usera to usunąć może tylko user z flagą is_staff
    template_name = 'transactions/delete_form.html' 

    def get_object(self):
        access_code = self.kwargs.get('access_code')
        return get_object_or_404(Order, access_code=access_code)
    
    
    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('transactions:list')
        else:
            return reverse('store:index')

# Wyszukanie zamówienia
def find_order(request):
    # Widok do wyszukiwania zamówień po access_code
    access_code = request.GET.get('access_code')
    if access_code:
        order = Order.objects.get(access_code=access_code)

        if order:
            return redirect('transactions:order', order.access_code)

    return render(request, 'transactions/find_order.html')

# Obsługa płatności
def payment(request, access_code):
    # TODO: przekierowanie do zapłaty
    order = Order.objects.get(access_code=access_code)
    if order.is_paid:
        return reverse('transactions:order', access_code)
    
    if order.payment_type == 1:
        msg = "Paying via card"
    elif order.payment_type == 2:
        msg = "Paying via blik"
    elif order.payment_type == 3:
        msg = "Information needed for transfer"
    elif order.payment_type == 4:
        msg = "Paying via Paypal"
    else:
        msg = "Wrong payment type was chosen."

    return render(request, 'transactions/payment.html', {'msg': msg})


