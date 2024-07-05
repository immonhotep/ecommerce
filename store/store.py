from .models import OrderItem
class Store():
    def __init__(self,request):
        self.session = request.session
        # if session  exist  get the session_key:
        store = self.session.get('session_key')
        # if not exist session create it :
        if 'session_key' not in request.session:
            store = self.session['session_key'] = {}


        if request.user.is_authenticated:
            user_cart = OrderItem.objects.filter(user=request.user,ordered=False)
            request.session['cart_num'] = len(user_cart)

        else:    
            try: 
                request.session['cart']
                request.session['cart_num'] = len(request.session['cart'])

            except:
                request.session['cart'] = {}
                request.session['cart_num'] = 0


        