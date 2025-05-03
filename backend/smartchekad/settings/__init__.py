from decouple import config

env = config('DJANGO_ENV', default='dev')

if env == 'prod':
    from .prod import *
elif env == 'local':
    from .local import *
else:
    from .dev import *
