import ctypes
from tkinter import *
from gui import Gui

# stop it from being blurry
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# process the decision making
def cast_vote(votes, candidate):
    if candidate == 1:
        votes['Isabella'] += 1
        votes['total'] += 1
        return 'Voted for Isabella'
    elif candidate == 2:
        votes['Genji'] += 1
        votes['total'] += 1
        return 'Voted for Genji'
    elif candidate == 3:
        votes['Hannah'] += 1
        votes['total'] += 1
        return 'Voted for Hannah'
    elif candidate == 4:
        votes['Ira'] += 1
        votes['total'] += 1
        return 'Voted for Ira'
    else:
        return 'Please select a candidate'

# return then display the votes for the candidates
def get_results(votes):
    return (f"Isabella – {votes['Isabella']},  "
            f"Genji – {votes['Genji']},  "
            f"Hannah – {votes['Hannah']},  "
            f"Ira – {votes['Ira']}\n"
            f"Total Votes – {votes['total']}")

#define the main window for the application
def main():
    window = Tk()
    window.geometry('520x320')
    window.resizable(False, False)
    app = Gui(window, cast_vote, get_results)
    window.mainloop()

# start main function
if __name__ == '__main__':
    main()