from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'edc_action_item'
    verbose_name = 'Action Items'

    def ready(self):
        from .signals import action_on_post_delete
        pass
