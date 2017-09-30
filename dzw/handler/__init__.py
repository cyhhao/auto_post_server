import inspect

import os

import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
import importlib

all_hander = []
all_hander_dict = {}
import_list = ['weibo', 'baike', 'tieba']
# for f in os.listdir(path):
#     if f.endswith('.py') and f.endswith('_handler.py'):
#         module = importlib.import_module(f[:-3])
#         for name, obj in inspect.getmembers(module):
#             if inspect.isclass(obj):
#                 if not str(obj).startswith('core.'):
#                     print name, obj
#                     all_hander.append(obj())

for li in import_list:
    module = importlib.import_module(li + '_handler')
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if not str(obj).startswith('core.'):
                print name, obj
                instance = obj()
                all_hander.append(instance)
                all_hander_dict[name] = instance
