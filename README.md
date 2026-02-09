# ESMFold Query Interface
This is a simple GUI that splits sequences of amino acids into smaller, overlapping parts and uses the public API for ESMFold to fold said sequences. Because this uses a public, shared resource, please limit use of this program unless if it is modified to query a private server. 

## Getting Started
Python version 3.14 and requests version 2.32.5 and its dependancies are all that's needed to run the program.
### On Windows
1. Install Python version 3.14 (pip should be included by default)
2. Open a new Terminal
3. Find where your python installation is located (Usually in C:/Users/{Your User name}/AppData/Local/Python/{python version core}) and run the following command
```powershell
./{path/to/python}/python.exe -m pip install requests==2.32.5
```

## Using the GUI
Sequences must be entered following the amino acid sequence FASTA format (all characters other than 'BJOUXZ' are valid). The length of the smaller sequences can be specified, and the start of each subsequent sequence is shifted right by 1 amino acid. The subsequences that should be folded can be selected via the table with shift and control clicks. Currently, the selected indicies entry is not useable, but it will list all of the indexes of the subsequences that are selected.

## Additional Info
More information about ESM Metagenomic Atlas and the API used can be found on [their website](https://esmatlas.com/about).
