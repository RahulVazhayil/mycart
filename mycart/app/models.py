from django.db import models
from django.contrib.auth.models import User
from  django.core.validators import MaxLengthValidator,MinValueValidator

# Create your models here.
STATE_CHOICES=(
('AndhraPradesh','AndhraPradesh'  ),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttarakhand','Uttarakhand'),
('Uttar Pradesh','Uttar Pradesh'),
('West Bengal','West Bengal'),
)
class Customer(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=250)
    locality= models.CharField(max_length=250)
    city= models.CharField(max_length=50)
    zipcode= models.IntegerField()
    state= models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('MOBILE','MOBILE'),
    ('LAPTOP','LAPTOP'),
    ('TOPWEAR', 'TOPWEAR'),
    ('BOTTOMWEAR','BOTTOMWEAR'),
    ('SHOES', 'SHOES'),
    ('WATCH', 'WATCH'),
    ('HEADPHONE', 'HEADPHONE'),
    ('APPLIANCE', 'APPLIANCE '),

)
BRAND_CHOICES=(
    ('LEE','LEE'),
    ('ALLENSOLLY','ALLENSOLLY'),
    ('APPLE', 'APPLE'),
    ('SAMSUNG','SAMSUNG'),
    ('REDMI','REDMI'),
    ('ASUS', 'ASUS'),
    ('DELL', 'DELL'),
    ('ACER', 'ACER'),
    ('ONEPLUS', 'ONEPLUS'),
    ('LG', 'LG'),
    ('LENOVO', 'LENOVO'),
    ('NOKIA', 'NOKIA'),
    ('MOTOROLA', 'MOTOROLA'),
    ('REALME', 'REALME'),
    ('WOODLAND','WOODLAND'),
    ('W','W'),
    ('JOCKEY','JOCKEY'),
    ('WILDCRAFT','WILDCRAFT'),
    ('HP','HP'),
    ('LP','LP'),
    ('CASIO','CASIO'),
    ('ADIDAS','ADIDAS'),
    ('NIKE','NIKE'),
    ('IFB','IFB'),
    ('WHIRLPOOL','WHIRLPOOL'),
    ('NOISE','NOISE'),

)


class Product(models.Model):

    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand=models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    brand=models.CharField(choices=BRAND_CHOICES,max_length=15)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('packed','packed'),
    ('onthe_way','on_the_way'),
    ('delivered','delivered'),
    ('cancel','cancel')
)



class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50, choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
      return self.quantity * self.product.discount_price

