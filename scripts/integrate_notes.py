import os
from glob import glob

NOTES_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notes')

for folder in os.listdir(NOTES_ROOT):
    folder_path = os.path.join(NOTES_ROOT, folder)
    if os.path.isdir(folder_path):
        adoc_files = []
        main_file = os.path.join(folder_path, 'main.adoc')
        if os.path.exists(main_file):
            adoc_files.append(main_file)
        # Add other .adoc files (excluding main.adoc)
        adoc_files += [f for f in glob(os.path.join(folder_path, '*.adoc')) if f != main_file]
        if adoc_files:
            out_file = os.path.join(NOTES_ROOT, f'{folder}.adoc')
            with open(out_file, 'w', encoding='utf-8') as out:
                for fpath in adoc_files:
                    with open(fpath, 'r', encoding='utf-8') as fin:
                        out.write(f'// ---- {os.path.basename(fpath)} ----\n')
                        out.write(fin.read())
                        out.write('\n\n')
            print(f'Integrated {len(adoc_files)} files into {out_file}')
