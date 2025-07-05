import os
import re
import json
from datetime import datetime

# Supported note file extensions
NOTE_EXTENSIONS = ['.adoc', '.md']

# Metadata regex patterns
META_PATTERNS = {
    'date': re.compile(r'^:date:\s*(.*)$', re.MULTILINE),
    'tags': re.compile(r'^:tags:\s*(.*)$', re.MULTILINE),
    'topic': re.compile(r'^:topic:\s*(.*)$', re.MULTILINE),
    'related': re.compile(r'^:related:\s*(.*)$', re.MULTILINE),
}

def find_notes(root_dir):
    notes = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if any(fname.endswith(ext) for ext in NOTE_EXTENSIONS):
                notes.append(os.path.join(dirpath, fname))
    return notes

def extract_metadata(filepath, root_dir):
    rel_path = os.path.relpath(filepath, root_dir)
    meta = {'file': rel_path, 'date': None, 'tags': [], 'topic': None, 'related': []}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2048)  # Only read the top part
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

def generate_knowledge_graph(notes_meta, out_path, abs_out_path=None, abs_paths=None):
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
    # Optionally write absolute paths to a separate file
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

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    notes = find_notes(root_dir)
    notes_meta = [extract_metadata(note, root_dir) for note in notes]
    abs_paths = notes
    generate_index(notes_meta, os.path.join(root_dir, 'index.adoc'))
    generate_knowledge_graph(
        notes_meta,
        os.path.join(root_dir, 'knowledge-graph.json'),
        abs_out_path=os.path.join(root_dir, '.knowledge-graph-abs.json'),
        abs_paths=abs_paths
    )

if __name__ == '__main__':
    main()
