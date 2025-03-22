from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from django.conf import settings

class DailyStock(models.Model):
    id = models.CharField(primary_key=True, max_length=21, editable=False)
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open = models.CharField(max_length=18)
    high = models.CharField(max_length=18)
    low = models.CharField(max_length=18)
    close = models.CharField(max_length=18)
    volume = models.PositiveIntegerField()

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        # Generate ID for new records
        if not self.id:
            self.id = f"{self.symbol}-{self.date.strftime('%Y-%m-%d')}"
        # Prevent changing symbol/date for existing records
        else:
            existing = StockRecord.objects.get(pk=self.id)
            if existing.symbol != self.symbol or existing.date != self.date:
                raise ValidationError("Cannot modify symbol or date for existing records")
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - Open: {self.open}, Close: {self.close}"

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('stock-day-price', args=[str(self.id)])

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class UserStock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'stock')

    def __str__(self):
        return f"{self.user.username} tracks {self.stock.symbol}"
