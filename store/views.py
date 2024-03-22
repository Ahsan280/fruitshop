from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from orders.models import OrderedProduct
from .Forms import ReviewForm
from .models import Product, Variation, ReviewRating


# Create your views here.
def store(request):
    products=Product.objects.filter(is_available=True).order_by('created_at')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    return render(request, 'store/store.html', context={'products':paged_products,
                                                        'count':product_count})
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! your review has been submitted")
                return redirect(url)
def products_by_category(request, category_slug):
    products=Product.objects.filter(category__slug=category_slug)
    count=products.count()
    return render(request, 'store/store.html', context={'products':products,
                                                        'count':count})
def search(request):
    if request.method=="GET":
        search=request.GET['search']
        products = Product.objects.order_by('created_at').filter(
            Q(description__icontains=search) | Q(product_name__icontains=search))
        count = products.count()
        return render(request, 'store/store.html', context={'products':products,
                                                            'count':count})

def product_details(request, category_slug, product_slug):
    product=Product.objects.get(category__slug=category_slug, slug=product_slug)
    if request.user.is_authenticated:
        ordered_product=OrderedProduct.objects.filter(user=request.user, product=product).exists()
        print(ordered_product)
    else:
        ordered_product=None
    try:
        variation=Variation.objects.filter(product=product)
        variation_category_value={}
        for var in variation:
            if var.variation_category in variation_category_value:
                variation_category_value[var.variation_category].append(var.variation_value)
            else:
                variation_category_value[var.variation_category]=[var.variation_value]
        print(variation_category_value)
    except Variation.DoesNotExist:
        pass
    return render(request, 'store/product_details.html', context={'product':product,
                                                                  'variation_category_value':variation_category_value,
                                                                  'ordered_product':ordered_product})