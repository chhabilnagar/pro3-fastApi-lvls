import json
import os
from typing import Any

def ensure_file_exists(path:str, default_data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok = True)
    if not os.path.isfile(path):
        with open(path,'w', encoding='utf-8') as f:
            json.dump(default_data,f,indent=2)
        

def load_json(path:str,default_data:Any) -> Any:
    ensure_file_exists(path,default_data)
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)


def save_json(path:str,data:Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = f"{path}.tmp"

    with open(tmp_path,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2)
    
    os.replace(tmp_path,path)



