import tkinter as tk
import os
import re
import threading
import queue
import time
from tkinter import ttk
from tkinter import font
from tkinter import scrolledtext as st
from ESMFold_Query_Interface import *

# default_font = ("Calibri", 12)

window = tk.Tk()
window.title("ESMFold Query Interface")
window.state("zoomed")
# window.geometry(str(int(window.winfo_screenwidth() / 2)) + "x" + str(4 * int(window.winfo_screenheight() / 5)) + "+10+10")
window.resizable(True, True)
window.option_add("*Font", "Calibri 12")
window.option_add("*Label.justify", "left")

default_font = font.Font(family="Calibri", size=12)
default_style = ttk.Style()
default_style.configure("Treeview.Heading", font="Calibri 12")

# font.nametofont("TkDefaultFont").config(family="Calibri", size=12)
# font.nametofont("TkHeadingFont").config(family="Calibri", size=12)


# =========================================================================
# Labels/Entries
# =========================================================================

# Input section frame
f_input_section = tk.Frame(window)

# Sequence name entry
f_seq_name = tk.Frame(master=f_input_section)
l_seq_name = tk.Label(master=f_seq_name, text="Sequence name:")
l_seq_name.pack(anchor="nw")

t_seq_name = tk.StringVar()

e_seq_name = tk.Entry(master=f_seq_name, textvariable=t_seq_name)
e_seq_name.pack(anchor="nw", fill='x')


# Save directory entry
f_save_dir = tk.Frame(master=f_input_section)
l_save_dir = tk.Label(master=f_save_dir, text="Directory name:")
l_save_dir.pack(anchor="nw")

t_save_dir = tk.StringVar()
e_save_dir = tk.Entry(master=f_save_dir, textvariable=t_save_dir)
e_save_dir.pack(anchor="nw", fill='x')

t_msg_save_dir = tk.StringVar(value="No directory specified")
msg_save_dir = tk.Label(master=f_save_dir, textvariable=t_msg_save_dir)
msg_save_dir.pack(anchor="nw")

save_dir_changed_flag = tk.BooleanVar(value=False)


# Sequence entry
f_seq = tk.Frame(master=f_input_section)
l_seq = tk.Label(master=f_seq, text="Sequence:")
l_seq.pack(anchor="nw")

t_seq = tk.StringVar()
e_seq = tk.Entry(master=f_seq, textvariable=t_seq)
e_seq.pack(anchor="nw", fill="x")

t_msg_seq = tk.StringVar(value="No sequence entered")
l_msg_seq = tk.Label(master=f_seq, textvariable=t_msg_seq)
l_msg_seq.pack(anchor="nw")


# Xmer length entry
f_xmer_len = tk.Frame(master=f_input_section)
l_xmer_len = tk.Label(master=f_xmer_len, text="Xmer length:")
l_xmer_len.pack(anchor="nw")

t_xmer_len = tk.IntVar(value=0)
sb_xmer_len = tk.Spinbox(master=f_xmer_len, textvariable=t_xmer_len, from_=0, to=2147483647, increment=1)
sb_xmer_len.pack(anchor="nw")


# Xmer list treeview
f_xmer_list = tk.Frame(master=f_input_section)
l_xmer_list = tk.Label(master=f_xmer_list, text="Xmers: (right-click table to refresh or click button below)")
l_xmer_list.pack(anchor="nw")

tv_xmer_list = ttk.Treeview(master=f_xmer_list, style="default_style.Treeview", height=10)

tv_xmer_list.tag_configure("header", background="#FFFFFF", font="Calibri 12")
tv_xmer_list.tag_configure("even", background="#FFFFFF", font="Calibri 12")
tv_xmer_list.tag_configure("odd", background="#E8E8E8", font="Calibri 12")

tv_xmer_list["columns"] = ("Index", "Xmer")

col_index_width = default_font.measure("Index") + 12
col_xmer_width = default_font.measure("Xmer") + 12

tv_xmer_list.column("#0", minwidth=0, width=0, anchor="nw", stretch=False)
tv_xmer_list.column("Index", width=col_index_width, anchor="nw", stretch=False)
tv_xmer_list.column("Xmer", minwidth=col_xmer_width, anchor="nw", stretch=True)

tv_xmer_list.heading("#0", text="", anchor="nw")
tv_xmer_list.heading("Index", text="Index", anchor="nw")
tv_xmer_list.heading("Xmer", text="Xmer", anchor="nw")

tv_xmer_list.pack(anchor="nw", expand=True, fill="x")

b_xmer_list = tk.Button(master=f_xmer_list, text="Refresh table", relief="raised")
b_xmer_list.pack(anchor="nw", pady=5)


# Select indicies entry
f_sel_indicies = tk.Frame(master=f_input_section)
l_sel_indicies = tk.Label(master=f_sel_indicies, text="Selected indicies:")
l_sel_indicies.pack(anchor="nw")

t_sel_indicies = tk.StringVar()
e_sel_indicies = tk.Entry(master=f_sel_indicies, textvariable=t_sel_indicies, state="readonly")
e_sel_indicies.pack(anchor="nw", fill='x')

v_sel_indicies = tk.Variable()

def update_t_sel_indicies():
    temp_sel_indicies = v_sel_indicies.get()
    temp_t_sel_indicies = ""
    for i in range(0, len(temp_sel_indicies) - 1):
        temp_t_sel_indicies += temp_sel_indicies[i][0] + ", "
    t_sel_indicies.set(temp_t_sel_indicies + temp_sel_indicies[len(temp_sel_indicies) - 1][0])


# Fold xmers button
f_fold_xmers = tk.Frame(master=f_input_section)
b_fold_xmers = tk.Button(master=f_fold_xmers, text="Fold Xmers")
b_fold_xmers.pack(anchor="nw")


# Debug console
f_debug_section = ttk.Frame(master=window)
st_debug = st.ScrolledText(master=f_debug_section, font=("Calibri", 12), state="disabled")
st_debug.pack(fill="both", expand=True)

def debug_print(msg: str):
    st_debug.config(state="normal")
    st_debug.insert(tk.END, msg + "\n")
    st_debug.see(tk.END)
    st_debug.config(state="disabled")
    st_debug.update()

debug_print("Start ESMFold Query Interface\n")

# c_debug = tk.Canvas(master=f_debug_section)
# sb_debug = ttk.Scrollbar(master=f_debug_section, orient="vertical", command=c_debug.yview)
# c_debug.configure(yscrollcommand=sb_debug.set)
# sf_debug = ttk.Frame(master=c_debug)

# sb_debug.pack(anchor="ne", side="right", fill="y")
# c_debug.pack(side="left", fill="both", expand=True)
# sf_debug.pack(fill="both", side="top", expand=True)

# c_debug.configure(yscrollcommand=sb_debug.set)
# c_debug.create_window((0, 0), window=sf_debug, anchor="nw")

# l_default_msg = tk.Label(master=sf_debug, text="Start Debugging", justify="left", anchor="nw")
# l_default_msg.pack(side="top", anchor="nw", fill="x")

# def debug_print(msg: str):
#     l_debug_msg = tk.Label(master=sf_debug, text=msg, justify="left", anchor="nw")
#     l_debug_msg.pack(side="top", anchor="nw", fill="x")
#     c_debug.update_idletasks()
#     c_debug.scrollregion = c_debug.bbox("all")
#     c_debug.yview_moveto(1.0)


# =========================================================================
# Events
# =========================================================================

# Sequence name events
change_source_seq_name_flag = tk.BooleanVar(value=False)

def t_seq_name_change(*args):
    if not save_dir_changed_flag.get():
        change_source_seq_name_flag.set(True)
        t_save_dir.set(t_seq_name.get())
t_seq_name.trace_add("write", t_seq_name_change)


# Save directory events
def t_save_dir_change(*args):
    text_t_save_dir = t_save_dir.get().replace(" ", "_")
    save_dir_changed_flag.set((not change_source_seq_name_flag.get()) and (len(text_t_save_dir) != 0))
    change_source_seq_name_flag.set(False)
    
    if len(text_t_save_dir) != 0:
        text_t_save_dir.replace(" ", "_")
        save_dir = "./output/" + text_t_save_dir
        if os.path.isdir(save_dir):
            debug_print("Warning: Pre-existing directory (" + save_dir + ")! Files could be overwritten.")
            t_msg_save_dir.set("Warning: Pre-existing directory (" + save_dir + ")!\nFiles could be overwritten.")
        else:
            t_msg_save_dir.set("Save outputs to: " + save_dir)
    else:
        t_msg_save_dir.set("No directory specified")
t_save_dir.trace_add("write", t_save_dir_change)


# Sequence entry events
def t_seq_change(*args):
    text_t_seq = t_seq.get().strip().upper()

    if len(text_t_seq) == 0:
        t_msg_seq.set("No sequence entered")
        l_msg_seq.config(bg="lightgray")
    elif not re.search("^[ARNDCQEGHILKMFPSTWYV]*$", text_t_seq):
        t_msg_seq.set("Invalid sequence!")
        l_msg_seq.config(bg="#ff0000")
    else:
        t_msg_seq.set("Valid sequence")
        l_msg_seq.config(bg="#00df00")
t_seq.trace_add("write", t_seq_change)


# Xmer list events
def fill_tv(xmers: list):
    for i in range(0, len(xmers)):
        if i%2 == 0:
            tv_xmer_list.insert("", index=i, values=(i, xmers[i]), tags=("even"))
        else:
            tv_xmer_list.insert("", index=i, values=(i, xmers[i]), tags=("odd"))
            
def update_tv_contents(event):
    tv_xmer_list.delete(*tv_xmer_list.get_children())

    if len(t_seq.get()) == 0 or t_xmer_len.get() == 0:
        return "break"

    xmers = construct_xmers(t_seq.get(), t_xmer_len.get())

    if len(xmers) != 0:
        fill_tv(xmers)
tv_xmer_list.bind("<Button-3>", update_tv_contents)

def prevent_resize(event):
    if (
        tv_xmer_list.identify_region(event.x, event.y) == "separator" or
        tv_xmer_list.identify_element(event.x, event.y) == "separator"
        ):
        return "break"
tv_xmer_list.bind("<Button-1>", prevent_resize)
tv_xmer_list.bind("<Motion>", prevent_resize)

def b_xmer_list_on_release(event):
    bbox_b_xmer_list = (b_xmer_list.winfo_rootx(), b_xmer_list.winfo_rooty(), b_xmer_list.winfo_width(), b_xmer_list.winfo_height())
    if (
        event.x_root >= bbox_b_xmer_list[0] and
        event.x_root < bbox_b_xmer_list[0] + bbox_b_xmer_list[2] and
        event.y_root >= bbox_b_xmer_list[1] and
        event.y_root < bbox_b_xmer_list[1] + bbox_b_xmer_list[3]
        ):
            update_tv_contents(event)
b_xmer_list.bind("<ButtonRelease-1>", b_xmer_list_on_release)

change_source_xmer_list_flag = tk.BooleanVar(value=False)

def tv_xmer_list_on_selection(event):
    if tv_xmer_list.identify_region(event.x, event.y) == "cell":
        selected_xmers = list()
        selected_xmers_ids = tv_xmer_list.selection()
        for target in selected_xmers_ids:
            selected_xmers.append(tv_xmer_list.item(target, "values"))
        v_sel_indicies.set(selected_xmers)
        update_t_sel_indicies()
tv_xmer_list.bind("<ButtonRelease-1>", tv_xmer_list_on_selection)

# Selected indicies events
# TO-DO

# Fold xmers events
def b_fold_xmers_on_click(event):
        bbox_b_fold_xmers = (b_fold_xmers.winfo_rootx(), b_fold_xmers.winfo_rooty(), b_fold_xmers.winfo_width(), b_fold_xmers.winfo_height())
        if (
            not (
                event.x_root >= bbox_b_fold_xmers[0] and
                event.x_root < bbox_b_fold_xmers[0] + bbox_b_fold_xmers[2] and
                event.y_root >= bbox_b_fold_xmers[1] and
                event.y_root < bbox_b_fold_xmers[1] + bbox_b_fold_xmers[3]
            )
        ):
            return "break"
        
        if len(t_save_dir.get()) == 0:
            debug_print("Error: No save directory specified!")
            return "break"
        
        if len(v_sel_indicies.get()) == 0:
            debug_print("Error: No xmers selected!")
            return "break"
        
        save_results()
b_fold_xmers.bind("<ButtonRelease-1>", b_fold_xmers_on_click)


def save_results():
    debug_print("Starting xmer folding process...")

    # Creating save directory
    debug_print("Creating output directory...")
    temp_save_dir = t_save_dir.get()
    res_create_dir = create_dir(temp_save_dir)
    
    if res_create_dir == "**UnableToCreateDir**": # Failed to create save directory
        debug_print(f"  Error: unable to create directory!\n   the specified directory, \"{temp_save_dir}\", couldn't be created.")
        return "break"
    
    debug_print(f"  Successfully created output directory \"{temp_save_dir}\"")
    
    # Writing sequence to txt file in save directory
    debug_print("\nWriting full sequence to file...")
    title = t_seq_name.get().strip().replace(" ", "_")
    sequence_file_write_results = create_file_ext(res_create_dir, "_" + title + "_full_sequence", ".txt", t_seq.get().strip().upper())
    
    if sequence_file_write_results:
        debug_print("  Successfully wrote full sequence to \"" + res_create_dir + "\"")
    else:
        debug_print("  Failed to write full sequence to \"" + res_create_dir + "\"")

    # Folding selected xmers
    debug_print("\nFolding selected xmers...")

    for xmer in v_sel_indicies.get():
        debug_print("\nFolding xmer index " + xmer[0] + ": " + xmer[1])
        try:
            # Creating thread to query ESMFold
            res_queue = queue.Queue()
            thread = threading.Thread(target=threaded_fold_sequence, args=(xmer[1], title + ": xmer #" + str(xmer[0]), res_queue))
            thread.start()
           
           # Waiting for thread to finish
            while thread.is_alive():
                debug_print("  Waiting...")
                time.sleep(1)
            
            thread.join()
            res_text = res_queue.get()

            if res_text == "**Exception**": # Thread exited with some exception
                debug_print("  Error: unable to send query to ESMFold! Please check your internet connection")
                continue
            elif res_text == "{\"message\": \"Endpoint request timed out\"}": # Response timed out
                debug_print("  Error: ESMFold endpoint request timed out! Please try again later")
                continue

            # Saving the result of the query to the save directory
            debug_print("  Result recieved\nSaving result to file...")
            res_title = title + "_" + str(xmer[0])
            write_res = create_file(res_create_dir, res_title, res_text)
            
            if write_res:
                debug_print("  Successfully wrote \"" + res_title + "\" to \"" + res_create_dir +"\"")
            else:
                debug_print("  Failed to write \"" + res_title + "\" to \"" + res_create_dir +"\"")

        except:
            debug_print("  Error: an unknown error occurred!")

    debug_print("\nDone\n")


# # Debug console events
# def on_sf_debug_configure(event):
#     c_debug.configure(scrollregion=c_debug.bbox("all"))
# sf_debug.bind("<Configure>", on_sf_debug_configure)

# def on_mouse_wheel(event):
#     c_debug.yview_scroll(int(-1*(event.delta/120)), "units")
# c_debug.bind_all("<MouseWheel>", on_mouse_wheel)


# =========================================================================
# Frame packing
# =========================================================================

f_input_section.pack(anchor="nw", padx=20, pady=5, fill='both', side="left", expand=True)
f_debug_section.pack(anchor="ne", padx=(20, 0), pady=(10,20), fill='both', side="left", expand=True)
f_seq_name.pack(anchor="nw", pady=5, fill='x', side="top")
f_save_dir.pack(anchor="nw", pady=5, fill='x', side="top")
f_seq.pack(anchor="nw", pady=5, fill='x', side="top")
f_xmer_len.pack(anchor="nw", pady=5, fill='x', side="top")
f_xmer_list.pack(anchor="nw", pady=5, fill='x', side="top")
f_sel_indicies.pack(anchor="nw", pady=5, fill='x', side="top")
f_fold_xmers.pack(anchor="nw", pady=5, fill='x', side="top")

window.mainloop()