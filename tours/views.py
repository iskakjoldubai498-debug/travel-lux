from django.shortcuts import render, get_object_or_404
from .models import Tour


# 1. БАШКЫ БЕТ (Издөө, Айлар жана Акыркы 6 тур)
def home(request):
    search_query = request.GET.get('search', '')
    month_query = request.GET.get('month', '')

    # Бардык турларды базадан алуу (жаңы кошулгандарын башында көрсөтүү)
    tours = Tour.objects.all().order_by('-created_at')

    # Аталышы боюнча издөө логикасы
    if search_query:
        tours = tours.filter(title__icontains=search_query)

    # Айлар боюнча издөө (Сүрөттөмөнүн ичинен издейт)
    if month_query and month_query != "Кайсы айда?":
        tours = tours.filter(description__icontains=month_query)

    context = {
        'tours': tours[:6],  # Башкы бетке 6 тур жетиштүү
        'search_query': search_query,
        'month_query': month_query,
    }
    return render(request, 'tours/home.html', context)


# 2. ТУРЛАР ТИЗМЕСИ (Категориялар боюнча фильтр)
def tours_list(request):
    category = request.GET.get('category')

    tours = Tour.objects.all().order_by('-created_at')

    if category:
        tours = tours.filter(category=category)

    return render(request, 'tours/tours_list.html', {'tours': tours})


# 3. ТУРДУН ТОЛУК МААЛЫМАТЫ (Деталдуу бет)
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    # Кошумча: Ушул эле категориядагы башка 3 турду сунуштоо
    related_tours = Tour.objects.filter(category=tour.category).exclude(pk=pk)[:3]

    context = {
        'tour': tour,
        'related_tours': related_tours,
        'whatsapp_number': '996553956070',  # Сиздин номериңиз
    }
    return render(request, 'tours/tour_detail.html', context)


# 4. БАЙЛАНЫШ БЕТИ
def contact_view(request):
    context = {
        'phone': '+996 553 956 070',
        'instagram': 'i_235_k',
        'whatsapp': '996553956070'
    }
    return render(request, 'tours/contact_page.html', context)


# 5. КОМПАНИЯ ЖӨНҮНДӨ (Details)
def details_page(request):
    return render(request, 'tours/details.html')
from django.shortcuts import render, get_object_or_404
from django.db import models  # МЫНА УШУЛ САПТЫ КОШУҢУЗ
from .models import Tour

def home(request):
    search_query = request.GET.get('search', '').strip()
    month_query = request.GET.get('month', '')

    tours = Tour.objects.all().order_by('-created_at')

    if search_query:
        # Эми models.Q ката бербейт
        tours = tours.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    if month_query and month_query != "Кайсы айда?":
        tours = tours.filter(month=month_query)

    context = {
        'tours': tours[:6],
        'search_query': search_query,
        'month_query': month_query,
    }
    return render(request, 'tours/home.html', context)