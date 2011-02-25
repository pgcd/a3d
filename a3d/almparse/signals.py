'''
Created on 13/giu/2010

@author: pgcd
'''
from django.dispatch import Signal
parsing_done = Signal(providing_args = ["text", ])
