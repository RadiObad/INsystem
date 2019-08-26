from django.forms import ModelForm
from django import forms
from .models import Order, Product,Oorder, Category

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]
class OrderForm(ModelForm):
    OPTIONS = (
        ('Postpay','Postpay'),
        ('Prepay (Full)','Prepay (Full)'),
        ('Prepay (Half)', 'Prepay (Half)')
    )
    OPTIONS2 = (
        ('Confirm', 'Confirm'),
        ('Ready', 'Ready'),
        ('Send', 'Send'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled')
    )
    order_status = forms.TypedChoiceField(required=False, choices=OPTIONS2, widget=forms.RadioSelect)
    payment_option = forms.ChoiceField(choices=OPTIONS)

    class Meta:
        model = Order
        fields = ['name','phone','address','payment_option','order_status']


class ProductForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='')
    class Meta:
        model = Product
        fields = ['product_name','product_details','price','price_out','stock','category' ]




class CartAddProductForm(forms.Form):
    # TODO: Define form fields here
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)    


class OrderCreateForm(forms.ModelForm):
    OPTIONS = (
        ('دين','دين'),
        ('نقد', 'نقد')
    )
    OPTIONS2 = (
        ('توكد', 'توكد'),
        ('جاهز', 'جاهز'),
        ('سلم', 'سلم'),
        ('إرجاع', 'إرجاع'),
        ('ألغيت', 'ألغيت')
    )
    order_status = forms.TypedChoiceField(required=False, choices=OPTIONS2, widget=forms.RadioSelect)
    payment_option = forms.ChoiceField(choices=OPTIONS)

    class Meta:
        model = Oorder
        fields = ('name','phone', 'address', 'payment_option','order_status', 'city')
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug')