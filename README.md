This is a simple GUI that splits sequences of amino acids into smaller, overlapping parts and uses the public API for ESMFold to fold said sequences. Because this uses a public, shared resource, please limit use of this program unless if it is modified to query a private server. 

This program uses the python module 'requests,' which can be installed by running 'pip install requests' if you are using the pip package manager.

Sequences must be entered following the amino acid sequence FASTA format (all characters other than 'BJOUXZ' are valid). The length of the smaller sequences can be specified, and the start of each subsequent sequence is shifted right by 1 amino acid. The subsequences that should be folded can be selected via the table with shift and control clicks. Currently, the selected indicies entry is not useable, but it will list all of the indexes of the subsequences that are selected.

More information about ESM Metagenomic Atlas and the API used can be found on [their website](https://esmatlas.com/about).