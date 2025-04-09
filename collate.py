import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ClusterIsolateMember:
    """
    Represents a member of a cluster isolate.
    """
    id: int
    source_name: str
    source_type: str


@dataclass
class ClusterIsolate:
    """

    """
    reps: list[str]

    isolates: list[ClusterIsolateMember] = field(default_factory=list)


isolates_by_id = {}
isolates_by_sequence_id = {}

otus_by_id = {}


with open("reference.json") as f:
    reference = json.load(f)

    for otu in reference["otus"]:
        otus_by_id[otu["_id"]] = {
            "id": otu["_id"],
            "name": otu["name"],
            "schema": otu["schema"],
        }

        for isolate in otu["isolates"]:
            cluster_isolate_member = ClusterIsolateMember(
                id= isolate["id"],
                source_name=isolate["source_name"],
                source_type=isolate["source_type"],
            )

            isolates_by_id[isolate["id"]] = cluster_isolate_member

            for sequence in isolate["sequences"]:
                isolates_by_sequence_id[sequence["_id"]] = cluster_isolate_member

for otu_path in Path("results/clustered").iterdir():
    otu = otus_by_id[otu_path.stem]

    

    schema_segment_names = {s["name"] for s in otus_by_id[otu["id"]]["schema"]}

    cluster_segment_names = {p.stem.replace("_rep_seq", "").replace("_all_seqs", "").replace("_cluster", "")for p in otu_path.iterdir()}

    if not cluster_segment_names == schema_segment_names:
        print({
        "otu_id": otu["id"],
        "stem": otu_path.stem,
    })
        
        raise ValueError(f"OTU {otu['name']} ({otu['id']} with segment names {cluster_segment_names} does not match schema with segment names {schema_segment_names}")