from django.contrib.staticfiles.storage import ManifestStaticFilesStorage as DjangoManifestStaticFilesStorage

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
            (r"""(['"]\s*(/static/[^"']*?\.(?:js|png))["'])""", "'%s'"),
        )),
        ('*.json', (
            (r"""("\s*(/static/[^"]*?\.(?:js|png))")""", '"%s"'),
        )),
    )
