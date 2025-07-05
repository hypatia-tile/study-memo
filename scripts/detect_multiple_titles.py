import os
import re

NOTES_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notes')
pattern = re.compile(r'^= ', re.MULTILINE)

for fname in os.listdir(NOTES_ROOT):
    if fname.endswith('.adoc'):
        fpath = os.path.join(NOTES_ROOT, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = list(pattern.finditer(content))
        if len(matches) > 1:
            print(f"{fname}: {len(matches)} occurrences of '^= '")
