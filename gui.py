from tkinter import *


class Gui:
    def __init__(self, window, cast_vote, get_results):
        self.window = window
        self.window.title('Vote Counter')
        self.window.configure(bg='#1a0a14')

        self.cast_vote = cast_vote
        self.get_results = get_results

        self.votes = {'Isabella': 0, 'Genji': 0, 'Hannah': 0, 'total': 0}

        # Title
        self.frame_title = Frame(self.window, bg='#1a0a14')
        self.label_title = Label(self.frame_title, text='🌸  VOTE COUNTER  🌸',
                                 bg='#1a0a14', fg='#f9d4e8',
                                 font=('Georgia', 18, 'bold'))
        self.label_subtitle = Label(self.frame_title, text='- - - - - - - - - - - - - - - - - -',
                                    bg='#1a0a14', fg='#c77aaa',
                                    font=('Georgia', 10))
        self.label_title.pack(pady=(5, 2))
        self.label_subtitle.pack()
        self.frame_title.pack(pady=10)

        # Vote menu label
        self.frame_menu_label = Frame(self.window, bg='#1a0a14')
        self.label_menu = Label(self.frame_menu_label, text='VOTE MENU',
                                bg='#1a0a14', fg='#c77aaa',
                                font=('Georgia', 10, 'italic'))
        self.label_menu.pack()
        self.frame_menu_label.pack()

        # Vote / Exit buttons in a grid, no radio indicator
        self.frame_option = Frame(self.window, bg='#1a0a14')
        self.radio_1 = IntVar()
        self.radio_1.set(0)

        self.radio_vote = Radiobutton(self.frame_option, text='🗳   v : Vote',
                                      variable=self.radio_1, value=1,
                                      command=self.show_candidates,
                                      bg='#2d1228', fg='#ffd6ea',
                                      selectcolor='#8b1a4a',
                                      activebackground='#2d1228',
                                      activeforeground='#ffd6ea',
                                      font=('Georgia', 12, 'bold'),
                                      width=14, anchor='w',
                                      relief='groove', bd=2,
                                      padx=10, pady=8,
                                      indicatoron=0)

        self.radio_exit = Radiobutton(self.frame_option, text='✖   x : Exit',
                                      variable=self.radio_1, value=2,
                                      command=self.show_results,
                                      bg='#1e0a2e', fg='#e8c8ff',
                                      selectcolor='#4a1a5e',
                                      activebackground='#1e0a2e',
                                      activeforeground='#e8c8ff',
                                      font=('Georgia', 12, 'bold'),
                                      width=14, anchor='w',
                                      relief='groove', bd=2,
                                      padx=10, pady=8,
                                      indicatoron=0)

        self.radio_vote.grid(row=0, column=0, padx=10, pady=5, ipadx=5)
        self.radio_exit.grid(row=0, column=1, padx=10, pady=5, ipadx=5)
        self.frame_option.pack(pady=10)

        # Candidate menu label (hidden until vote is selected)
        self.frame_cand_label = Frame(self.window, bg='#1a0a14')
        self.label_cand_menu = Label(self.frame_cand_label, text='CANDIDATE MENU',
                                     bg='#1a0a14', fg='#c77aaa',
                                     font=('Georgia', 10, 'italic'))
        self.label_cand_menu.pack()
        self.frame_cand_label.pack()
        self.frame_cand_label.pack_forget()

        # Candidate buttons in a grid, no radio indicator
        self.frame_candidate = Frame(self.window, bg='#1a0a14')
        self.radio_2 = IntVar()
        self.radio_2.set(0)

        self.radio_isabella = Radiobutton(self.frame_candidate, text='🌷  1 : Isabella',
                                          variable=self.radio_2, value=1,
                                          bg='#2d1228', fg='#f9d4e8',
                                          selectcolor='#7a1a4a',
                                          activebackground='#2d1228',
                                          activeforeground='#f9d4e8',
                                          font=('Georgia', 11, 'bold'),
                                          width=13, anchor='w',
                                          relief='groove', bd=2,
                                          padx=10, pady=8,
                                          indicatoron=0)

        self.radio_genji = Radiobutton(self.frame_candidate, text='🌙  2 : Genji',
                                       variable=self.radio_2, value=2,
                                       bg='#2d1228', fg='#f9d4e8',
                                       selectcolor='#7a1a4a',
                                       activebackground='#2d1228',
                                       activeforeground='#f9d4e8',
                                       font=('Georgia', 11, 'bold'),
                                       width=13, anchor='w',
                                       relief='groove', bd=2,
                                       padx=10, pady=8,
                                       indicatoron=0)

        self.radio_hannah = Radiobutton(self.frame_candidate, text='✨  3 : Hannah',
                                        variable=self.radio_2, value=3,
                                        bg='#2d1228', fg='#f9d4e8',
                                        selectcolor='#7a1a4a',
                                        activebackground='#2d1228',
                                        activeforeground='#f9d4e8',
                                        font=('Georgia', 11, 'bold'),
                                        width=13, anchor='w',
                                        relief='groove', bd=2,
                                        padx=10, pady=8,
                                        indicatoron=0)

        self.radio_isabella.grid(row=0, column=0, padx=8, pady=5, ipadx=5)
        self.radio_genji.grid(row=0, column=1, padx=8, pady=5, ipadx=5)
        self.radio_hannah.grid(row=0, column=2, padx=8, pady=5, ipadx=5)
        self.frame_candidate.pack(pady=5)
        self.frame_candidate.pack_forget()

        # Result label
        self.frame_result = Frame(self.window, bg='#1a0a14')
        self.label_result = Label(self.frame_result, text='',
                                  bg='#1a0a14', fg='#f9d4e8',
                                  font=('Georgia', 12),
                                  wraplength=460, justify='center')
        self.label_result.pack(pady=5)
        self.frame_result.pack()

        # Submit button
        self.frame_button = Frame(self.window, bg='#1a0a14')
        self.button_submit = Button(self.frame_button, text='SUBMIT',
                                    command=self.compute,
                                    bg='#3a0520', fg='#3a0520',
                                    font=('Georgia', 11, 'bold'),
                                    relief='flat', padx=20, pady=6,
                                    activebackground='#5a0830',
                                    activeforeground='#ffffff',
                                    cursor='hand2')
        self.button_submit.pack(pady=10)
        self.frame_button.pack()

    def show_candidates(self):
        self.label_result.config(text='')
        self.radio_2.set(0)
        self.frame_cand_label.pack()
        self.frame_candidate.pack(pady=5)

    def show_results(self):
        self.frame_cand_label.pack_forget()
        self.frame_candidate.pack_forget()
        result = self.get_results(self.votes)
        self.label_result.config(text=result)

    def compute(self):
        option = self.radio_1.get()

        if option == 1:
            candidate = self.radio_2.get()
            message = self.cast_vote(self.votes, candidate)
            self.label_result.config(text=message)
            self.radio_1.set(0)
            self.radio_2.set(0)
            self.frame_cand_label.pack_forget()
            self.frame_candidate.pack_forget()
        elif option == 2:
            self.show_results()
        else:
            self.label_result.config(text='Please select an option')