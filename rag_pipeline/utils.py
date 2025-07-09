import os
import re


def load_documents_from_folder(folder_path):
    documents = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            documents[filename] = text
    return documents


def split_text(text, max_sentences=2):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_sentences):
        chunk = " ".join(words[i:i + max_sentences])
        chunks.append(chunk)
    return chunks


def split_by_sections(text):

    # Find lines that look like headings
    pattern = re.compile(r'^([A-Z][A-Za-z /&-]+):\s*$')

    sections = []
    current_title = None
    current_content = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = pattern.match(line)
        if match:
            # Found a new section heading
            if current_title:
                sections.append((current_title, " ".join(current_content)))
            current_title = match.group(1)
            current_content = []
        else:
            current_content.append(line)

    # Add the last section
    if current_title:
        sections.append((current_title, " ".join(current_content)))

    return sections


def split_text_in_sections(sections, max_sentences=3):
    chunks = []
    for title, content in sections:
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content.strip())

        for i in range(0, len(sentences), max_sentences):
            chunk_text = " ".join(sentences[i:i + max_sentences])
            if chunk_text:
                chunk = f"{title}: {chunk_text}"
                chunks.append(chunk)

    return chunks