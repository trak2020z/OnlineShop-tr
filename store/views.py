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
def set_amount(request):
    data = {
        'deleted': False,
        'price': -1
    }
    item = request.GET.get('item', None)
    try:
        amount = int(request.GET.get('amount', None))
    except:
        return JsonResponse(data)
    try:
        cart = request.session['cart']
    except:
        cart = {}
    
    cart[item] = amount
    if cart[item] <= 0:
        cart.pop(item)
        data['deleted'] = True
    else:
        data['price'] = Product.objects.get(id=int(item)).price
    print(cart)
    request.session['cart'] = cart
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