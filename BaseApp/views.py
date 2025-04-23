from django.shortcuts import render
from Sellers.models import ProductModel
# Create your views here.
def home_view(request):
     context  = {
          'products': ProductModel.objects.all()
     }
     return render(request, 'Public/Home/index.html' , context )