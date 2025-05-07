from django.shortcuts import render
from .models import Kitap
from django.db.models import Avg
from datetime import datetime

def home(request):
    kitaplar = Kitap.objects.all()

    # Başlıkta arama
    title_query = request.GET.get('title')
    if title_query:
        kitaplar = kitaplar.filter(title__icontains=title_query)

    # İçerikte arama
    content_query = request.GET.get('content')
    if content_query:
        kitaplar = kitaplar.filter(content__icontains=content_query)

    # Fiyat aralığı filtresi
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        kitaplar = kitaplar.filter(price__gte=min_price)
    if max_price:
        kitaplar = kitaplar.filter(price__lte=max_price)

    # Tarih aralığı filtresi
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        kitaplar = kitaplar.filter(published_time__gte=start_date)
    if end_date:
        kitaplar = kitaplar.filter(published_time__lte=end_date)

    # Sıralama
    sort_by = request.GET.get('sort', '')
    if sort_by == 'title_asc':
        kitaplar = kitaplar.order_by('title')
    elif sort_by == 'title_desc':
        kitaplar = kitaplar.order_by('-title')
    elif sort_by == 'price_asc':
        kitaplar = kitaplar.order_by('price')
    elif sort_by == 'price_desc':
        kitaplar = kitaplar.order_by('-price')

    # Ortalama fiyat hesapla
    ortalama_fiyat = kitaplar.aggregate(Avg('price'))['price__avg']

    context = {
        'kitaplar': kitaplar,
        'ortalama_fiyat': ortalama_fiyat,
    }
    return render(request, 'kitaplar/home.html', context)
