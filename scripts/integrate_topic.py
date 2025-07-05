import os
from glob import glob
import sys

def integrate_topic(topic_dir):
    topic = os.path.basename(topic_dir.rstrip('/'))
    adoc_files = []
    main_file = os.path.join(topic_dir, 'main.adoc')
    if os.path.exists(main_file):
        adoc_files.append(main_file)
    adoc_files += [f for f in glob(os.path.join(topic_dir, '*.adoc')) if f != main_file]
    if adoc_files:
        out_file = os.path.join(os.path.dirname(topic_dir), f'{topic}.adoc')
        with open(out_file, 'w', encoding='utf-8') as out:
            for fpath in adoc_files:
                with open(fpath, 'r', encoding='utf-8') as fin:
                    out.write(f'// ---- {os.path.basename(fpath)} ----\n')
                    out.write(fin.read())
                    out.write('\n\n')
        print(f'Integrated {len(adoc_files)} files into {out_file}')
    else:
        print(f'No .adoc files found in {topic_dir}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 scripts/integrate_topic.py <notes/topic_folder>')
        sys.exit(1)
    integrate_topic(sys.argv[1])
