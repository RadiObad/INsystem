from django.contrib import admin
from django.urls import reverse

from .models import Category, Product, Order,  OrderItem, Oorder
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	'''
		Admin View for Category
	'''
	list_display = ('name','slug',)
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
	'''
		Admin View for Product
	'''
	list_display = ('product_name','slug','category','price', 'price_out','stock','available','created','updated',)
	list_filter = ('available','created','updated','category',)
	list_editable = ('price','price_out','stock','available',)
	prepopulated_fields = {'slug':('product_name',)}

class OrderItemAdmin(admin.TabularInline):
	'''
		Admin View for OrderItem
	'''
	model = OrderItem
	raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
	'''
		Admin View for Order
	'''
	list_display = ('id','name', 'address','city','created')
	list_filter = ('created','updated',)
	list_editable = ('name',)
	search_fields = ['first_name','last_name','email']
	inlines = [
	OrderItemAdmin,
	]

admin.site.register(Oorder, OrderAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(Order)

admin.site.register(OrderItem)
