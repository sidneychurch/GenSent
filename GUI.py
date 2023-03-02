from tkinter import *
import tkinter.messagebox
import file_functions as ff
import tkinter.scrolledtext

# to get the window icon to work with pyinstaller the icon file
# must be in the same folder as the exe
icon = 'gensent.ico'


def launch_GUI():
    # -------- Main GUI Functions --------
    def set_text():
        num_words = entry_num.get()
        num_sentences = entry_sent.get()

        if not str.isdigit(num_words):
            tkinter.messagebox.showwarning(title="Value Error", message="Invalid Max Word Count Entered")
        elif not str.isdigit(num_sentences):
            tkinter.messagebox.showwarning(title="Value Error", message="Invalid Sentence Count Entered")
        else:
            ff.num_words_to_generate = int(num_words)
            num_sentences = int(num_sentences)
            text = ''

            if rhyme_check.get():
                output = ff.gen_rhyming_sentences(num_sentences)
            else:
                output = ff.gen_sentences(num_sentences)

            if space_check.get():
                spacing = '\n\n'
            else:
                spacing = '\n'

            for lines in output:
                text += lines + spacing

            text_box.configure(state='normal')
            text_box.delete(1.0, 'end')
            text_box.insert(1.0, text)
            text_box.configure(state='disabled')

    def copy_text():
        root.clipboard_clear()
        root.clipboard_append(text_box.get("1.0", 'end-1c'))

    # -------- Tkinter Main Window Setup --------
    root = Tk()
    root.minsize(width=450, height=220)
    root.resizable(width=False, height=False)
    root.title(" GenSent - Sentence Generator")
    root.iconbitmap(icon)

    menu_frame = Frame(root)
    left_frame = Frame(root, width=255)
    right_frame = Frame(root)
    btm_frame = Frame(root)

    menu_frame.grid(row=0, column=0, sticky="NEW")
    left_frame.grid(padx=2, pady=1, row=1, column=0, sticky="NW")
    right_frame.grid(padx=2, pady=1, row=1, column=1, sticky="NE")
    btm_frame.grid(padx=3, pady=2, row=2, column=0, columnspan=2, sticky="NSEW")

    # -------- Menu Bar Setup --------
    menu_bar = Menu(menu_frame)
    # ---- File Menu ----
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Load Dictionary', command=lambda: ff.load_dict(file_names, status_text))
    file_menu.add_command(label='Save Dictionary', command=lambda: ff.save_dict())
    file_menu.add_command(label='Quit', command=root.destroy)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # -------- Main GUI Layout--------
    # ---- GUI Variables ----
    file_names = StringVar(root, "Add at least one .txt file to generate a dictionary.")
    status_text = StringVar(root, "Waiting for File...")
    rhyme_check = IntVar(root, 0)
    space_check = IntVar(root, 0)

    # -------- Left Frame Setup --------

    # ---- Files Label ----
    lbl_files = Label(left_frame, justify=LEFT)
    lbl_files.config(textvariable=file_names)
    lbl_files.grid(row=0, column=0, columnspan=2, sticky="W")

    # ---- Add File Btn ----
    btn_add_file = Button(left_frame, command=lambda: ff.load_file(file_names, status_text), width=2, height=1)
    btn_add_file.config(text="+")
    btn_add_file.grid(row=1, column=0, sticky="W")

    # ---- Add Label ----
    lbl_add = Label(left_frame)
    lbl_add.config(text=' Add File...')
    lbl_add.grid(row=1, column=1, sticky="W")

    # ---- Spacer Label ----
    lbl_space = Label(left_frame)
    lbl_space.config(text='')
    lbl_space.grid(row=2, column=1, sticky="W")
    # ---- Num Sentence Label ----
    lbl_sent = Label(left_frame, text="Number of Sentences: ", justify=LEFT)
    lbl_sent.grid(row=3, column=0, sticky="W")

    # ---- Num Sentence Entry ----
    entry_sent = Entry(left_frame, width=3)
    entry_sent.grid(row=3, column=1, sticky="W")

    # ---- Word Count Label ----
    lbl_count = Label(left_frame, text="Max Words Per Sentence: ", justify=LEFT)
    lbl_count.grid(row=4, column=0, sticky="W")

    # ---- Word Count Entry ----
    entry_num = Entry(left_frame, width=3)
    entry_num.grid(row=4, column=1, sticky="W")

    # ---- Rhyme Label ----
    lbl_rhyme = Label(left_frame)
    lbl_rhyme.config(text="Generate Rhyming Sentences?")
    lbl_rhyme.grid(row=5, column=0, sticky="W")
    # ---- Rhyme Checkbox ----
    chk_rhyme = Checkbutton(left_frame, variable=rhyme_check, onvalue=1, offvalue=0)
    chk_rhyme.grid(row=5, column=1, sticky="W")

    # ---- Space Label ----
    lbl_rhyme = Label(left_frame)
    lbl_rhyme.config(text="Double-space Sentences?")
    lbl_rhyme.grid(row=6, column=0, sticky="W")
    # ---- Rhyme Checkbox ----
    chk_rhyme = Checkbutton(left_frame, variable=space_check, onvalue=1, offvalue=0)
    chk_rhyme.grid(row=6, column=1, sticky="W")

    # -------- Right Frame Setup --------
    # ---- Status Label ----
    lbl_dict_status = Label(right_frame, borderwidth=1, relief="groove", width=22, font=('bold italic', 9))
    lbl_dict_status.config(textvariable=status_text)
    lbl_dict_status.grid(padx=5, pady=5, row=0, column=0)

    # ---- Dict Btn ----
    btn_create_dict = Button(right_frame, command=lambda: ff.extract_words(status_text), width=15)
    btn_create_dict.config(text="Create Dictionary")
    btn_create_dict.grid(padx=5, pady=5, row=1, column=0)

    # ---- Gen Btn ----
    btn_gen = Button(right_frame, command=lambda: set_text(), width=15, state='normal')
    btn_gen.config(text="Generate Text")
    btn_gen.grid(padx=5, pady=5, row=2, column=0)

    # ---- Copy Btn ----
    btn_copy = Button(right_frame, command=lambda: copy_text(), width=15, state='normal')
    btn_copy.config(text="Copy Text")
    btn_copy.grid(padx=5, pady=5, row=3, column=0)

    # -------- Bottom Frame Setup --------

    # ---- Output Label ----
    lbl_output = Label(btm_frame)
    lbl_output.config(text="Generated Sentences:")
    lbl_output.grid(row=0, column=0,)

    # ---- Output Text Box ----
    text_box = tkinter.scrolledtext.ScrolledText(btm_frame, width=60)
    text_box.configure(padx=6, pady=3, wrap=WORD, state='disabled',
                       inactiveselectbackground=text_box.cget("selectbackground"))
    text_box.grid(row=1, column=0, sticky="NS")

    # -------- End Main Window --------
    root.config(menu=menu_bar)
    root.mainloop()
