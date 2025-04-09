import json


with open("reference.json") as f:
    reference = json.load(f)

for otu in reference["otus"]:
    if otu["_id"] == "8aaf573e":
        for isolate in otu["isolates"]:
            for sequence in isolate["sequences"]:
                if "RNA2" in sequence["definition"]:
                    sequence["segment"] = "RNA 2"

        break


with open("reference_cleaned.json", "w") as f:
    json.dump(reference, f)
