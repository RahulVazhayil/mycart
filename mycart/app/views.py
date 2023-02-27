from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart,Customer,Product,OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):
  totalitem =0
  topwears   =Product.objects.filter(category='TOPWEAR')
  bottomwears=Product.objects.filter(category='BOTTOMWEAR')
  mobiles    =Product.objects.filter(category='MOBILE')
  laptop     =Product.objects.filter(category='LAPTOP')
  watch      =Product.objects.filter(category='WATCH')
  headphone  =Product.objects.filter(category='HEADPHONE')
  shoes      =Product.objects.filter(category='SHOES')
  appliances =Product.objects.filter(category='APPLIANCE')





  if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,
                                         'mobiles':mobiles,'totalitem':totalitem,'laptop':laptop,'watch':watch,
                                         'headphone':headphone,'shoes':shoes,'appliances':appliances}
                )


class ProductDetailView(View):
 def get(self,request,pk):
  totalitem =0
  product=Product.objects.get(pk=pk)
  item_already_in_cart= False
  if request.user.is_authenticated:
   item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
   totalitem=len(Cart.objects.filter(user=request.user))

  return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required()
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product =Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart' )



@login_required()
def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart=Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount= 0.0
  total_amount = 0.0
  quantity=0
  totalitem =0
  cart_product =[p for p in Cart.objects.all() if p.user ==user]

  if request.user.is_authenticated:

   totalitem = len(Cart.objects.filter(user=request.user))

  if cart_product:
   for p in cart_product:
    tempamount      = (p.quantity * p.product.discount_price)
    quantity       += (p.quantity)
    tempshipamount  = (p.quantity * 100)
    shipping_amount += tempshipamount
    amount += tempamount
    total_amount    = amount + shipping_amount
    total_quantity  =quantity
   return render(request, 'app/addtocart.html',{'carts':cart,'total_amount':total_amount,'amount':amount,'shipping_amount':shipping_amount,'total_quantity':total_quantity,'tempamount':tempamount,'totalitem':totalitem})
  else:
   return render(request,'app/emptycart.html')


def plus_cart(request):
 if request.method =='GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  quantity=0

  shipping_amount = 0.0
  cart_product =[p for p in Cart.objects.all() if p.user ==request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   tempshipamount = (p.quantity *100)
   shipping_amount+=tempshipamount
   amount += tempamount
   quantity += (p.quantity)

  data={'quantity':c.quantity,'amount':amount,'totalamount':amount + shipping_amount,'shipping_amount':shipping_amount }
  return JsonResponse(data)


def minus_cart(request):
 if request.method =='GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 0.0
  cart_product =[p for p in Cart.objects.all() if p.user ==request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   tempshipamount = (p.quantity * 100)
   shipping_amount += tempshipamount
   amount += tempamount
  data={'quantity':c.quantity,'amount':amount,'totalamount':amount + shipping_amount}
  return JsonResponse(data)


def remove_cart(request):
 if request.method =='GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 0.0
  cart_product =[p for p in Cart.objects.all() if p.user ==request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   amount += tempamount
  data={'amount':amount,'totalamount':amount + shipping_amount }
  return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required()
def address(request):
 add =Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})


@login_required()
def orders(request):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 op =OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})



def mobile(request,data=None):
 totalitem=0
 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))
 if data==None:
  mobiles = Product.objects.filter(category='MOBILE')
 elif data=='APPLE' or data == 'SAMSUNG' or data == 'ONEPLUS':
  mobiles = Product.objects.filter(category='MOBILE').filter(brand=data)
 elif data=='below':
  mobiles = Product.objects.filter(category='MOBILE').filter(discount_price__lt=40000)
 elif data=='above':
  mobiles = Product.objects.filter(category='MOBILE').filter(discount_price__gt=40000)
 return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})


def topwear(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  topwear = Product.objects.filter(category='TOPWEAR')
 elif data=='LEE' or data == 'ALLENSOLLY' or data == 'LP':
  topwear = Product.objects.filter(category='TOPWEAR').filter(brand=data)
 elif data=='below':
  topwear = Product.objects.filter(category='TOPWEAR').filter(discount_price__lt=2000)
 elif data=='above':
  topwear = Product.objects.filter(category='TOPWEAR').filter(discount_price__gt=2000)
 return render(request, 'app/topwear.html',{'topwear':topwear,'totalitem':totalitem})


def bottomwear(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  bottomwear = Product.objects.filter(category='BOTTOMWEAR')
 elif data=='LEE' or data == 'ALLENSOLLY' or data == 'LP':
  bottomwear = Product.objects.filter(category='BOTTOMWEAR').filter(brand=data)
 elif data=='below':
  bottomwear = Product.objects.filter(category='BOTTOMWEAR').filter(discount_price__lt=2000)
 elif data=='above':
  bottomwear = Product.objects.filter(category='BOTTOMWEAR').filter(discount_price__gt=2000)
 return render(request, 'app/bottomwear.html',{'bottomwear':bottomwear,'totalitem':totalitem})


def laptop(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  laptop = Product.objects.filter(category='LAPTOP')
 elif data=='HP' or data == 'LENOVO' or data == 'APPLE' or data=='DELL' or data=='ACER' or data=='ASUS':
  laptop = Product.objects.filter(category='LAPTOP').filter(brand=data)
 elif data=='below':
  laptop = Product.objects.filter(category='LAPTOP').filter(discount_price__lt=60000)
 elif data=='above':
  laptop = Product.objects.filter(category='LAPTOP').filter(discount_price__gt=60000)
 return render(request, 'app/laptop.html',{'laptop':laptop,'totalitem':totalitem})


def watch(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  watch = Product.objects.filter(category='WATCH')
 elif data=='SAMSUNG' or data == 'APPLE' or data == 'ONEPLUS' or data=='NOISE' or data=='CASIO' :
  watch = Product.objects.filter(category='WATCH').filter(brand=data)
 elif data=='below':
  watch = Product.objects.filter(category='WATCH').filter(discount_price__lt=5000)
 elif data=='above':
  watch = Product.objects.filter(category='WATCH').filter(discount_price__gt=5000)
 return render(request, 'app/watch.html',{'watch':watch,'totalitem':totalitem})



def headphone(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  headphone = Product.objects.filter(category='HEADPHONE')
 elif data=='SAMSUNG' or data == 'APPLE' or data == 'ONEPLUS' or data=='NOISE'  :
  headphone = Product.objects.filter(category='HEADPHONE').filter(brand=data)
 elif data=='below':
  headphone = Product.objects.filter(category='HEADPHONE').filter(discount_price__lt=4000)
 elif data=='above':
  headphone = Product.objects.filter(category='HEADPHONE').filter(discount_price__gt=4000)
 return render(request, 'app/headphone.html',{'headphone':headphone,'totalitem':totalitem})


def shoes(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  shoes = Product.objects.filter(category='SHOES')
 elif data=='WOODLAND' or data == 'NIKE' or data == 'ADIDAS':
  shoes = Product.objects.filter(category='SHOES').filter(brand=data)
 elif data=='below':
  shoes = Product.objects.filter(category='SHOES').filter(discount_price__lt=4000)
 elif data=='above':
  shoes = Product.objects.filter(category='SHOES').filter(discount_price__gt=4000)
 return render(request, 'app/shoes.html',{'shoes':shoes,'totalitem':totalitem})


def appliances(request,data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
  appliances = Product.objects.filter(category='APPLIANCE')
 elif data=='REDMI' or data == 'LG' or data == 'SAMSUNG':
  appliances = Product.objects.filter(category='APPLIANCE').filter(brand=data)
 elif data=='below':
  appliances = Product.objects.filter(category='APPLIANCE').filter(discount_price__lt=50000)
 elif data=='above':
  appliances = Product.objects.filter(category='APPLIANCE').filter(discount_price__gt=50000)
 return render(request, 'app/appliances.html',{'appliances':appliances,'totalitem':totalitem})

class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',{'form':form})

 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'congratulations !! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

@login_required()
def checkout(request):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  user =request.user
  add=Customer.objects.filter(user=user)
  cart_item=Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 0.0
  totalamount =0.0
  cart_product =[p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discount_price)
    tempshipamount = (p.quantity * 100)
    shipping_amount += tempshipamount
    amount += tempamount
    total_amount=amount+shipping_amount
 return render(request, 'app/checkout.html', {'add': add,'total_amount':total_amount,'cart_item':cart_item,'shipping_amount':shipping_amount,'totalitem':totalitem})






@login_required()
def payment_done(request):
 user =request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart= Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect('orders')


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   user= request.user
   name= form.cleaned_data['name']
   locality= form.cleaned_data['locality']
   city= form.cleaned_data['city']
   state= form.cleaned_data['state']
   zipcode= form.cleaned_data['zipcode']
   reg =Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulations!! Profile Updated Successfully')
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})





def search(request):
 q=request.GET['q']
 data=Product.objects.filter(title__icontains=q).order_by('-id')
 if data:
  data==q
  return render(request,'app/search.html',{'data':data})
 else:
  return render(request,'app/emptysearch.html')








