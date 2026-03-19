import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib import messages
from .models import Tour, Order  # Category импортун алып салдык

# 1. БАШКЫ БЕТ
def home(request):
    search_query = request.GET.get('search', '').strip()
    month_query = request.GET.get('month', '')
    tours = Tour.objects.all().order_by('-created_at')

    if search_query:
        tours = tours.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    if month_query and month_query != "Кайсы айда?":
        tours = tours.filter(month=month_query)

    context = {'tours': tours[:6]}
    return render(request, 'tours/home.html', context)

# 2. ТУРЛАР ТИЗМЕСИ
def tours_list(request):
    category = request.GET.get('category')
    tours = Tour.objects.all().order_by('-created_at')
    if category:
        tours = tours.filter(category=category)
    return render(request, 'tours/tours_list.html', {'tours': tours})

# 3. ТУРДУН ТОЛУК МААЛЫМАТЫ
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    # related_tours үчүн категория керек, эгер ката берсе муну өчүрүп койсоң болот
    related_tours = Tour.objects.filter(category=tour.category).exclude(pk=pk)[:3]
    return render(request, 'tours/tour_detail.html', {'tour': tour, 'related_tours': related_tours})

# 4. БАЙЛАНЫШ
def contact_view(request):
    return render(request, 'tours/contact_page.html')

# 5. ДЕТАЛДАР
def details_page(request):
    return render(request, 'tours/details.html')

# 6. ТЕЛЕГРАМГА ЗАКАЗ
def create_order(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', 'Белгисиз')
        phone_number = request.POST.get('phone_number', 'Номери жок')
        service_name = request.POST.get('service_name', 'Тез заказ')

        try:
            Order.objects.create(full_name=full_name, phone_number=phone_number, service_name=service_name)
        except: pass

        TOKEN = "8632706293:AAGUFr-eBHri8U9BLUZ_5j19g9flYnmngqw"
        CHAT_ID = "6365816184"
        message = f"🚀 <b>ЖАҢЫ ЗАКАЗ!</b>\n\n👤 <b>Кардар:</b> {full_name}\n📞 <b>Тел:</b> {phone_number}\n🌍 <b>Кызмат:</b> {service_name}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
            messages.success(request, "Рахмат! Билдирүү кабыл алынды.")
        except:
            messages.error(request, "Тармак катасы.")

        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')