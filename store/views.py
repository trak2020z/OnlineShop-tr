from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .models import Product, CartLine, Cart

# Create your views here.
def index(request):
    return render(request, 'store/index.html')

# Lista produktów wraz ze stronnicowaniem
ITEMS_ON_PAGE = 6
def product_list(request, cat=''):
    try:
        if cat == '':
            paginator = Paginator(Product.objects.all(), ITEMS_ON_PAGE)
        else:
            paginator = Paginator(Product.objects.filter(category=cat), ITEMS_ON_PAGE)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
    page = request.GET.get('page')
    
    if not page:
        page = 1
    products = paginator.page(page)

    # Określenie kategorii
    categories = [p.category for p in Product.objects.all()]
    categories = list(dict.fromkeys(categories))
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/list.html', context)

# Szczegóły produktu
def product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse(status=304)
    context = {
        'product': product
    }

    return render(request, 'store/details.html', context)

# Koszyk na zakupy
# Pobiera przedmioty z sesji
# W sesji przedmioty są zapisane w formacie słownika: { id_produktu: ilość, ...}
def cart(request):
    try:
        items = request.session['cart']
    except:
        items = {}
    
    if items:
        ids = items.keys()
        products = Product.objects.filter(id__in=ids)
    else:
        products=[]
    
    cart = Cart()
    for product in products:
        cart.add_to_cart(product, items[str(product.id)])
    
    page = request.GET.get('page')
    if not page:
        page=1
    print('items: {}'.format(items))
    paginator = Paginator(cart.lines, 10)
    total_price = cart.total_price
    cart = paginator.page(page)
    context = {
        'cart': cart,
        'total_price': total_price
    }
    return render(request, 'store/shopping_cart.html', context)

# Dodanie jednego produktu do koszyka
# Wywoływanie ajax
# zapis do sesji - widoki "product_list" oraz "product_list" - przycisk "Add to cart"
def add_one(request):
    data = {
        'modified': False,
    }
    item = request.GET.get('item', None)
    try:
        cart = request.session['cart']
    except:
        cart = {}
    if item in cart:
        cart[item] = cart[item] + 1
        data['modified'] = True
    else:
        cart[item] = 1
        data['modified'] = True
    request.session['cart'] = cart
    return JsonResponse(data)


# Ustawienie ilości przedmiotów w koszyku
# Wywołanie ajax
# Wykonywane tylko w widoku koszyka na zakupy - "cart"
def set_amount2(request):
    data = {
        'deleted': False,
        'price': -1
    }
    item = request.GET.get('item', None)
    try:
        amount = int(request.GET.get('amount', None))
        item = int(item)
    except TypeError:
        print('returning data: {}'.format(data))
        return JsonResponse(data)
    if amount > 100:
        amount = 100
        data['msg'] = 'Amount set to 100 due to recieving to big value.'
    
    if not Product.objects.get(id=item):
        return JsonResponse(data)

    try:
        cart = request.session['cart']
    except:
        cart = {}
    
    cart[item] = amount
    if cart[item] <= 0:
        print('delete product_id: {} from session cart'.format(item))
        cart.pop(str(item))
        data['deleted'] = True
    else:
        data['price'] = Product.objects.get(id=item).price

    print('session cart: {}'.format(cart))
    request.session['cart'] = cart
    return JsonResponse(data)

def set_amount(request):
    # Pobranie argumentów: item, amount i rzutowanie ich do int
    try:
        item = int(request.GET.get('item', None))
        amount = int(request.GET.get('amount', None))
    except ValueError: # Jak inny format niż int to błąd o złych danych
        return JsonResponse({'price': -1})
    
    data = {}
    # sprawdzanie poprawności argumentu amount
    if amount > 100:
        amount = 100
        data['msg'] = 'Amount set to 100 due to recieving to big value.'
    
    # sprawdzenie czy produkt istnieje
    try:
        product = Product.objects.get(id=item)
    except Product.DoesNotExist:
        return JsonResponse({'price': -1})
    
    # pobranie koszyka na zakupy
    cart = request.session.get('cart')
    if not cart:
        cart = {}
    
    # gdy amount <= 0 -> usuń produkt z koszyka
    if amount <= 0:
        cart.pop(str(item))
        request.session['cart'] = cart
        print('removing id: {} from {}'.format(item, cart))
        return JsonResponse({'deleted': True})
    
    # dodanie produktu do koszyka
    cart[str(item)] = amount 
    request.session['cart'] = cart

    # dane do odpowiedzi
    data['price'] = product.price
    return JsonResponse(data)
    

# Usuwanie przedkiotu z koszyka
# Wywołanie ajax
# Usuwa przedmiot - widok "cart" - przycisk "Remove"
def remove_all(request):
    item = request.GET.get('item', None)
    try:
        cart = request.session['cart']
    except:
        cart = {}
    data = {
        'modified': False
    }
    if item in cart:
        cart.pop(item)
        data['modified'] = True
    request.session['cart'] = cart
    return JsonResponse(data)