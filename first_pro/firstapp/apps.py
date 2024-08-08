from django.apps import AppConfig


class FirstappConfig(AppConfig):
    name = 'firstapp'
    def ready(self):
        import firstapp.signals
