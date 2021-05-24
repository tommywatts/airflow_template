import os
import sys
from pathlib import Path
from datetime import datetime
import importlib

def date_transform(str_date): 
    if isinstance(str_date, datetime):
        return str_date
    if isinstance(str_date, str):
        return datetime.strptime(str_date, '%Y-%m-%d')
    return datetime.combine(str_date, datetime.min.time())

def import_str_module(module_str):
    mod, cls_ = module_str.rsplit('.', 1)
    return getattr(importlib.import_module(mod), cls_)
    
def get_python_func(python_callable_name, python_callable_file):
    python_callable_file = os.path.join(os.getenv('DAG_DIR'), python_callable_file)
    python_file_path = Path(python_callable_file).resolve()
    module_name = python_file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, python_callable_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    return getattr(module, python_callable_name)
