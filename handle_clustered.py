import json
from pathlib import Path
import csv


with open("input/reference.json") as f:
    data = json.load(f)

    id_to_name = {
        otu["_id"]: otu["name"] for otu in data["otus"]
    }


counts = []
    

for otu_path in Path("results/clustered").iterdir():
    otu_id = otu_path.stem
    name = id_to_name[otu_id]

    input_count = 0
    rep_count = 0

    for input_fasta_path in otu_path.glob("*.fa"):
        with open(input_fasta_path) as f:
            input_count += len([line for line in f if line[0] == ">"])

        stem = input_fasta_path.stem

        with open(input_fasta_path.parent / f"{stem}_rep_seq.fasta") as f:
            rep_count += len([line for line in f if line[0] == ">"])

    counts.append((otu_id, name, input_count, rep_count))

with open("counts.csv", "w") as f:
    writer = csv.writer(f)

    writer.writerow(["otu_id", "name", "input_count", "rep_count"])
    writer.writerows(counts)


        # print(f"'{stem}'", input_count, "->", rep_count)
 

    # with open(all_seqs_path) as f:
    #     for line in f:
    #         if line[0] == ">":
    #             print(line.rstrip().lstrip(">"))
