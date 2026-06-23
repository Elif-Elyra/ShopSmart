"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""


    
    """
    os => is the python library
     
    get_asgi_application => django function 
    
    os.environ => is a list of system setting 
    
    DJANGO_SETTINGS_MODULE => aik environment variable hai jo Django ko yeh batati hai ke aapke project ki sari configurations (settings) kis file mein pari hain.
    
    """

import os

from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # give the access of setting.py file 
application = get_asgi_application() # make blueprint of whole website 
