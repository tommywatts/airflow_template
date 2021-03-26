
from datetime import datetime
from importlib import import_module

def date_transform(str_date): 
    if isinstance(str_date, datetime):
        return str_date
    if isinstance(str_date, str):
        return datetime.strptime(str_date, '%Y-%m-%d')
    return datetime.combine(str_date, datetime.min.time())

def import_str_module(module_str):
    mod, cls_ = module_str.rsplit('.', 1)
    return getattr(import_module(mod), cls_)