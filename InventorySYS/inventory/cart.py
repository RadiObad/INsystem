from decimal import Decimal
from django.conf import settings
from .models import Product
from django.shortcuts import get_object_or_404


class Cart(object):
	"""docstring for Cart"""
	def __init__(self, request):
		"""initalize the cart"""
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)

		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart



	def add(self,product,quantity=1,update_quantity=False):
		product_id = str(product.id)

		if product_id not in self.cart:
			self.cart[product_id] = {'quantity':0,'price':str(product.price_out)}

		if update_quantity:
			if quantity > int(self.cart[product_id]['quantity']):
				product.stock = product.stock + int(self.cart[product_id]['quantity'])
				product.save()

				product.stock = product.stock - int(quantity)
				product.save()
			else:
				product.stock = product.stock + int(self.cart[product_id]['quantity'])
				product.save()

				product.stock = product.stock - int(quantity)
				product.save()					

			self.cart[product_id]['quantity'] = quantity
			


		else:
			self.cart[product_id]['quantity'] += quantity
			product.stock = product.stock - int(quantity)
			product.save()

		self.save()

	def save(self):

		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True


	def remove(self,product):
		product_id = str(product.id)
		if product_id in self.cart:
			product.stock += self.cart[product_id]['quantity']
			product.save()			
			del self.cart[product_id]
			self.save()

	def remove_all(self):
		product_ids = self.cart.keys()

		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			pom = str(product.id)
			if pom in self.cart:
				product.stock += self.cart[pom]['quantity']
				product.save()
			
		self.clear()	

		

	def __iter__(self):

		product_ids = self.cart.keys()

		products = Product.objects.filter(id__in=product_ids)

		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] *  item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
