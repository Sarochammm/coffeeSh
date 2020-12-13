from django.contrib import admin

# Register your models here.
from .models import Member
from .models import Shop
from .models import Payment
from .models import Product
from .models import Receipt
from .models import ReceiptLineItem

admin.site.register(Member)
admin.site.register(Shop)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Receipt)
admin.site.register(ReceiptLineItem)