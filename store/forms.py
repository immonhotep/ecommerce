from django import forms
from .models import User, Orders, ShippingAddress,Payment_and_transport,customer_question,Category,Product,customer_review

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model




class UpdateUserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('first_name','last_name','email','phone_number')


class ShippingForm(forms.ModelForm):
    class Meta:   
        model = ShippingAddress
        fields = ('address','city','state','zipcode','country')

    address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Enter Address 2',
    'class': 'form-control '}),required=True)

    city = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Enter City',
    'class': 'form-control '}),required=True)

    state = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'state',
    'class': 'form-control '}),required=True)

    zipcode = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Enter Zipcode',
    'class': 'form-control '}),required=True)

    country = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Enter Country',
    'class': 'form-control '}),required=True)


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
    username = forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control form-control-lg','placeholder':'Username or Email'}),
    label="Username or Email")
        
    password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control form-control-lg', 'placeholder':'Password'}))






class SignupForm(UserCreationForm):
        class Meta:
            model = User
            fields = ('username','email','password1','password2')


        def __init__(self, *args, **kwargs):
            super(SignupForm, self).__init__(*args, **kwargs)
            self.fields['password1'].label = "Password"
            self.fields['password2'].label = "Password confirm"


        username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control'}))

        email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email Address',
        'class': 'form-control'}))

        password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': 'form-control'}))

        password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Your Password',
        'class': 'form-control'}))
        

class UpdateOrdersFormCustomer(forms.ModelForm):

    class Meta:

        model= Orders

        fields = ('city','address','zipcode')



class UpdateOrdersFormGuest(forms.ModelForm):

    class Meta:

        model= Orders

        fields = ('city','state','country','address','zipcode','first_name','last_name','email','phone_number')


class ChangeUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')



    def __init__(self, *args, **kwargs):
            super(ChangeUserPasswordForm, self).__init__(*args, **kwargs)
            self.fields['new_password1'].label = "New password"
            self.fields['new_password2'].label = "New Password confirm"

    

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your previous Password',
        'class': 'form-control'}))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New password',
        'class': 'form-control'}))     

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat New Password',
        'class': 'form-control'}))




class  Shipping_checkForm(forms.ModelForm):

    class Meta:
        model = Orders 
        fields=('shipped',)


        shipped = forms.BooleanField(label='Shipping')



class payment_and_transportForm(forms.ModelForm):

    class Meta:
        model = Payment_and_transport
        fields=('payment_type','transport_service')

    payment_choices=[
        ('Cash on Delivery','Cash on Delivery'),
        ('Card on Delivery','Card on Delivery'),
    ]

    transport_choices = [
        ('GLS Transport service','GLS Transport service: 2500 HUF '),
        ('Post Transport service','Post Transport service : 1900 HUF'),
    ]


    payment_type = forms.ChoiceField(
        
        choices=payment_choices,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
        })


    )


    transport_service= forms.ChoiceField(
        
        choices=transport_choices,
        widget=forms.Select(attrs={

            'class':'form-select form-control fw-bolder'
        })


    )



class QuestionForm(forms.ModelForm):
        
        class Meta: 
            model = customer_question
            fields = ('first_name','last_name','email','user_info')


        first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First name',
        'class': 'form-control'}),required=True)
        
        last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last name',
        'class': 'form-control'}),required=True)

        email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email Address',
        'class': 'form-control'}),required=True)

        user_info = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your Question',
        'class': 'form-control'}),required=True)
        


class Add_category_Form(forms.ModelForm):
     
     class Meta:
          model = Category
          fields = ('title','subtitle','image')

          image = forms.ImageField()


     title = forms.CharField(widget=forms.TextInput(attrs={
     'placeholder': 'Title',
     'class': 'form-control'}),required=True)

     subtitle = forms.CharField(widget=forms.TextInput(attrs={
     'placeholder': 'Subtitle',
     'class': 'form-control'}),required=True)




class Add_product_Form(forms.ModelForm):
     
     class Meta:
          model = Product
          fields = ('title','category','subtitle','description','price','image')


     title = forms.CharField(widget=forms.TextInput(attrs={
     'placeholder': 'Title',
     'class': 'form-control'}),required=True)

     category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={
          'class':'form-select form-control fw-bolder'
     }),required=True)

     subtitle = forms.CharField(widget=forms.TextInput(attrs={
     'placeholder': 'subtitle',
     'class': 'form-control'}),required=True)

     description = forms.CharField(widget=forms.Textarea(attrs={
       'placeholder':'Description',  
       'class':'form-control' 
     }),required=True)

     price = forms.CharField(widget=forms.NumberInput(attrs={
     'placeholder': '0',
     'class': 'form-control'}),required=True)





class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
            super(SetPasswordForm, self).__init__(*args, **kwargs)
            self.fields['new_password1'].label = "Password"
            self.fields['new_password2'].label = "Password confirm"

    

    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={
      'Placeholder': 'Enter Password',
      'class' :' form-control' 

    }))

    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={
      'Placeholder': 'Repeat Password',
      'class' :'form-control'    

    }))




class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.EmailInput(attrs={
    'placeholder': 'Your Email Address',
    'class': 'form-control'}))


