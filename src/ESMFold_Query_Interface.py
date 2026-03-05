# ESMFold Query Interface

import requests
import re
import os
import queue


def construct_xmers(sequence: str, x: int) -> list:
    """
    Constructs xmers and returns a list of them

    Parameters:
        sequence -- string of amino acids following the FASTA format
        x -- length of the xmers to construct

    Return:
        list -- a list containing the xmers constructed; if x < 1, then returns an empty list
    """

    res = list()
    
    if x >= len(sequence):
        res.append(sequence)
        return res
    
    if x < 1:
        print("Invalid xmer length!")
        return res
    
    for i in range(len(sequence) + 1 - x):
        res.append(sequence[i:i + x])

    return res


"""URL for the public ESMFold API"""
esmfold_url = "https://api.esmatlas.com/foldSequence/v1/pdb/"

def fold_sequence(sequence: str, title: str) -> str:
    """
    Queries the public ESMFold API to fold a sequence.

    Parameters:
        sequence -- string of amino acids following the FASTA format
        title -- the title to be associated with the sequence (default "Untitled Sequence")

    Return:
        string -- the response text in the form of a protein database file (.pbd)
    """

    # Setting default title if whitespace only
    if title.strip() == "":
        title = "Untitled Sequence"
    
    # Post request to ESMFold API
    res = requests.post(esmfold_url, data= sequence.upper()).text
    # Add title into response text
    res = re.sub("TITLE *([^\n]*)", ("TITLE     " + title), res, flags= re.UNICODE | re.DOTALL)
    return res


def threaded_fold_sequence(sequence: str, title: str, result_queue: queue.Queue) -> None:
    """
    Starts a new thread running :py:func:`fold_sequence` and stores the result in the queue when finished

    Parameters:
        sequence -- string of amino acids following the FASTA format
        title -- the title to be associated with the sequence (default "Untitled Sequence")
        result_queue -- queue for recieving the return value
    """
    try:
        result = fold_sequence(sequence, title)
        result_queue.put(result)
    except:
        result_queue.put("**Exception**")


def create_dir(dir_name: str) -> str:
    """
    Creates a new directory in "./output/" 
    
    Parameters:
        dir_name -- the name of the directory to be created (spaces are replaced with underscores)
    
    Return:
        string -- the name of the created directory if the directory is successfully created or already exists, otherwise returns "**UnableToCreateDir**"
    """
    try:
        temp_dir_name = "./output/" + dir_name.strip().replace(" ", "_")
        os.mkdir(temp_dir_name)
        return temp_dir_name
    except Exception as ex:
        if type(ex).__name__ == "FileExistsError":
            return temp_dir_name
        else:
            return "**UnableToCreateDir**"


# def create_file(dir: str, file_name:str, content:str) -> bool:
#     temp_dir = "./output/" + dir.strip().replace(" ", "_")
#     with open(dir + "/" + file_name.replace(" ", "_") + ".pdb", "wt") as file:
#         file.write(content)
#         file.close()
#         return True
#     return False


def create_file_ext(dir: str, file_name: str, file_ext: str, content: str) -> int:
    """
    Creates a new file or overwrites an existing file with the same name in the specified directory

    Parameters:
        dir -- the name of the directory for the file to be created in
        file_name -- the name of the file to be created
        file_ext -- the file extension to be appended to the file name
        content -- the contents to be written to the file
        
    Return:
        int -- 0 if the file is successfully opened and written to, 1 if dir is empty, 2 if file_name is empty, 3 if an exception occurrs while writing to the file
    """
    if len(dir) <= 0:
        return 1
    
    if len(file_name) <= 0:
        return 2

    temp_file_ext = file_ext.strip()
    if len(temp_file_ext) > 0 and not file_ext.startswith('.'):
        temp_file_ext = "." + temp_file_ext
    
    try:
        with open(f"{dir}/{file_name}{temp_file_ext}", "wt") as file:
            file.write(content)
            file.close()
            return 0
    except Exception as ex:
        return 3



"""
These methods are deprecated as they were used for the command line version of the interface

# def request_sequence() -> str:
#     while True:
#         res = input("Enter the sequence you wish to fold: ").strip().upper()
        
#         if re.search("^[ARNDCQEGHILKMFPSTWYV]*$", res):
#             return res
        
#         print("Error: " + res + " : Invalid sequence!")


# def request_xmer_len() -> int:
#     while True:
#         res = input("Enter xmer length: ")

#         if res.isdigit() and int(res) > 2:
#             return int(res)
        
#         print("Error: " + res + ": Invalid xmer length!")


# def request_indices(xmers: list) -> set:
#     res = set()

#     for i in range(len(xmers)):
#         print(str(i) + ": " + xmers[i])

#     ans = input("Enter the index of an xmer you wish to fold or done to continue: ")
    
#     while ans != "done":
#         if ans.isdigit() and int(ans) >= 0 and int(ans) < len(xmers):
#             res.add(int(ans))
#         else:
#             print("Error: " + ans + ": Invalid index!")
        
#         ans = input("Enter the index of an xmer you wish to fold or done to continue: ")

#     return res



# def fold_specific_xmers(xmers, indices, base_title=""):
#     res = list()
    
#     if len(indices) == 0:
#         print("Warning: No xmers selected!")
#         return res
    
#     if base_title == "":
#         title = "Untitled Sequence"
#     else:
#         title = base_title
    
#     for i in indices:
#         res.append((title + "_" + str(i), fold_sequence(xmers[i], title + ": xmer #" + str(i))))

#     return res


# def fold_specific_xmers(index_xmers: list, base_title=""):
#     res = list()
    
#     if base_title == "":
#         title = "Untitled Sequence"
#     else:
#         title = base_title
    
#     for target in index_xmers:
#         res.append((title + "_" + str(target[0]), fold_sequence(target[1], title + ": xmer #" + str(target[0]))))

#     return res


# def resolve_conflicting_dir_name(dir_name) -> str:
#     temp_dir_name = dir_name.replace(" ", "_")
#     dupicate_dir_name_index = 1
#     created_dir_name = temp_dir_name + "(" + str(dupicate_dir_name_index) + ")"
    
#     while create_dir(created_dir_name) == "**DirAlreadyExists**":
#         dupicate_dir_name_index += 1
#         created_dir_name = temp_dir_name + "(" + str(dupicate_dir_name_index) + ")"
    
#     return created_dir_name


    
# Main
# def main() -> int:
#     seq_name = input("Enter the name of the sequence: ")
#     seq = request_sequence()
#     xmer_len = request_xmer_len()

#     xmers = construct_xmers(seq, xmer_len)

#     indices = request_indices(xmers)
#     folded_xmers = fold_specific_xmers(xmers, indices, seq_name)

#     create_dir_res = create_dir(seq_name)
    
#     if create_dir_res == "**DirAlreadyExists**":
#         create_dir_res = resolve_conflicting_dir_name(seq_name)

#     if create_dir_res == "**UnableToCreateDir**":
#         print("Could not create a new directory!")
#         return 1
    
#     file_write_results = list()
#     for xmer in folded_xmers:
#         file_write_results.append((create_file(create_dir_res, xmer[0], xmer[1]), xmer[0]))

#     for file_write_result in file_write_results:
#         if file_write_result[0]:
#             print("    Successfully written \"" + file_write_result[1] + "\" to \"" + create_dir_res +"\"")
#         else:
#             print("    Failed to write \"" + file_write_result[1] + "\" to \"" + create_dir_res +"\"")

#     print("Output written to " + create_dir_res)
#     return 0


# Main entrypoint
#main()

"""