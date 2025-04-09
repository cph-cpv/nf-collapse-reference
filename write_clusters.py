import json
import sys
from pathlib import Path

json_path = Path(sys.argv[1])
otus_path = Path(sys.argv[2]) 

print(otus_path,json_path) 


with open(json_path) as f:
    data = json.load(f)


for otu in data["otus"]:
    otu_id = otu["_id"]
    otu_path = otus_path / otu["_id"]
    otu_path.mkdir(exist_ok=True, parents=True)

    for isolate in otu["isolates"]:
        isolate_id = isolate["id"]

        for sequence in isolate["sequences"]:
            segment_name = sequence["segment"]

            with open(otu_path / f"{segment_name}.fa", "a") as f:
                f.write(f">{sequence['_id']}\n{sequence['sequence']}\n")
