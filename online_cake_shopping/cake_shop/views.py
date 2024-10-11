from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.views import View


from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetails

from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
def home(request):
    products = None
    totalitem = 0

    if request.session.has_key('password'):
        password = request.session['password']
        customer = Customer.objects.filter(password=password)

        # Check if the customer with the given password exists
        if customer.exists():
            # Assuming phno is a field in your Customer model
            phno = customer[0].phno

            # Rest of your code
            category = Category.get_all_categories()
            totalitem = len(Cart.objects.filter(phno=phno))

            for c in customer:
                name = c.name
                categoryID = request.GET.get('category')

                if categoryID:
                    products = Product.get_all_product_by_category_id(categoryID)
                else:
                    products = Product.get_all_products()

                data = {
                    'name': name,
                    'product': products,
                    'category': category,
                    'totalitem': totalitem
                }
                return render(request, 'home.html', data)
        else:
            return redirect('login')
    else:
        return redirect('login')



def shop(request):
    products = None
    category = Category.get_all_categories()

    categoryID =request.GET.get('category')
    if categoryID:
        products =Product.get_all_product_by_category_id(categoryID)

    else:
        products = Product.get_all_products()

    data = {}
    data['product'] = products
    data['category'] = category
    print('you are ',request.session.get('password'))
    return render(request,'shop.html',data)


class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        postData = request.POST
        name = postData.get('name')
        email = postData.get('email')
        password = postData.get('password')
        phno = postData.get('phno')


        customer =Customer(name=name,
                           email=email,
                           password=password,
                           phno=phno)
        
        customer.register()
        
        return HttpResponse("Signup success")




    
class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        password = request.POST.get('password')
        error_message = None
        value = {
            'password': password
        }
        
        customer = Customer.objects.filter(password=password)

        if customer:
            phno = customer[0].phno 
            request.session['password'] = password
            request.session['phno'] = phno
            return redirect('homepage')
        else:
            error_message = "Password is Invalid !!"
            data = {
                'error': error_message,
                'value': value
            }

        return render(request, 'login.html', data)
    





def productdetail(request,pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.session.has_key('phno'):
        phno = request.session['phno']
        totalitem = len(Cart.objects.filter(phno=phno))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(phno=phno)).exists()
        customer = Customer.objects.filter(phno=phno)
        for c in customer:
            name=c.name

        data = {
            'product': product,
            'item_already_in_cart' : item_already_in_cart,
            'name' : name,
            'totalitem' : totalitem
        }
        return render(request,'productdetail.html', data)


def logout(request):
    if request.session.has_key('password'):
        del request.session['password']
        return redirect('login')
    else:
        return redirect('login')
    



def add_to_cart(request):
    if 'phno' in request.session:
        phno = request.session['phno']
        product_id = request.GET.get('prod_id')
        product_name = Product.objects.get(id=product_id)
        product = Product.objects.filter(id=product_id)

        for p in product:
            image = p.image
            price = p.price
            Cart(phno=phno, product=product_name, image=image, price=price).save()
        
        return redirect('homepage')
    else:

        return HttpResponse("User not authenticated")
    


def show_cart(request):
    totalitem = 0
    if request.session.has_key('phno'):
        phno = request.session['phno']
        totalitem = len(Cart.objects.filter(phno=phno))
        
        customer = Customer.objects.filter(phno=phno)
        for c in customer:
            name=c.name

            cart =  Cart.objects.filter(phno=phno)
            data ={
                'name' : name,
                'totalitem' : totalitem,
                'cart' : cart

            }
            if cart:
                return render(request,'show_cart.html',data)
            else:
                return render(request,'empty_cart.html')

def cart_close(request):
    if request.session.has_key('phno'):
        phno = request.session["phno"]
        product_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(phno=phno))
        cart.delete()
        return JsonResponse({'status': 'success'})
    

def checkout(request):
    totalitem = 0
    if request.session.has_key('phno'):
        phno = request.session["phno"]
        fname =request.POST.get('fname')
        lname =request.POST.get('lname')
        address =request.POST.get('address')
        city =request.POST.get('city')
        place =request.POST.get('place')
        pin =request.POST.get('pin')
        mobile =request.POST.get('mobile')
        email =request.POST.get('email')

        cart_product = Cart.objects.filter(phno=phno)
        for c in cart_product:
            qty = c.quantity
            price = c.price
            product_name = c.product
            image = c.image

            OrderDetails(user=phno,product_name=product_name,image=image,qty=qty,price=price).save()
            cart_product.delete()

            totalitem = len(Cart.objects.filter(phno=phno))

            customer = Customer.objects.filter(phno=phno)

            for c in customer:
                name = c.name 
                data = {
                    'name' : name,
                    'totalitem' : totalitem
                }
            return render(request,'empty_cart.html',data)
        
    else:
        return redirect('login.html')


def check_out(request):
    return render(request,'check_out.html')


def order(request):
    totalitem = 0
    if request.session.has_key('phno'):
        phno = request.session["phno"]
        totalitem = len(Cart.objects.filter(phno=phno))
        customer = Customer.objects.filter(phno=phno)

        for c in customer:
            name = c.name 
            order = OrderDetails.objects.filter(user=phno)

            data = {
            'order' : order,
            'name' : name,
            'totalitem' : totalitem
        }
        
        
        if order:
            return render(request,'order.html',data)
        else:
            return redirect('emptyorder.html',data) 
    else:
        return redirect('login.html')
    
def about(request):
    return render(request,'about.html')


        
        
    
        
    




