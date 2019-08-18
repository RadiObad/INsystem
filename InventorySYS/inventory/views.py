from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.http import require_POST
from .cart import Cart
from .models import Order, Product, Category, OrderItem, Oorder
from .forms import OrderForm, ProductForm, CartAddProductForm, OrderCreateForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework import authentication, permissions

from django.contrib.auth.models import User
from django.template.loader import render_to_string


User = get_user_model()
class HomeView(View):
    def get(self, request, *args, **Kwargs):
        return render(request,'charts.html',{'customers': 10})

def get_data(request, *args, **Kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []
    def te(self,order):
        items_sold=[]
        items_lables=[]
        pro=[]
        pro1=[]
        products = Product.objects.all()
        
        for product in products:
                item_sum=sum(it.get_cost() for it in product.order_items.all())
                items_sold.append(int(item_sum))           
        for item in order:
            if item:
                item_sum=sum(it.get_cost() for it in item.items.all())
                #items_sold.append(int(item_sum))

                for prud in item.items.all():
                    product_id=prud.product.id

                    items_lables.append(prud.product.product_name)
                    pro.append(str(prud.product.price_out))
                    pro1.append(prud.get_cost())                  

                    

                    #pro_sum=sum(pro.append(str(prud.product.price_out)))

        m=sum(items_sold)
        return items_sold,items_lables,pro,pro1

    def wek(self):
        date_lte = datetime.datetime.now()
        date_gte = datetime.date(2019,7,21)-timedelta(days=1)
        order = Oorder.objects.filter(created__lte=date_lte,created__gte=date_gte)
        
        return self.te(order)
        
    def get(self, request, format=None):
        items_sold,items_lables,pro,pro1 =self.wek()
        labels = items_lables
        my_data_items = items_sold

        data = {
            "labels": labels,
            "my_data": my_data_items,
            "pro": pro,
            "pro1": pro1,
            }
        return Response(data)



#to view home the frist page when the system run
@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    orders = Oorder.objects.all()
    return render(request, 'index.html', {'orders': orders})



@login_required
def show(request, order_id):
    order = get_object_or_404(Oorder,id =order_id)
    return render(request, 'show.html', {'order': order})



@login_required
def order_detils(request, order_id):
    order = get_object_or_404(Oorder,id =order_id)
    return render(request, 'order_detils.html', {'order': order})
@login_required
def add_new(request):
    cart = Cart(request)
    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            for item in cart:
                order.price =item['price']

            order.save()
            for item in cart:
                order.product.add(item['product'])

    else:
        form = OrderForm()
        return render(request, 'new.html', {'form':form})

@login_required
def new(request):
    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/', messages.success(request, 'Order was successfully created.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm()
        return render(request, 'new.html', {'form':form})

@login_required
def edit(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if form.save():
                return redirect('/', messages.success(request, 'Order was successfully updated.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm(instance=order)
        return render(request, 'edit.html', {'form':form})

@login_required
def destroy(request, order_id):
    order = Oorder.objects.get(id=order_id)
    order.delete()
    return redirect('/', messages.success(request, 'Order was successfully deleted.', 'alert-success'))



#Product

@login_required
def index_product(request):
    products = Product.objects.filter(available=True)
    return render(request, 'index_product.html', {'products': products})    

@login_required
def new_product(request):
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/products', messages.success(request, 'Product was successfully created.', 'alert-success'))
            else:
                return redirect('/products', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/products', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        product_form = ProductForm()
        return render(request, 'new_product.html', {'product_form':product_form})    

@login_required
def destroy_product(request, product_id):
    #order = Order.objects.filter(product_id=product_id).count()

    #if order > 0:
    #     return redirect('/products', messages.success(request, 'Cannot delete product while its order exists.', 'alert-danger'))    
    #else:
    #    product = Product.objects.get(id=product_id)
    #    product.delete()
    #    return redirect('/products', messages.success(request, 'Product was successfully deleted.', 'alert-success'))      

    if Product.objects.filter(id=product_id).update(active='0'):
        return redirect('/products', messages.success(request, 'Product was successfully deleted.', 'alert-success'))  
    else:
        return redirect('/products', messages.danger(request, 'Cannot delete product while its order exists.', 'alert-danger'))  

@login_required
def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'],'update':True})
   
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
        
    context = {
        'category':category,
        'categories':categories,
        'products':products,
        'cart_product_form':cart_product_form,
        'cart':cart
    }
    return render(request,'test.html',context)
@login_required
def product_detail(request,id,slug):

    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    context = {
        'product':product,
        
    }
    return render(request,'deatil.html',context)



@login_required
def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('test')

@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'],'update':True})
    context = {
        'cart':cart,
       
    }
    return render(request,'cart_detail.html',context)           

@login_required
@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
            )
    return redirect('test')


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            Oorder = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=Oorder,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])

            cart.clear()
            context = {
                'order':Oorder,
            }
            
            return render(request,'created.html',context)

    else:
        form = OrderCreateForm()
    context = {
        'cart':cart,
        'form':form
    }
    return render(request,'create.html',context)
