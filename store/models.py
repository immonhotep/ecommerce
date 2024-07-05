from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from django.db.models import Avg,Count
from django.utils.text import slugify





class User(AbstractUser):


    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField( unique=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    
    
    
    def __str__(self):
        return self.username
    

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User,auto_now=True)
    address = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=200,blank=True)
    state = models.CharField(max_length=200,blank=True)
    zipcode = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{0,9}$')],null=True)
    country = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = ShippingAddress(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)



class Category(models.Model):

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200,blank=True)
    slug = models.SlugField(blank=True, unique=True)
    image= models.ImageField(null=True,blank=True,upload_to='uploads/category')
    

    class Meta:
        verbose_name_plural = 'Categories'
        ordering=('-title',)

    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
@receiver(pre_save, sender=Category)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    




class Product(models.Model):
    title= models.CharField(max_length=120)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=200,blank=True)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image= models.ImageField(null=True,blank=True,upload_to='uploads/products/')
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering=('-title',)

  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def averagerate(self):
        review = customer_rating.objects.filter(product=self).aggregate(avarage=Avg('star_rating'))
        avg=0
        if review["avarage"] is not None:
            avg=float(review["avarage"])
        return avg
    
    @property
    def countrate(self):
        reviews = customer_rating.objects.filter(product=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    
    @property
    def countreview(self):
        reviews = customer_review.objects.filter(product=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    
@receiver(pre_save, sender=Product)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    
   
    

class Orders(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{0,9}$')],null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    shipped = models.BooleanField(default=False)
    shipping_date = models.DateTimeField(auto_now_add=True)

  
    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ['-date_added']


    def __str__(self):
        return 'Order {}'.format(self.id)
    
    @property
    def get_total_cost(self):
        return sum(item.get_total for item in self.items.all() )
    
@receiver(pre_save, sender=Orders)
def set_shipped_data_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = timezone.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.shipping_date = now




class OrderItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    total = models.PositiveIntegerField(null=True,default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, null=True)
   

    def __str__(self):
        return '{}'.format(self.id)
    

    @property 
    def get_total(self):
        total = self.item.price  * self.quantity
        return total
    

 
    


class OrderItem_final(models.Model):
    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    total = models.PositiveIntegerField(null=True,default=0)

    
    def __str__(self):
        return '{}'.format(self.id)
    
    class Meta:

        ordering = ['-order']
    
   
    @property 
    def get_total(self):
        total = self.item.price  * self.quantity
        return total
    
    
class Payment_and_transport(models.Model):

    order=models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    payment_type=models.CharField(max_length=50, blank=True, null=True)
    transport_service = models.CharField(max_length=200, blank=True, null=True)
    trasport_price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return 'related - {}'.format(self.order)
    




class customer_question(models.Model):

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    user_info = models.TextField(max_length=1000, null=True)
    question_date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):

        return  self.email
    
    class Meta:
        ordering=['-question_date']
    

class customer_review(models.Model):

    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True , blank=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):

        return  f'comment to : {self.product.title}-@{self.user.username}'
    
    class Meta:
        ordering=['-comment_date']


class customer_rating(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True , blank=True, on_delete=models.CASCADE)
    star_rating = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return f'rating for {self.product.title}-@{self.user.username}'
    

    
