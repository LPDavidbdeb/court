import os, re

d = "/Users/Louis-Philippe/Documents/GitHub/court/legal/organisation_preuve"
files = [f for f in os.listdir(d) if f.endswith(".md") and f.startswith(("2015_", "2019_", "2023_"))]
files.sort()

link_pattern = re.compile(r"\[.*?\]\((.*?)\)")
# find files like .md, .csv, .xlsx
mentions_pattern = re.compile(r"[\w-]+\.(?:md|csv|xlsx)")

inventory = []

for f in files:
    filepath = os.path.join(d, f)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        links = link_pattern.findall(content)
        mentions = mentions_pattern.findall(content)
        
        external_refs = set()
        for link in links:
            # clean up sandbox link
            link = link.replace("sandbox:/mnt/data/", "")
            link = link.split("/")[-1] # just get the filename
            if not link.startswith("piece_") and not link.startswith("http") and link != f:
                external_refs.add(link)
        
        for mention in mentions:
            if not mention.startswith("piece_") and mention != f:
                # filter out obvious internal sections or standard notes
                if mention not in ("faits_par18_2015.md", "pont_par18_2015.md", "argument paragraphe 18.md"):
                    external_refs.add(mention)
        
        inventory.append({
            "file": f,
            "refs": list(external_refs)
        })

print("INVENTORY:")
for item in inventory:
    print(f"- **{item['file']}**")
    if item['refs']:
        print("  - Réfère à :")
        for r in sorted(item['refs']):
            print(f"    - `{r}`")
    else:
        print("  - *Aucune référence externe consolidée trouvée.*")
