from importlib import import_module

import django
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models import signals

import admincommand


def sync_db_callback(verbosity=0, interactive=False, signal=None, **kwargs):
    """
    Callback for post_syncdb signal that installs the Permissions necessary
    to use the app. This needs to be done manually because the app doesn't
    expose any concrete models.
    """

    for app_module_path in settings.INSTALLED_APPS:
        try:
            admin_commands_path = "%s.admincommands" % app_module_path
            import_module(admin_commands_path)
        except ImportError:
            pass
    ct = ContentType.objects.get(model="admincommand", app_label="admincommand")
    for subclass in admincommand.models.AdminCommand.__subclasses__():
        codename = subclass.permission_codename()
        perm, created = Permission.objects.get_or_create(
            codename=codename, content_type=ct, name="Can run %s" % subclass.command_name()
        )


if django.VERSION >= (1, 7):
    signals.post_migrate.connect(sync_db_callback, sender=admincommand.models)
else:
    signals.post_syncdb.connect(sync_db_callback, sender=admincommand.models)
