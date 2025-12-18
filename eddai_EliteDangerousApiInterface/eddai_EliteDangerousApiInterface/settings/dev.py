from .default import *

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]

# Configurazione per dev container
INTERNAL_IPS = [
    "127.0.0.1",
]

# Configurazione debug toolbar per risolvere problemi JSON
DEBUG_TOOLBAR_CONFIG = {
    "RENDER_PANELS": True,
}