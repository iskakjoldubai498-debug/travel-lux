from django.contrib import admin
from .models import Tour, TourImage


# Сүрөттөрдү турдун ичинде дароо кошуу үчүн (Inline)
class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1  # Жаңы тур кошуп жатканда бош сүрөт кошуу үчүн 1 кутуча чыгарат
    verbose_name = "Турдун кошумча сүрөтү"
    verbose_name_plural = "Турдун кошумча сүрөттөрү"


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    # Админканын башкы тизмесинде көрүнүүчү маалыматтар
    list_display = ('title', 'category', 'month', 'price', 'created_at')

    # Оң тараптагы чыпкалоо (фильтр) блогу
    list_filter = ('category', 'month', 'created_at')

    # Текст аркылуу издөө (Аталышы жана Сүрөттөмөсү боюнча)
    search_fields = ('title', 'description')

    # Турду түзүп жатканда сүрөттөрдү дароо кошуу
    inlines = [TourImageInline]

    # Админкада иреттөө (жаңылары башында)
    ordering = ('-created_at',)


# TourImage моделин өзүнчө да көрүү үчүн (кааласаңыз)
@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ('tour', 'image', 'caption')