DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kabu',
        'USER': 'dbuser',  # budokai#dbuser
        'PASSWORD': 'dbpass',  # budokai#dbpass
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

DEBUG = False