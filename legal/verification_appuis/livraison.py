"""Conserver les recettes et rapports ; aucune mutation Git ni accès réel."""
from pathlib import Path
import subprocess
import sys

from .commun import RAPPORTS, RACINE, Refus, chemin_sortie


def recette(story, description, fichiers, lectures="Aucune. Fixtures synthétiques uniquement.", ecarts="Aucun.", verdict="PASS"):
    commande = [sys.executable, "-B", "-W", "error::ResourceWarning", "-m", "unittest",
                f"legal.verification_appuis.tests.test_{story.lower()}", "-v"]
    execution = subprocess.run(commande, cwd=RACINE, capture_output=True, text=True)
    sortie = execution.stdout + execution.stderr
    chemin_sortie(RAPPORTS / f"{story}.tests.txt").write_text(sortie)
    if execution.returncode:
        print(sortie)
        raise Refus(f"{story} : recette échouée, aucun PASS")
    texte = (f"# {story} — rapport d'exécution\n\n**Verdict : {verdict}.**\n\n{description}\n\n"
             f"## Commande et sortie réelle\n\n```sh\n{' '.join(commande)}\n```\n\n"
             f"Code de sortie : {execution.returncode}. [Sortie brute]({story}.tests.txt).\n\n"
             "## Fichiers créés ou modifiés\n\n" + "\n".join(f"- `{f}`" for f in fichiers) +
             f"\n- Le présent rapport et sa sortie de tests.\n\n## Données réelles\n\n{lectures}\n\n"
             f"## Écarts et raisons\n\n{ecarts}\n\n"
             "Le SHA du commit est relevé après sa création dans le [registre](REGISTRE_EXECUTION.md).\n")
    chemin_sortie(RAPPORTS / f"{story}.md").write_text(texte)
    print(sortie, end="")


def referencer(story, sha, verdict="PASS", rapport=None):
    # SHA déjà créé, jamais calculé d'avance ni inscrit dans son propre commit.
    effectif = subprocess.check_output(["git", "rev-parse", sha], cwd=RACINE, text=True).strip()
    if effectif != sha:
        raise Refus("SHA incomplet ou différent")
    rapport = rapport or f"{story}.md"
    registre = RAPPORTS / "REGISTRE_EXECUTION.md"
    with registre.open("a") as f:
        f.write(f"\n- **{story} : {verdict}** — `{sha}` — [rapport]({rapport}).\n")
