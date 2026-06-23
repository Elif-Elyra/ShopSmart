from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'apps.orders'
    def ready(self):
        # Jab app start ho, signals automatically register ho jaayein
        import apps.orders.signals
