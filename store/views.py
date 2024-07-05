from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import UpdateUserDataForm, UserLoginForm,SignupForm, UpdateOrdersFormCustomer, UpdateOrdersFormGuest,ShippingForm,ChangeUserPasswordForm,Shipping_checkForm
from .forms import payment_and_transportForm,QuestionForm,Add_category_Form,Add_product_Form
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash,get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import user_is_superuser,user_not_authenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.text import slugify


# for email verification these will need
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from .forms import  SetPasswordForm, PasswordResetForm





def  store(request):

    p = Paginator(Product.objects.all(),6)
    page= request.GET.get('page')
    products = p.get_page(page)

    context={'products':products}
    return render(request,'store/store.html',context)


def category(request):

    p = Paginator(Category.objects.all(),6)
    page= request.GET.get('page')
    categories = p.get_page(page)                       
    context={'categories':categories}

    return render(request,'store/categories.html',context)


@user_is_superuser
def add_new_category(request):



    if request.method == "POST":
        form = Add_category_Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f'New category added to database')

        else:
            for error in list(form.errors.values()):
                              messages.error(request,error)
           

    else:
        form = Add_category_Form()

    context = {'form':form,'type':'Category','action':'Add New'}
    return render(request,'store/add_category_and_product.html', context)




@user_is_superuser
def add_new_product(request):

    

    if request.method == "POST":

        form = Add_product_Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'New Product added to database')

        else:
             for error in list(form.errors.values()):
                  messages.error(request,error)


    else:
        form = Add_product_Form()

    context={'form':form,'type':'Product','action':'Add new'}
    return render(request,'store/add_category_and_product.html',context)



@user_is_superuser
def modify_category(request,slug):

    category = Category.objects.get(slug=slug)

    if request.method == "POST":

        form = Add_category_Form(request.POST, request.FILES, instance=category)
        if form.is_valid():
            data=form.save(commit=False)
            data.slug=slugify(request.POST['title'])
            data.save()

            messages.success(request,'category modified')
            return redirect('modify_category',category.slug)
        
        else:
            for error in list(form.errors.values()):
                              messages.error(request,error)
           

    else:
        form = Add_category_Form(instance=category)

    context={'form':form,'object':category,'type':'category','action':'Modify'}
    return render(request,'store/add_category_and_product.html',context)


@user_is_superuser
def delete_category(request,slug):

     category = Category.objects.get(slug=slug)
     if request.method == "POST":
        category.delete()
        messages.success(request,f'{category} has been deleted')
        return redirect('category')
     
     else:
         context={'object':category,'type':'Category'}
         return render(request,'store/confirm_delete.html',context)





def product_detail(request,slug):

    product = Product.objects.get(slug=slug)
    p = Paginator(customer_review.objects.filter(product=product),2)
    page= request.GET.get('page')
    comments = p.get_page(page)
    
    all_rate=product.averagerate
    num_rate=product.countrate
    num_review = product.countreview


    if request.user.is_authenticated:
        if customer_rating.objects.filter(product=product,user=request.user).exists():
            rated = customer_rating.objects.get(product=product,user=request.user)
            rate_range=rated.star_rating

        else:
            rate_range=0
            rated=None
       

    
        if request.method == "POST":
                
                star = request.POST.get('star')
                comment = request.POST.get('comment')

                if comment:
                    customer_review.objects.create(user=request.user,
                                            product=product,
                                            comment=comment)
                    
                    messages.success(request,'Your review has been saved')
                                     
                if star:

                    rated, created =  customer_rating.objects.get_or_create(user=request.user,
                                                                                  product=product)
                    if created :
                        rated.star_rating = star
                        rated.save()
                        messages.success(request,'Your rating has been saved')                     

                    else:
                        messages.error(request,'You already rated this item') 
                        rated = None  
                                                           
                return redirect('product',product.slug)
    else:
        rate_range=0
        rated = None

    
    context={'product':product,'comments':comments,'rated':rated,'rate_range':rate_range,'all_rate':all_rate,'num_review':num_review}
    return render(request,'store/product.html',context)


def product_list(request,slug):

    category= Category.objects.get(slug=slug)
    
    products = Product.objects.filter(category=category)
    context={'products':products,'category':category}
    return render(request,'store/products.html',context)


@user_is_superuser
def modify_product(request,slug):
    product = Product.objects.get(slug=slug)

    if request.method == "POST":
        form = Add_product_Form(request.POST,request.FILES,instance=product)
        if form.is_valid():
            data = form.save(commit=False)
            data.slug=slugify(request.POST['title'])
            data.save()


            messages.success(request,f'Product: {product} has been modified')
            return redirect('store')
        else:
            for error in list(form.errors.values()):
                              messages.error(request,error)
           
    else:

        form = Add_product_Form(instance=product)

    context={'form':form}
    return render(request,'store/add_category_and_product.html',context)


@user_is_superuser
def delete_product(request,slug):

    product = Product.objects.get(slug=slug)

    if request.method =="POST":
        product.delete()
        messages.success(request,f'product: {product} has been deleted')
        return redirect('store')
    
    context={'object':product,'type':'Product'}
    return render(request,'store/confirm_delete.html',context)





   
@user_is_superuser
def check_orders(request):

    check = request.GET.get('inlineRadioOptions')
    if check == None:
        check = "all"
    
    if check == "all":
        p = Paginator(Orders.objects.all(),10)

    elif check == "shipped":
        p = Paginator(Orders.objects.filter(shipped=True),10)

    else:
        p = Paginator(Orders.objects.filter(shipped=False),10)



    page= request.GET.get('page')
    orders = p.get_page(page)                       
    context={'orders':orders,'check':check}
    return render(request,'store/check_orders.html',context)



@user_is_superuser
def order_details(request,pk):

    order = get_object_or_404(Orders, pk=pk)
    orderitems = OrderItem_final.objects.filter(order = pk)

    if request.method == "POST":
        form = Shipping_checkForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            messages.success(request,'shipping altered')
            return redirect('order_details',pk=pk)


    form = Shipping_checkForm(instance=order) 
    context={'order':order,'orderitems':orderitems,'form':form}
    return render(request,'store/order_details.html',context)



def order_summary(request,order_id):

   
    order = get_object_or_404(Orders, order_id=order_id)
    orderitems = OrderItem_final.objects.filter(order = order)
    transport = Payment_and_transport.objects.get(order = order)
    total_price = sum(item.item.price * item.quantity for item in orderitems)
    subtotal_price = total_price + transport.trasport_price

    context ={'order':order,'orderitems':orderitems,'transport':transport,'subtotal_price':subtotal_price}
    return render(request,'store/order_summary.html',context)






def about(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Your Question has sent, we will send response soon')
            return redirect('store')
        
        else:
             for error in list(form.errors.values()):
                              messages.error(request,error)
           
     
    else:

        form = QuestionForm()



    context={'form':form}
    return render(request,'store/about.html',context)


@user_is_superuser
def check_questions(request):

    p = Paginator(customer_question.objects.all(),3)
    page=request.GET.get('page')
    questions= p.get_page(page)

    if request.method == "POST":

        question_num = request.POST.get('Question_number')

        response_text = request.POST.get('comment')

        if response_text and question_num:
          
            question_qs = customer_question.objects.filter(id=question_num)
            question_qs_values = question_qs.values('first_name','last_name','email','user_info')[0]

            first_name = question_qs_values.get('first_name')
            last_name = question_qs_values.get('last_name')
            email = question_qs_values.get('email')
            question = question_qs_values.get('user_info')
            #fake mail for admin
            admin_mail="ecommercer@admin.com"


            subject = f'Reply to question: {question[:50]} ....'
            email_body = """\
                            <html>
                            <head></head>
                            <body>
                            <hr>                          
                            <p>%s</p>
                            <hr>
                            </body>
                            </html>
                            """ % (response_text)

            email_from = f'ecommerce website <{request.user}>'
            recipient_list = [email,]
            

            mail = EmailMessage(subject,email_body,email_from,[email,admin_mail])
            mail.content_subtype = "html"
            try: 
                mail.send()
                question_qs.update(answered=True)
                messages.success(request,f'You sent answer mail to {email} ')
            except ConnectionRefusedError:
                 messages.error(request,'Mail unable to sent, <b> SERVER CONNECTION ERROR </b> ')
            except Exception:
                 messages.error(request,'Mail unable to sent, <b> SERVER PROBLEM</b>')


        else:
            messages.error(request,'you must fill the textfield and select question to send answer')
            
    context={'questions':questions}
    return render(request,'store/customer_questions.html',context)



def  cart(request):
        
        # loged user cart in the database:
        if request.user.is_authenticated:
            user = request.user
            cart_items = OrderItem.objects.filter(user=user,ordered=False)
            total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)
            total_items = sum( 1 * cart_item.quantity for cart_item in cart_items)
            

            context={'cart_items':cart_items,'cart':'cart','total_price':total_price,'total_items':total_items}
            return render(request,'store/cart.html',context)
        
        # anyonymous user cart in session
        else:
            cart = request.session.get('cart', {})
            cart_items = {}       
            total_price = 0
            total_items = 0
            

            for slug, cart_item in cart.items():
                product = Product.objects.get(slug=slug)
                quantity = cart_item['quantity']
                total_price += product.price * quantity
                total_items += quantity
                cart_items.update({product:quantity})
            
            
                
                    
            context={'cart_items':cart_items,'total_price':total_price,'total_items':total_items}
            return render(request,'store/cart.html',context)

    
           
# add  product to cart(OrderItems)

def add_cart(request, slug):

    if request.method == "POST":

        next = request.GET.get("next", None)
        item = get_object_or_404(Product,slug=slug)

        if request.user.is_authenticated:
                
            order_item ,created = OrderItem.objects.get_or_create(
            user=request.user,
            item =item,   
            )

            if created == True:
                order_item.total = order_item.get_total
                order_item.save()
                messages.success(request,f' new item added to cart: {order_item.item.title}')

            if created == False:
                order_item.quantity+=1
                order_item.total = order_item.get_total
                order_item.save()
                messages.success(request,f' {order_item.item.title} quantity increased - currently have: {order_item.quantity}')
            


        
            if next and next != '':
                return HttpResponseRedirect(redirect_to=next)
            
            #anonymous user  add item to session
        else:
            cart = request.session.get("cart", {})
            if slug in cart:
                cart[slug]['quantity'] += 1
                messages.success(request,f'{slug}  quantity increased - currently have: {cart[slug]["quantity"]}')
                
            else:
                product = Product.objects.get(slug=slug)
                cart[slug] = {'quantity': 1}
                messages.success(request,f'{slug} added to cart')
    
        request.session['cart'] = cart


        if next and next != '':
            return HttpResponseRedirect(redirect_to=next)


# remove products from Cart(OrderItems)

def remove_cart(request, slug):

    if request.method == "POST":

        next = request.GET.get("next", None)
        item = get_object_or_404(Product,slug=slug)
       

        if request.user.is_authenticated:

            
                order_item = OrderItem.objects.get(user=request.user,item=item)
                order_item.quantity-=1
                order_item.total = order_item.get_total
                order_item.save()

                if order_item.quantity <= 0:
                    order_item.delete()
                    messages.success(request,f'{order_item.item.title} removed from your cart')
                else:
                    messages.success(request,f'{order_item.item.title}  quantity decreased - currently have: {order_item.quantity}')

                if next and next != '':
                    return HttpResponseRedirect(redirect_to=next)


        #anonymous user remove item from session

        else:
            cart = request.session.get("cart", {})
            if slug in cart:
                cart[slug]['quantity'] -= 1
                if cart[slug]["quantity"] > 0:
                    messages.success(request,f'{slug} quantity decreased - currently have: {cart[slug]["quantity"]}')
                
                if cart[slug]['quantity'] <= 0:
                    cart.pop(slug)
                    messages.success(request,f'{slug} item  removed from your cart')
         
            
            request.session['cart'] = cart


            if next and next != '':
                return HttpResponseRedirect(redirect_to=next)

             
    else:
         messages.error(request,"you have no permission to do this")


       
#Send Order

def send_order(request):

    user = request.user
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=user,ordered=False)
        profile = User.objects.get(id=request.user.id)
        shipping = ShippingAddress.objects.get(user = request.user)

        print(profile.last_name)

        if not profile.last_name  or not profile.first_name  or not profile.phone_number:
            messages.info(request,'please fill your profile')
            return redirect('profile')
        
        if not shipping.address  or  not shipping.city  or  not shipping.zipcode or not  shipping.country  or not shipping.state :

             messages.info(request,'please fill your shipping address')
             return redirect('shipping')

        



        total_price = sum(item.item.price * item.quantity for item in items)
        total_items = sum( 1 * item.quantity for item in items)


        if not items:
            return redirect('store')
        
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)

        if request.method == "POST":
            
            data=Orders.objects.create(city=shipping_user.city,
                                state=shipping_user.state,
                                country=shipping_user.country,
                                address=shipping_user.address,
                                zipcode=shipping_user.zipcode,
                                first_name=user.first_name,
                                last_name=user.last_name,
                                email=user.email,
                                phone_number=user.phone_number,
                                user=request.user,)

     
            for object in items:

                OrderItem_final.objects.create(order=data,
                                            item=object.item,
                                            total=object.total,
                                            quantity=object.quantity,
                                            user = user,
                                            )

                object.delete()


            payform = payment_and_transportForm(request.POST)
            if payform.is_valid():
                payment =  payform.cleaned_data['payment_type']
                transport = payform.cleaned_data['transport_service']
                if transport == "GLS Transport service":
                    price = 2500
                else:
                    price = 1900

                payment_transport = Payment_and_transport.objects.create(
                order = data,
                payment_type=payment,
                trasport_price = price,
                transport_service = transport,)
                payment_transport.save()

                messages.success(request,'order has been saved')

                subject= f'about order:{data.order_id}'
                email_from = f'Ecommerce website @Admin'
                email_body = """\
                            <html>
                            <head></head>
                            <body>
                            <hr> 
                            <h3>Congratulation %s %s your order sent successfull </h3>                         
                            <p> you can see order status here: http://127.0.0.1:8000/order_summary/%s</p>
                            <hr>
                            </body>
                            </html>
                            """ % (user.first_name,user.last_name,data.order_id)
                
                mail = EmailMessage(subject,email_body,email_from,[user.email])
                mail.content_subtype = "html"
                try:
                     mail.send()

                except ConnectionRefusedError:
                     messages.error(request, "Problem sending order confirmation email, <b> MAIL SERVER CONNECTION PROBLEM</b>")
                     
                except Exception:
                     messages.error(request, "Problem sending order confirmation email,, <b>SERVER PROBLEM</b>")
                     
                
    

                return redirect('order_summary',order_id=data.order_id)
                 
        payform = payment_and_transportForm()
        context={'items':items,'total_price':total_price,'total_items':total_items,'shipping_user':shipping_user,'user':user,'payform':payform}
        return render(request,'store/order.html',context)

    else:

        user=None
        cart = request.session.get('cart',{})
        cart_items = {}
        total_price = 0
        total_items = 0

        for slug, cart_item in cart.items():
                    product = Product.objects.get(slug=slug)
                    quantity = cart_item['quantity']
                    total_price += product.price * quantity  
                    total_items += quantity
                    cart_items.update({product:quantity})

        if not total_items:
             return redirect('store')


        if request.method == "POST":
            form = UpdateOrdersFormGuest(request.POST)
            payform = payment_and_transportForm(request.POST)

            if form.is_valid():

                data = form.save()

                for key,value in cart_items.items():
                    price = key.price * value
                    OrderItem_final.objects.create(order=data,
                                         item=key,
                                         total=price,
                                         quantity=value,
                                         user=user,
                                         )
                    
               
                del request.session['cart']

            
                if payform.is_valid():
                    payment =  payform.cleaned_data['payment_type']
                    transport = payform.cleaned_data['transport_service']
                    if transport == "GLS Transport service":
                        price = 2500
                    else:
                        price = 1900
                    payment_transport = Payment_and_transport.objects.create(
                    order = data,
                    payment_type=payment,
                    trasport_price = price,
                    transport_service = transport,)
                    payment_transport.save()
                  
                
                    messages.success(request,' order has been saved')

                    subject= f'about order:{data.order_id}'
                    email_from = f'Ecommerce website @Admin'
                    email_body = """\
                            <html>
                            <head></head>
                            <body>
                            <hr> 
                            <h3>Congratulation %s %s your order sent successfull </h3>                         
                            <p> you can see order status here: http://127.0.0.1:8000/order_summary/%s</p>
                            <hr>
                            </body>
                            </html>
                            """ % (data.first_name,data.last_name,data.order_id)
                
                    mail = EmailMessage(subject,email_body,email_from,[data.email])
                    mail.content_subtype = "html"
                    try :
                         mail.send()
                    except ConnectionRefusedError:
                        messages.error(request,'unable to sent order confirmation mail,<b>MAIL SERVER CONNECTION PROBLEM</b>')
                    except Exception:
                         messages.error(request,'unable to sent order confirmation mail, MAIL SERVER ERROR')

                    

                    return redirect('order_summary',order_id=data.order_id)
              
    

            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
        else:
            form = UpdateOrdersFormGuest()
            payform = payment_and_transportForm()


        context={'form':form,'cart_items':cart_items,'total_price':total_price,'total_items':total_items,'payform':payform}
        return render(request,'store/order.html',context)
        







def  search(request):

    item_prices=Product.objects.values_list('price')

    if item_prices:
        priceMin=item_prices.order_by('price').first()[0]
        priceMax=item_prices.order_by('price').last()[0]
    else:
        priceMin=0
        priceMax=1000

    


    
    if request.method =="POST":

        price_value= request.POST.get('price_value') if request.POST.get('price_value') != None else '0'
        item = request.POST.get('search')
        
        searching = Product.objects.filter((Q(price__gte=price_value) & (Q(title__icontains=item) | Q(description__icontains=item))))

        

        if not searching:
            messages.error(request,f'this product: {item} not found')
            return redirect('search')
        
        else:
            messages.success(request,'products found:')
            context={'searching':searching,'priceMin':priceMin,'priceMax':priceMax}
            return render(request,'store/search.html',context)

    else:
        context={'priceMin':priceMin,'priceMax':priceMax}
        return render(request,'store/search.html',context)

        





# user management 

def user_login(request):

    

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = UserLoginForm(request,data=request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            
            if user is not None:
                login(request, user)
                messages.success(request, f'welcome: {request.user} please check your information')
                return redirect('store')
            
        else:
             messages.error(request, 'Username or password invalid')       
        

    else:
        form = UserLoginForm()

    context={'form':form}
    return render(request, 'store/login.html', context)



# User Registration
def register(request):


    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request,user,form.cleaned_data['email'])

        else: 
            for error in list(form.errors.values()):
                messages.error(request, error)
            
  

    else:
        form = SignupForm()

    context={'form':form}
    return render(request,'store/register.html',context)


  
def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    try: 
        email.send()
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    except ConnectionRefusedError:
         messages.error(request,'unable to sent activation email, <b>MAIL SERVER CONNECTION PROBLEM</b>')

    except Exception:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')




def activate(request,uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user =None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"thank you for your confirmation now you can login")
        return redirect('login')
    
    else:
        messages.error(request,"Activation link is not valid")
    return redirect('store')








    
# logout User 

@login_required(login_url='store')
def logoutUser(request):
    logout(request)
    return redirect('/')


#User Profile 
@login_required(login_url='store')
def user_profile(request):

    user=request.user
    all_order = OrderItem_final.objects.filter(user=user)
    
    p = Paginator(OrderItem_final.objects.filter(user=user),3)
    page= request.GET.get('page')
    orders = p.get_page(page)
    total_price = sum(order.item.price * order.quantity for order in all_order)
    total_items = sum( 1 * order.quantity for order in all_order)
    
    if request.method == "POST":
        form = UpdateUserDataForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You had successfully submitted the request')
            return redirect('order')
        else:

            for error in list(form.errors.values()):
                    messages.error(request,error)        
         


    else:
        form = UpdateUserDataForm(instance=user)
        

    context = {'form':form,'orders':orders,'total_price':total_price,'total_items':total_items}
    return render(request, 'store/profile.html', context)




@login_required(login_url='store')
def change_password(request):
    
    if request.method == "POST":
        form = ChangeUserPasswordForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,f'{request.user} your password has been changed')
            return redirect('store')
          
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    else:
        form = ChangeUserPasswordForm(request.user)

    context={'form':form}
    return render(request, 'store/change_password.html', context)
     




@login_required(login_url='store')
def shipping(request):

    shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
    if request.method == "POST":
        
        form = ShippingForm(request.POST, instance=shipping_user)
        if form.is_valid():
            form.save()
            messages.success(request,'Your information has beed updated')
            return redirect('order')

        else:
            
            for error in list(form.errors.values()):
                              messages.error(request,error)
           

    else:
        form = ShippingForm(instance=shipping_user)
        

    context={'form':form,}
    return render(request,'store/shipping.html',context)

 



@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                try: 
                    email.send()
                    messages.warning(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>We sent instructions to your mailbox about the password reset, please follow the instructions.
                           <br>If you don't receive our mail please check your spam folder
                        </p>
                        """
                    )
                except ConnectionRefusedError:
                      messages.error(request, "Problem sending reset password email, <b>MAIL SERVER CONNECTION ERROR</b>")

                except Exception:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('store')


    form = PasswordResetForm()
    context={'form':form}
    return render(request,'password_reset.html',context)





def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("store")





