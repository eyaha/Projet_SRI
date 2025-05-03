import pandas as pd
import pyterrier as pt

if not pt.started():
    pt.init()

# Liste de vos fichiers Qrels
qrels_paths = [
    "qrels_MB01-06.txt",
    # "qrels_MB07-11.txt",
    # "qrels_MB12-16.txt",
    # "qrels_MB17-21.txt",
    # "qrels_MB22-27.txt",
    # "qrels_MB28-32.txt",
    # "qrels_MB33-38.txt",
    # "qrels_MB39-45.txt",
    "qrels_MB46-50.txt",
    # "qrels_MB51-55.txt",
    # "qrels_MB56-60.txt"
]

# Lire et concaténer tous les fichiers qrels
qrels_df = pd.concat([pt.io.read_qrels(f) for f in qrels_paths], ignore_index=True)

# Sauvegarder le DataFrame concaténé dans un fichier
qrels_df.to_csv("TotalQrels.txt", sep=" ", header=False, index=False)

# Afficher un aperçu
print(qrels_df.head())
print(f"Total qrels saved to totalqrels.txt: {len(qrels_df)}")
