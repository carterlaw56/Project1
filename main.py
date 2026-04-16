from tkinter import *
from gui import Gui

#function to allow vote to be casted, and create the people to vote for
def cast_vote(votes, candidate):
    if candidate == 1:
        votes['Ira'] += 1
        votes['total'] += 1
        return 'Voted Ira'
    elif candidate == 2:
        votes['Genji'] += 1
        votes['total'] += 1
        return 'Voted Genji'
    elif candidate == 3:
        votes['Hannah'] += 1
        votes['total'] += 1
        return 'Voted Hannah'
    else:
        return 'Please select a candidate'

#return then display the votes for the candidates
def get_results(votes):
    return (f"Ira – {votes['Ira']},  "
            f"Genji – {votes['Genji']},  "
            f"Hannah – {votes['Hannah']},  "
            f"Total – {votes['total']}")

#create window, define shape and make it NOT resizable :)
def main():
    window = Tk()
    window.geometry('520x320')
    window.resizable(False, False)
    app = Gui(window, cast_vote, get_results)
    window.mainloop()


main()