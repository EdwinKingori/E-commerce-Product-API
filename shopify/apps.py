from django.apps import AppConfig


class ShopifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopify'

    def ready(self):
        import shopify.signals
