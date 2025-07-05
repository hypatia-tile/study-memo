import os
import sys
from glob import glob
from datetime import datetime

NOTES_DIR = 'notes'
DRAFT_BASE = 'draft'

# --- Model ---
class NoteModel:
    @staticmethod
    def create_draft(draft_dir, title=None):
        full_draft_dir = os.path.join(DRAFT_BASE, draft_dir)
        if not os.path.exists(full_draft_dir):
            os.makedirs(full_draft_dir)
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'note_{date_str}.adoc'
        filepath = os.path.join(full_draft_dir, filename)
        if title is None:
            title = 'Draft Note'
        content = f"= {title}\n:toc:\n:icons: font\n:date: {datetime.now().strftime('%Y-%m-%d')}\n:tags: draft\n\nWrite your note here.\n"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    @staticmethod
    def integrate_topic(topic_dir, notes_dir=NOTES_DIR):
        topic = os.path.basename(topic_dir.rstrip('/'))
        adoc_files = []
        main_file = os.path.join(topic_dir, 'main.adoc')
        if os.path.exists(main_file):
            adoc_files.append(main_file)
        adoc_files += [f for f in glob(os.path.join(topic_dir, '*.adoc')) if f != main_file]
        if adoc_files:
            out_file = os.path.join(notes_dir, f'{topic}.adoc')
            with open(out_file, 'w', encoding='utf-8') as out:
                for fpath in adoc_files:
                    with open(fpath, 'r', encoding='utf-8') as fin:
                        out.write(f'// ---- {os.path.basename(fpath)} ----\n')
                        out.write(fin.read())
                        out.write('\n\n')
            return out_file, len(adoc_files)
        else:
            return None, 0

    @staticmethod
    def find_notes(root_dir=NOTES_DIR, extensions=None):
        if extensions is None:
            extensions = ['.adoc', '.md']
        notes = []
        for dirpath, _, filenames in os.walk(root_dir):
            for fname in filenames:
                if any(fname.endswith(ext) for ext in extensions):
                    notes.append(os.path.join(dirpath, fname))
        return notes

    @staticmethod
    def extract_metadata(filepath, root_dir):
        import re
        META_PATTERNS = {
            'date': re.compile(r'^:date:\s*(.*)$', re.MULTILINE),
            'tags': re.compile(r'^:tags:\s*(.*)$', re.MULTILINE),
            'topic': re.compile(r'^:topic:\s*(.*)$', re.MULTILINE),
            'related': re.compile(r'^:related:\s*(.*)$', re.MULTILINE),
        }
        rel_path = os.path.relpath(filepath, root_dir)
        meta = {'file': rel_path, 'date': None, 'tags': [], 'topic': None, 'related': []}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(2048)
            for key, pattern in META_PATTERNS.items():
                match = pattern.search(content)
                if match:
                    value = match.group(1).strip()
                    if key == 'tags':
                        meta['tags'] = [t.strip() for t in value.split(',') if t.strip()]
                    elif key == 'related':
                        meta['related'] = [r.strip() for r in value.split(',') if r.strip()]
                    else:
                        meta[key] = value
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
        return meta

    @staticmethod
    def generate_index(notes_meta, out_path):
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("= Notes Index\n\n")
            for meta in notes_meta:
                rel_path = meta['file']
                f.write(f"* link:{rel_path}[{os.path.basename(rel_path)}] ")
                if meta['topic']:
                    f.write(f"({meta['topic']}) ")
                if meta['date']:
                    f.write(f"[{meta['date']}] ")
                if meta['tags']:
                    f.write(f"tags: {', '.join(meta['tags'])} ")
                f.write("\n")
        print(f"Index written to {out_path}")

    @staticmethod
    def generate_knowledge_graph(notes_meta, out_path, abs_out_path=None, abs_paths=None):
        import json
        graph = {'nodes': [], 'edges': []}
        file_to_id = {meta['file']: idx for idx, meta in enumerate(notes_meta)}
        for idx, meta in enumerate(notes_meta):
            graph['nodes'].append({
                'id': idx,
                'file': meta['file'],
                'topic': meta['topic'],
                'tags': meta['tags'],
            })
            for rel in meta['related']:
                for other_idx, other_meta in enumerate(notes_meta):
                    if rel in other_meta['file']:
                        graph['edges'].append({'from': idx, 'to': other_idx})
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2)
        print(f"Knowledge graph written to {out_path}")
        if abs_out_path and abs_paths:
            abs_graph = {'nodes': [], 'edges': graph['edges']}
            for idx, meta in enumerate(notes_meta):
                abs_graph['nodes'].append({
                    'id': idx,
                    'file': abs_paths[idx],
                    'topic': meta['topic'],
                    'tags': meta['tags'],
                })
            with open(abs_out_path, 'w', encoding='utf-8') as f:
                json.dump(abs_graph, f, indent=2)
            print(f"Absolute path knowledge graph written to {abs_out_path}")

    @staticmethod
    def detect_multiple_titles(notes_dir=NOTES_DIR):
        import re
        pattern = re.compile(r'^= ', re.MULTILINE)
        for fname in os.listdir(notes_dir):
            if fname.endswith('.adoc'):
                fpath = os.path.join(notes_dir, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                matches = list(pattern.finditer(content))
                if len(matches) > 1:
                    print(f"{fname}: {len(matches)} occurrences of '^= '")

# --- View ---
class NoteView:
    @staticmethod
    def show_created(filepath):
        print(f"Created template: {filepath}")

    @staticmethod
    def show_integrated(out_file, count):
        if out_file:
            print(f"Integrated {count} files into {out_file}")
        else:
            print("No .adoc files found to integrate.")

    @staticmethod
    def show_usage():
        print("""
Usage:
  python3 scripts/note_manager.py draft <draft_dir> [title]         # Create a draft note
  python3 scripts/note_manager.py integrate <draft/topic_dir> [notes_dir]  # Integrate topic notes
  python3 scripts/note_manager.py interactive                      # Interactive mode
""")

    @staticmethod
    def menu():
        print("""
Note Manager - Interactive Mode
1. Create a draft note
2. Integrate a topic
3. Exit
""")

    @staticmethod
    def prompt(msg):
        return input(msg)

# --- Controller ---
def interactive():
    while True:
        NoteView.menu()
        choice = NoteView.prompt("Select an option: ").strip()
        if choice == '1':
            draft_dir = NoteView.prompt("Draft topic directory (e.g., draft/mytopic): ").strip()
            title = NoteView.prompt("Note title (optional): ").strip()
            title = title if title else None
            filepath = NoteModel.create_draft(draft_dir, title)
            NoteView.show_created(filepath)
        elif choice == '2':
            topic_dir = NoteView.prompt("Draft topic directory to integrate (e.g., draft/mytopic): ").strip()
            notes_dir = NoteView.prompt("Output notes directory [notes]: ").strip() or 'notes'
            out_file, count = NoteModel.integrate_topic(topic_dir, notes_dir)
            NoteView.show_integrated(out_file, count)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def main():
    if len(sys.argv) < 2:
        NoteView.show_usage()
        sys.exit(1)
    command = sys.argv[1]
    if command == 'draft':
        if len(sys.argv) < 3:
            NoteView.show_usage()
            sys.exit(1)
        draft_dir = sys.argv[2]
        title = sys.argv[3] if len(sys.argv) > 3 else None
        filepath = NoteModel.create_draft(draft_dir, title)
        NoteView.show_created(filepath)
    elif command == 'integrate':
        if len(sys.argv) < 3:
            NoteView.show_usage()
            sys.exit(1)
        topic_dir = sys.argv[2]
        notes_dir = sys.argv[3] if len(sys.argv) > 3 else 'notes'
        out_file, count = NoteModel.integrate_topic(topic_dir, notes_dir)
        NoteView.show_integrated(out_file, count)
    elif command == 'interactive':
        interactive()
    else:
        NoteView.show_usage()
        sys.exit(1)

if __name__ == '__main__':
    main()
