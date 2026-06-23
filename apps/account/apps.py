from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.account'
    
    def ready(self):
        # Jab app start ho, signals automatically register ho jaayein
        import apps.account.signals
