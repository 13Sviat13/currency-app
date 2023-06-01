
from concurrent.futures import ThreadPoolExecutor

import requests
from datetime import date, timedelta, datetime

from django.utils import timezone

from currency.models import ExchangeRate, ExchangeRateProvider


class ExchangeRatesService:
    url = 'https://api.privatbank.ua/p24api/exchange_rates'
    CURRENCIES = ['GBP', 'USD', 'CHF', 'EUR']

    def get_rates(self):

        start_date = date(date.today().year, 1, 1)
        end_date = date.today()

        delta = timedelta(days=1)
        current_date = start_date

        provider = ExchangeRateProvider.objects.create(name='PrivatBank', api_url=self.url)

        while current_date <= end_date:
            params = {
                "date": current_date.strftime('%d.%m.%Y')
            }

            response = requests.get(self.url, params=params)
            data = response.json()

            rates = data.get('exchangeRate')
            base_currency = data.get('baseCurrencyLit')

            aware_date = timezone.make_aware(datetime.combine(current_date, datetime.min.time()),
                                             timezone.get_current_timezone())

            if rates:
                for r in rates:
                    if r.get('currency') not in self.CURRENCIES:
                        continue

                    ExchangeRate.objects.update_or_create(
                        base_currency=base_currency,
                        currency=r['currency'],
                        date=aware_date,
                        sale_rate=r.get('saleRate', 0),
                        buy_rate=r.get('purchaseRate', 0),
                        provider=provider
                    )

            current_date += delta

    def ThreadPool(self):
        with ThreadPoolExecutor(max_workers=10) as pool:
            res = pool.submit(self.get_rates)
        return res.result()
