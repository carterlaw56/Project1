from tkinter import *
from tkinter import messagebox

# define the class and intitialize
class Gui:
    def __init__(self, window, cast_vote, get_results):
        self.window = window
        self.window.title('Vote Counter')
        self.window.configure(bg='#1a0a14')

        self.cast_vote = cast_vote
        self.get_results = get_results

        self.votes = {'Isabella': 0, 'Genji': 0, 'Hannah': 0, 'Ira': 0, 'total': 0}

        # containers for the buttons
        self.top_container = Frame(self.window, bg='#1a0a14')
        self.top_container.pack(side=TOP, fill=X, pady=(5, 0))

        self.middle_container = Frame(self.window, bg='#1a0a14')
        self.middle_container.pack(side=TOP, fill=X, pady=2)

        self.bottom_container = Frame(self.window, bg='#1a0a14')
        self.bottom_container.pack(side=TOP, fill=X, pady=(5, 0))

        # set up vote menu
        self.frame_title = Frame(self.top_container, bg='#1a0a14')
        self.label_title = Label(self.frame_title, text='  VOTE COUNTER  ',
                                 bg='#1a0a14', fg='#f9d4e8',
                                 font=('Georgia', 14, 'bold'))
        self.label_subtitle = Label(self.frame_title, text='- - - - - - - - - - - - - - - - - -',
                                    bg='#1a0a14', fg='#c77aaa',
                                    font=('Georgia', 8))
        self.label_title.pack(pady=(0, 0))
        self.label_subtitle.pack()
        self.frame_title.pack()

        self.label_menu = Label(self.top_container, text='VOTE MENU',
                                bg='#1a0a14', fg='#c77aaa',
                                font=('Georgia', 9, 'italic'))
        self.label_menu.pack(pady=(5, 0))

        self.frame_option = Frame(self.top_container, bg='#1a0a14')
        self.radio_1 = IntVar()
        self.radio_1.set(0)

#set the radio buttons
        self.radio_vote = Radiobutton(self.frame_option, text='  v: Vote',
                                      variable=self.radio_1, value=1, command=self.show_candidates,
                                      bg='#2d1228', fg='#ffd6ea', selectcolor='#8b1a4a',
                                      activebackground='#2d1228', activeforeground='#ffd6ea',
                                      font=('Georgia', 10, 'bold'), width=12, anchor='w',
                                      relief='groove', bd=2, padx=5, pady=4, indicatoron=0)

        self.radio_exit = Radiobutton(self.frame_option, text='  x: Exit',
                                      variable=self.radio_1, value=2, command=self.show_results,
                                      bg='#1e0a2e', fg='#e8c8ff', selectcolor='#4a1a5e',
                                      activebackground='#1e0a2e', activeforeground='#e8c8ff',
                                      font=('Georgia', 10, 'bold'), width=12, anchor='w',
                                      relief='groove', bd=2, padx=5, pady=4, indicatoron=0)

        self.radio_vote.grid(row=0, column=0, padx=5, pady=2, ipadx=2)
        self.radio_exit.grid(row=0, column=1, padx=5, pady=2, ipadx=2)
        self.frame_option.pack()

        # create the menu to display candidates
        self.label_cand_menu = Label(self.middle_container, text='CANDIDATE MENU',
                                     bg='#1a0a14', fg='#c77aaa',
                                     font=('Georgia', 9, 'italic'))

        self.frame_candidate = Frame(self.middle_container, bg='#1a0a14')
        self.radio_2 = IntVar()
        self.radio_2.set(0)

        self.radio_isabella = Radiobutton(self.frame_candidate, text=' 1: Isabella',
                                          variable=self.radio_2, value=1,
                                          bg='#2d1228', fg='#f9d4e8', selectcolor='#7a1a4a',
                                          activebackground='#2d1228', activeforeground='#f9d4e8',
                                          font=('Georgia', 9, 'bold'), width=11, anchor='w',
                                          relief='groove', bd=2, padx=5, pady=4, indicatoron=0)

        self.radio_genji = Radiobutton(self.frame_candidate, text=' 2: Genji',
                                       variable=self.radio_2, value=2,
                                       bg='#2d1228', fg='#f9d4e8', selectcolor='#7a1a4a',
                                       activebackground='#2d1228', activeforeground='#f9d4e8',
                                       font=('Georgia', 9, 'bold'), width=11, anchor='w',
                                       relief='groove', bd=2, padx=5, pady=4, indicatoron=0)

        self.radio_hannah = Radiobutton(self.frame_candidate, text=' 3: Hannah',
                                        variable=self.radio_2, value=3,
                                        bg='#2d1228', fg='#f9d4e8', selectcolor='#7a1a4a',
                                        activebackground='#2d1228', activeforeground='#f9d4e8',
                                        font=('Georgia', 9, 'bold'), width=11, anchor='w',
                                        relief='groove', bd=2, padx=5, pady=4, indicatoron=0)

        self.radio_ira = Radiobutton(self.frame_candidate, text=' 4: Ira',
                                     variable=self.radio_2, value=4,
                                     bg='#2d1228', fg='#f9d4e8', selectcolor='#7a1a4a',
                                     activebackground='#2d1228', activeforeground='#f9d4e8',
                                     font=('Georgia', 9, 'bold'), width=11, anchor='w',
                                     relief='groove', bd=2, padx=5, pady=4, indicatoron=0)

        self.radio_isabella.grid(row=0, column=0, padx=4, pady=2, ipadx=2)
        self.radio_genji.grid(row=0, column=1, padx=4, pady=2, ipadx=2)
        self.radio_hannah.grid(row=1, column=0, padx=4, pady=2, ipadx=2)
        self.radio_ira.grid(row=1, column=1, padx=4, pady=2, ipadx=2)

        # create the submit, vote, etc buttons
        self.label_result = Label(self.bottom_container, text='',
                                  bg='#1a0a14', fg='#f9d4e8',
                                  font=('Georgia', 10, 'bold'),
                                  wraplength=460, justify='center')
        self.label_result.pack(pady=(0, 5))

        self.button_submit = Button(self.bottom_container, text='SUBMIT',
                                    command=self.compute,
                                    bg='#5a0830', fg='#f9d4e8',
                                    font=('Georgia', 10, 'bold'),
                                    relief='flat', padx=20, pady=4,
                                    activebackground='#7a1a4a',
                                    activeforeground='#ffffff',
                                    cursor='hand2')
        self.button_submit.pack()

# function to show the candidates
    def show_candidates(self):
        self.label_result.config(text='')
        self.radio_2.set(4)  # Ira is the default candidate for the user to choose in
        self.label_cand_menu.pack()
        self.frame_candidate.pack()

    def show_results(self):
        self.label_cand_menu.pack_forget()
        self.frame_candidate.pack_forget()
        result = self.get_results(self.votes)
        self.label_result.config(text=result)

    def compute(self):
        option = self.radio_1.get()

        if option == 1:
            candidate = self.radio_2.get()

# ask the user if they are truly they don't wanna vote for ira & create messagebox
            if candidate in [1, 2, 3]:
                names = {1: 'Isabella', 2: 'Genji', 3: 'Hannah'}
                is_sure = messagebox.askyesno("Hold on a second...",
                                              f"Are you SURE you want to vote for {names[candidate]} instead of Ira?")
                if not is_sure:
                    candidate = 4

            message = self.cast_vote(self.votes, candidate)
            self.label_result.config(text=message)
            self.radio_1.set(0)
#set default to ira
            self.radio_2.set(4)
            self.label_cand_menu.pack_forget()
            self.frame_candidate.pack_forget()

        elif option == 2:
            self.show_results()
        else:
            self.label_result.config(text='Please select an option.')