from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Product, PriceLink, Store


def index(request):
    all_products = Product.objects.all().order_by('-pageviews')[:4]
    context = {'all_products': all_products}
    return render(request, 'products/index.html', context)


def categorydetail(request, category):
    clickeditems = Product.objects.all().order_by('-pageviews')[:10]
    all_products = Product.objects.filter(mycategory=category)
    if all_products:
        all_products = all_products
    else:
        all_products = Product.objects.filter(realcategory=category)
        if all_products:
            all_products = all_products
        else:
            all_products = Product.objects.filter(subcategory=category)
    subcategories = {}
    for product in all_products:
        if product.mycategory not in subcategories:
            subcategories.update({product.mycategory: 1})
        else:
            subcategories[product.mycategory] += 1
        if product.subcategory not in subcategories:
            subcategories.update({product.subcategory: 1})
        else:
            subcategories[product.subcategory] += 1
        if product.realcategory not in subcategories:
            subcategories.update({product.realcategory: 1})
        else:
            subcategories[product.realcategory] += 1
    context = {'all_products': all_products,
               'subcategories': sorted(subcategories.items(), key=lambda item: item[1], reverse=True), 'clickeditems': clickeditems, 'MAINCATEGORY': category}
    return render(request, 'products/listallproducts.html', context)


def productdetail(request, rank, category):
    product = Product.objects.get(rank=rank, mycategory=category)
    relatedproducts =  Product.objects.filter(subcategory=product.subcategory)[:4]
    pricelinks = product.link.all()
    context = {'product': product, 'pricelinks': pricelinks, 'relatedproducts': relatedproducts}
    return render(request, 'products/oneproduct.html', context)


def addProduct(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        name = request.POST['name']
        short_name = request.POST['short_name']
        description = request.POST['description']
        short_description = request.POST['short_description']
        img_thumb = request.POST['img_thumb']
        img_full = request.POST['img_full']
        rank = request.POST['rank']
        mycategory = request.POST['mycategory']
        realcategory = request.POST['realcategory']
        subcategory = request.POST['subcategory']
        price = request.POST['price']
        url = request.POST['url']
        # check whether it's valid:
        full = Product(
            name=name,
            short_name=short_name,
            description=description,
            short_description=short_description,
            img_thumb=img_thumb,
            img_full=img_full,
            rank=rank,
            mycategory=mycategory,
            realcategory=realcategory,
            subcategory=subcategory
        )
        full.save()
        STORE = Store.objects.get(name="Amazon")
        sendpricelink = PriceLink(
        product=full,
        store=STORE,
        price=price,
        clicks=0,
        url=url
        )
        sendpricelink.save()
        return HttpResponse(f"{full}: {sendpricelink}")
        

    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponse('Something Went wrong')

