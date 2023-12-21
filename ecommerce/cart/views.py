from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Account,Order

# Create your views here.
def cartview(request):
    u=request.user
    total=0
    try:
        cart=Cart.objects.filter(user=u)
        for i in cart:
            total=i.quantity*i.product.price+total
    except:
        pass
    return render(request,'cart.html',{'c':cart,'total':total})
@login_required
def addtocart(request,p):
    d=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=d)
        if(cart.quantity<cart.product.stock):
          cart.quantity+=1
        cart.save()
    except:
        cart=Cart.objects.create(product=d,user=u,quantity=1)
        cart.save()
    return redirect('cart:cartview')
@login_required
def minusquantity(request,p):
    d = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=d)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cartview')
def deletequantity(request,p):
    d = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=d)

        cart.delete()
    except:
        pass
    return redirect('cart:cartview')
def orderform(request):
    if (request.method == "POST"):
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['ac']
        u=request.user
        cart=Cart.objects.filter(user=u)

#accntil ninu place order kodukumbo money kureyn
        total=0
        for i in cart:
            total=i.quantity*i.product.price+total
# check whether user has sufficient amount or not
        ac=Account.objects.get(accntno=n)
        if(ac.amount>=total):
            ac.amount=ac.amount-total
            ac.save()

            for i in cart:#creates record in order table for each objects in cart table for the current user
                o=Order.objects.create(user=u,product=i.product,adress=a,phone=p,noofitems=i.quantity,order_status="paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity#product tableil ninu count kurayan naml order cheyta sadanatintai
                i.product.save()
            cart.delete()#clears the cart items from the current user
            msg="Order Placed Succesfully"
            return render(request,'orderdetail1.html',{'m':msg})
        else:
            msg="Insuffucient Amount In User Account. You Cannot Place Order"
            return render(request, 'orderdetail2.html', {'m': msg})
    return render(request,'order.html')
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o})
