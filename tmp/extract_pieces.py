import os, re

d = "/Users/Louis-Philippe/Documents/GitHub/court/legal/organisation_preuve"
files = [f for f in os.listdir(d) if f.endswith(".md")]
files.sort()

# pattern to match piece_*.md files
piece_pattern = re.compile(r"piece_[\w-]+\.md")

all_pieces = set()
pieces_by_file = {}

for f in files:
    filepath = os.path.join(d, f)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        pieces = piece_pattern.findall(content)
        
        for p in pieces:
            all_pieces.add(p)
            if p not in pieces_by_file:
                pieces_by_file[p] = set()
            pieces_by_file[p].add(f)

print("UNIQUE PIECES:")
for p in sorted(all_pieces):
    print(p)
