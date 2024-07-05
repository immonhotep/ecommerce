from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('add_cart/<slug:slug>/',views.add_cart,name='add_cart'),
    path('remove_cart/<slug:slug>/',views.remove_cart,name='remove_cart'),
    path('profile/',views.user_profile,name='profile'),
    path('shipping/',views.shipping,name='shipping'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.register,name='register'),
    path('change_password/',views.change_password,name='change_password'),
    path('order/',views.send_order,name='order'),
    path('product/<slug:slug>/',views.product_detail,name='product'),
    path('add_new_product/',views.add_new_product,name='add_new_product'),
    path('modify_product/<slug:slug>/',views.modify_product,name='modify_product'),
    path('delete_product/<slug:slug>/',views.delete_product,name='delete_product'),
    path('products/<slug:slug>/',views.product_list,name="products"),
    path('category/',views.category,name='category'),
    path('add_new_category/',views.add_new_category,name='add_new_category'),
    path('modify_category/<slug:slug>/',views.modify_category,name='modify_category'),
    path('delete_category/<slug:slug>/',views.delete_category,name='delete_category'),
    path('about/',views.about,name='about'),
    path('check_questions/',views.check_questions,name='check_questions'),
    path('search/',views.search,name='search'),
    path('check_orders/',views.check_orders,name='check_orders'),
    path('order_details/<int:pk>/',views.order_details,name='order_details'),
    path('order_summary/<uuid:order_id>/',views.order_summary,name='order_summary'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),

]
