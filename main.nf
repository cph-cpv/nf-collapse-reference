#!/usr/bin/env nextflow

params.reference_json = file("input/reference.json")




process createClusterDirs {
    publishDir "results/clusters", mode: 'copy'

    input:
    path reference
    path write_clusters

    output:
    path "otus/*"

    script:
    """
    python3 ${write_clusters} ${reference} otus
    """
}

process clusterWithMmseqs {
    publishDir "results/clustered"

    cpus 2
    memory '15 GB'

    input:
    tuple(path(otu_path),  path(fasta_path))

    output:
    path "**/*.{tsv,fa,fasta}"

    script:
    """
    mmseqs easy-cluster --threads 4 -c 0.99 --split-memory-limit 15G ${otu_path}/${fasta_path} '${otu_path}/${fasta_path.baseName}' \$(mktemp -d mmseqs-cluster-XXXXXXXX)
    """

    stub:
    """
    tree ${otu_path} > content.txt
    ls -lh ${otu_path}/${fasta_path} >> content.txt
    echo "${otu_path}/${fasta_path.baseName}" >> content.txt
    """
}

workflow {
    def write_clusters = file("write_clusters.py")

    // First, create OTU directories
    otu_paths = createClusterDirs(params.reference_json, write_clusters)
    otu_paths
        | flatten
        | flatMap { 
            p -> p.listFiles().collect { fp -> tuple(p, fp) }
        }
        | clusterWithMmseqs    
}