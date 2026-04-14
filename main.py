from tkinter import *
from gui import Gui


def cast_vote(votes, candidate):
    if candidate == 1:
        votes['Isabella'] += 1
        votes['total'] += 1
        return 'Voted Isabella'
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


def get_results(votes):
    return (f"Isabella – {votes['Isabella']},  "
            f"Genji – {votes['Genji']},  "
            f"Hannah – {votes['Hannah']},  "
            f"Total – {votes['total']}")


def main():
    window = Tk()
    window.geometry('520x320')
    window.resizable(False, False)
    app = Gui(window, cast_vote, get_results)
    window.mainloop()


main()