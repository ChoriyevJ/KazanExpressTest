from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="gncLEwgkQqcV9WlCfUlA6untV45E5mioC0ApwMBGgRNmgv2Hnnhrnjs4sMEbcfWT",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa: F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER", default="no") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa: F405
# Celery
# ------------------------------------------------------------------------------

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa
    }
}


# JAZZMIN_SETTINGS = {
#     # title of the window (Will default to current_admin_site.site_title if absent or None)
#     "site_title": "Library Admin",
#
#     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_header": "Library",
#
#     # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_brand": "Library",
#
#     # Logo to use for your site, must be present in static files, used for brand on top left
#     "site_logo": "books/img/logo.png",
#
#     # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
#     "login_logo": None,
#
#     # Logo to use for login form in dark themes (defaults to login_logo)
#     "login_logo_dark": None,
#
#     # CSS classes that are applied to the logo above
#     "site_logo_classes": "img-circle",
#
#     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
#     "site_icon": None,
#
#     # Welcome text on the login screen
#     "welcome_sign": "Welcome to the library",
#
#     # Copyright on the footer
#     "copyright": "Acme Library Ltd",
#
#     # List of model admins to search from the search bar, search bar omitted if excluded
#     # If you want to use a single search field you dont need to use a list, you can use a simple string
#     "search_model": ["auth.User", "auth.Group"],
#
#     # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
#     "user_avatar": None,
#
#     ############
#     # Top Menu #
#     ############
#
#     # Links to put along the top menu
#     "topmenu_links": [
#
#         # Url that gets reversed (Permissions can be added)
#         {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
#
#         # external url that opens in a new window (Permissions can be added)
#         {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
#
#         # model admin to link to (Permissions checked against model)
#         {"model": "auth.User"},
#
#         # App with dropdown menu to all its models pages (Permissions checked against models)
#         {"app": "books"},
#     ],
#
#     #############
#     # User Menu #
#     #############
#
#     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
#     "usermenu_links": [
#         {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
#         {"model": "auth.user"}
#     ],
#
#     #############
#     # Side Menu #
#     #############
#
#     # Whether to display the side menu
#     "show_sidebar": True,
#
#     # Whether to aut expand the menu
#     "navigation_expanded": True,
#
#     # Hide these apps when generating side menu e.g (auth)
#     "hide_apps": [],
#
#     # Hide these models when generating side menu (e.g auth.user)
#     "hide_models": [],
#
#     # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
#     "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
#
#     # Custom links to append to app groups, keyed on app name
#     "custom_links": {
#         "books": [{
#             "name": "Make Messages",
#             "url": "make_messages",
#             "icon": "fas fa-comments",
#             "permissions": ["books.view_book"]
#         }]
#     },
#
#     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
#     # for the full list of 5.13.0 free icon classes
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "auth.Group": "fas fa-users",
#     },
#     # Icons that are used when one is not manually specified
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-circle",
#
#     #################
#     # Related Modal #
#     #################
#     # Use modals instead of popups
#     "related_modal_active": False,
#
#     #############
#     # UI Tweaks #
#     #############
#     # Relative paths to custom CSS/JS scripts (must be present in static files)
#     "custom_css": None,
#     "custom_js": None,
#     # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
#     "use_google_fonts_cdn": True,
#     # Whether to show the UI customizer on the sidebar
#     "show_ui_builder": False,
#
#     ###############
#     # Change view #
#     ###############
#     # Render out the change view as a single form, or in tabs, current options are
#     # - single
#     # - horizontal_tabs (default)
#     # - vertical_tabs
#     # - collapsible
#     # - carousel
#     "changeform_format": "horizontal_tabs",
#     # override change forms on a per modeladmin basis
#     "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
#     # Add a language dropdown into the admin
#     "language_chooser": True,
# }
