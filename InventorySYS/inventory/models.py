from django.db import models
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timedelta, time
import datetime
# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_category',args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,db_index=True)
    product_details = models.TextField()
    price= models.IntegerField()
    price_out= models.IntegerField()    
    active = models.IntegerField(default='1')
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
            ordering = ('-created',)
            index_together = (('id','slug'),)
            verbose_name = "Product"
            verbose_name_plural = "Products"

    def __str__(self):
        return str(self.product_name)

    def get_absolute_url(self):
        return reverse('product_detail',args=[self.id,self.slug])
  
    def get_expenses(self):
        expenses = self.price * self.stock
        return expenses


    def get_profit(self):
        expenses = self.price * self.stock
        revenue =  sum(item.get_cost() for item in self.order_items.all())        
        profit =   expenses - revenue
        return profit

class Order (models.Model):
    name = models.CharField(max_length=200)
    product = models.ManyToManyField(Product, related_name='items')
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_option = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)


    class Meta:
        ordering = ('name',)

    def __str__(self):
            return self.name



class Oorder(models.Model):
    name  = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address     = models.CharField(max_length=250)
    city        = models.CharField(max_length=100)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50)
    payment_option = models.CharField(max_length=50)
    
    class Meta:
        ordering = ('-created',)
        verbose_name = "Oorder"
        verbose_name_plural = "Oorders"

    def __str__(self):
        return 'Oorder {}'.format(self.id)

    def get_total_cost(self):
        total_cost =  sum(item.get_cost() for item in self.items.all())
        return total_cost    
    def get_absolute_url(self):
        return reverse('product_detail',args=[self.id,self.slug])
    def te(self,order):
        neq=[]
        m=[]
        for item in order:
            if item:
                for it in item.items.all():
                    s=it.get_cost()
                    neq.append(int(s))
            m=sum(neq)
        return m, neq

    def wek(self):
        date_lte = datetime.datetime.now()
        date_gte = datetime.date(2019,7,21)-timedelta(days=1)
        order = Order.objects.filter(created__lte=date_lte,created__gte=date_gte)
        self.te(order)
        
    def current_week(self):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        order = Oorder.objects.filter(created__range=[start_week, end_week])    
        
        return  self.te(order)
    
    def current_day(self):
        today = datetime.datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.datetime.combine(today, time())
        today_end = datetime.datetime.combine(tomorrow, time())
        order = Oorder.objects.filter(created__lte=today_end, created__gte=today_start)

        #date = datetime.datetime.today()
        #order = Oorder.objects.filter(created__day=date.day,created__year=date.year,created__month=date.month)
        return self.te(order)
    
    def current_month(self):
        date = datetime.datetime.today()
        order = Oorder.objects.filter(created__year=date.year,created__month=date.month)
        return self.te(order)

    def current_year(self):
        date = datetime.datetime.today()
        order = Oorder.objects.filter(created__year=date.year)
        return self.te(order)
        

class OrderItem(models.Model):
    order       = models.ForeignKey(Oorder,related_name='items',on_delete=models.CASCADE)
    product     = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price       = models.DecimalField(max_digits=10,decimal_places=2)
    quantity    = models.PositiveIntegerField(default=1)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"


    def __str__(self):
        return '{}'.format(self.id)


    def get_cost(self):
        return self.price * self.quantity
   