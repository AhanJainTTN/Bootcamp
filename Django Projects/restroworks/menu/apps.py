from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "menu"

    # ensures that signals are registered when the application starts
    def ready(self):
        import menu.signals


# why def ready()
# Django does not automatically discover signals. The signals.py file needs to be manually imported to register signal handlers. When Django initializes the application, it calls ready(). Importing menu.signals inside ready() triggers signal registration.
