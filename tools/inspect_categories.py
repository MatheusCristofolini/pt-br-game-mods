import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/menu_target_strings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def print_cat(title, filter_fn):
    print(f"\n{'='*20} {title} {'='*20}")
    items = {k: v for k, v in data.items() if filter_fn(k, v['en'].lower())}
    for k, v in items.items():
        print(f"{k} | EN: {repr(v['en'])} | ES: {repr(v['es'])}")
    return items

video = print_cat("VIDEO", lambda k, s: any(w in k.lower() for w in ['video', 'resolut', 'gamma', 'vsync', 'quality', 'tessell', 'ssaa', 'blur', 'directx', 'physx']))
audio = print_cat("AUDIO", lambda k, s: any(w in k.lower() for w in ['audio', 'volume', 'sound', 'music', 'speaker']))
dialogs = print_cat("DIALOGS & POPUPS", lambda k, s: any(w in k.lower() for w in ['confirm', 'warning', 'error', 'prompt', 'alert', 'message', 'dialog']) or k in ['$yes', '$no', '$apply_settings', '$use_defaults', '$cancel', '$back'])
