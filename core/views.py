from django.shortcuts import render


from currency.services import ExchangeRatesService


# Create your views here.
def index(request):
    service = ExchangeRatesService()
    rates = service.threadPool()

    print(rates)
    return render(request, 'currency/index.html')
