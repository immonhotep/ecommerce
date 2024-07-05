from django.contrib import admin
from .models import * 

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Orders)
admin.site.register(User)
admin.site.register(OrderItem_final)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Payment_and_transport)
admin.site.register(customer_question)
admin.site.register(customer_review)
admin.site.register(customer_rating)


class ProfileInline(admin.StackedInline):
    model = ShippingAddress



class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username','first_name', "last_name","email","phone_number"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)




class OrderItem_finalInline(admin.StackedInline):
    model = OrderItem_final
    
    extra = 0


class Payment_and_transportInline(admin.StackedInline):
    model = Payment_and_transport

    extra=0

class OrdersAdmin(admin.ModelAdmin):

    model = Orders
    readonly_fields = ['date_added','updated']
    fields = ['user','city','state','country','address','zipcode','first_name','last_name','email','phone_number','shipped']
    inlines = [OrderItem_finalInline,Payment_and_transportInline]


admin.site.unregister(Orders)
admin.site.register(Orders, OrdersAdmin)
 