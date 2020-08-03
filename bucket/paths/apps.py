from django.apps import AppConfig


class PathsConfig(AppConfig):
    name = 'paths'

    def ready(self):
        import paths.signals  # noqa
