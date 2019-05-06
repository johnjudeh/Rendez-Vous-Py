from django.contrib.staticfiles.storage import ManifestStaticFilesStorage as DjangoManifestStaticFilesStorage

from django.conf import settings
from django.apps import apps
import os
import subprocess

class ManifestStaticFilesStorage(DjangoManifestStaticFilesStorage):
    """
    A static file system storage backend which also saves
    hashed copies of the files it saves.

    The storage also handles replacing paths declared in static
    files with the hashed names of those paths. It specifies how to
    find these paths in the patterns attributed. This overrides
    the patterns attribute found in HashedFilesMixin class which
    this class inherits from.

    In js files, it looks for patterns like:
    '/static/.../<>.png' and  '/static/.../<>.js'

    In json files, it looks for patterns like:
    "/static/.../<>.png" and  "/static/.../<>.js"
    """

    patterns = (
        ('*.css', (
            r"""(url\(['"]{0,1}\s*(.*?)["']{0,1}\))""",
            (r"""(@import\s*["']\s*(.*?)["'])""", """@import url("%s")"""),
        )),
        ('*.js', (
            (f"""(['"]\\s*({settings.STATIC_URL}[^"']*?\\.(?:js|png))["'])""", "'%s'"),
        )),
        ('*.json', (
            (f"""("\\s*({settings.STATIC_URL}[^"]*?\\.(?:js|png))")""", '"%s"'),
        )),
    )

    def post_process(self, *args, **kwargs):
        # Run ManifestStaticFilesStorage's post_process
        yield from super().post_process(*args, **kwargs)

        # Pulls appropriate command from settings and splits into arguments for running in the shell
        command = settings.GULP_COMMAND_DEV if settings.DEBUG else settings.GULP_COMMAND_PROD
        gulp_cli_args = command.split(' ')

        # Creates a colon-separated string to store in environment variable
        installed_apps = [app.label for app in apps.get_app_configs()]
        installed_apps += ['rendezvous']
        installed_apps = str.join(':', installed_apps)

        # Run gulp task passing it the appropriate environment variables
        os.environ['STATIC_ROOT'] = os.path.basename(settings.STATIC_ROOT)
        os.environ['RENDEZVOUS_APPS'] = installed_apps
        # TODO: Make sure this works with the build process
        subprocess.run(gulp_cli_args, check=True)
        del os.environ['STATIC_ROOT']
        del os.environ['RENDEZVOUS_APPS']
