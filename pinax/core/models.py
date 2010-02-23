from django.conf import settings
from django.db.models.signals import post_syncdb
from django.contrib.sites.models import Site

def site_name_handler(created_models, **kwargs):
    if Site in created_models:
        try:
            site = Site.objects.get_current()
        except Site.DoesNotExist:
            return
        if hasattr(settings, 'SITE_NAME'):
            if site.name == settings.SITE_NAME:
                # If the name is already set, dont re-save it again
                return
            site.name = settings.SITE_NAME
        if hasattr(settings, 'SITE_DOMAIN'):
            site.domain = settings.SITE_DOMAIN
        site.save()
        
post_syncdb.connect(site_name_handler)