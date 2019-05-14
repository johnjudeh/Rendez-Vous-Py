"""
Structure for separating settings for each environment.

The settings file is picked based on the environment variable `DJANGO_SETTINGS_MODULE`.

The base one is used for defaults or common settings across environments. Each environment
That requires more specific settings imports it and overrides what it requires.
"""