from django.db import models
from cloudinary.models import CloudinaryField

class Tour(models.Model):
    # Категорияларды тандоо
    CATEGORY_CHOICES = [
        ('mountain', 'Тоо турлары'),
        ('horse', 'Атчан жүрүү'),
        ('vip', 'VIP Экспедиция'),
    ]

    # Издөө системасы үчүн айларды тандоо
    MONTH_CHOICES = [
        ('Март', 'Март'),
        ('Апрель', 'Апрель'),
        ('Май', 'Май'),
        ('Июнь', 'Июнь'),
        ('Июль', 'Июль'),
        ('Август', 'Август'),
        ('Сентябрь', 'Сентябрь'),
        ('Октябрь', 'Октябрь'),
    ]

    title = models.CharField(max_length=200, verbose_name="Турдун аталышы")
    description = models.TextField(verbose_name="Сүрөттөмөсү")
    price = models.IntegerField(verbose_name="Баасы (сом)")
    duration = models.CharField(max_length=100, verbose_name="Мөөнөтү")

    # Сүрөт (Cloudinary аркылуу)
    image = CloudinaryField('Башкы сүрөт')

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='mountain',
        verbose_name="Категория"
    )

    month = models.CharField(
        max_length=20,
        choices=MONTH_CHOICES,
        null=True,
        blank=True,
        verbose_name="Кайсы айга таандык?"
    )

    # ЖАҢЫ ТАЛААЛАР: Программа жана баага киргендер
    program = models.TextField(
        verbose_name="Турдун программасы",
        help_text="Ар бир күндү жаңы саптан жазыңыз (мисалы: 1-күн: Тосуп алуу)",
        blank=True, null=True
    )
    included = models.TextField(
        verbose_name="Баага эмнелер кирет?",
        help_text="Ар бир кызматты жаңы саптан жазыңыз",
        blank=True, null=True
    )
    not_included = models.TextField(
        verbose_name="Баага эмнелер кирбейт?",
        help_text="Ар бир пунктту жаңы саптан жазыңыз",
        blank=True, null=True
    )

    map_embed = models.TextField(blank=True, null=True, verbose_name="Карта (iframe)")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Турлар"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('Кошумча сүрөт')
    caption = models.CharField(max_length=200, blank=True, verbose_name="Сүрөт маалыматы")

    class Meta:
        verbose_name = "Турдун сүрөтү"
        verbose_name_plural = "Турдун сүрөттөрү"

    def __str__(self):
        return f"{self.tour.title} - Сүрөт"


# ЗАКАЗДАР ҮЧҮН МОДЕЛЬ (Өзүнчө класс, солго такалып жазылды)
class Order(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Кардардын аты")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон номери")
    service_name = models.CharField(max_length=255, default="Тез заказ", verbose_name="Кызмат")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Убактысы")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказдар"

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"