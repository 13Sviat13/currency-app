from django.db import models


class Rate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExchangeRateProvider(models.Model):
    name = models.CharField(max_length=20)
    api_url = models.URLField()


class ExchangeRate(models.Model):
    base_currency = models.CharField(max_length=20)
    currency = models.CharField(max_length=20)

    date = models.DateTimeField(null=True)
    sale_rate = models.DecimalField(max_digits=10, decimal_places=4)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=4)

    provider = models.ForeignKey(ExchangeRateProvider, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.base_currency}//{self.currency}"


# Create your models here.
