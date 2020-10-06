import os
from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
# print(os.environ)
if os.environ['HOME'] == '/root':
   from .prod import *
else:
   from .dev import *



SECRET_KEY = os.environ.get('SECRET_KEY',os.urandom(32))