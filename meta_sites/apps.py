import sys

from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.management.color import color_style
from django.db.models.signals import post_migrate
from meta_sites import meta_sites, fqdn

style = color_style()


def post_migrate_update_sites(sender=None, **kwargs):
    from edc_sites.utils import add_or_update_django_sites

    sys.stdout.write(style.MIGRATE_HEADING("Updating sites:\n"))
    add_or_update_django_sites(
        apps=django_apps, sites=meta_sites, fqdn=fqdn, verbose=True
    )
    sys.stdout.write("Done.\n")
    sys.stdout.flush()


class AppConfig(DjangoAppConfig):
    name = "meta_sites"

    def ready(self):
        post_migrate.connect(post_migrate_update_sites, sender=self)
