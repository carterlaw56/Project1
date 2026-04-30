import sys
import csv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui import VoteApp


class VoteManager:
    # handle csv, voting, and id tracking
    def __init__(self, filename="votes.csv", ids_filename="voted_ids.txt"):
        self.filename = filename
        self.ids_filename = ids_filename
        self.votes = {"William Taft": 0, "Margaret Thatcher": 0, "David": 0, "Ira": 0}
        self.voted_ids = set()

        self.load_data()
        self.load_ids()

    def load_data(self):
        # check to see if voting information was already saved, and then load it in
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        candidate, count = row
                        if candidate in self.votes:
                            self.votes[candidate] = int(count)
        except (FileNotFoundError, ValueError):
            pass

    def save_data(self):
        # save the data to csv file
        try:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                for candidate, count in self.votes.items():
                    writer.writerow([candidate, count])
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_ids(self):
        # load in previously used voter ids
        try:
            with open(self.ids_filename, mode='r') as file:
                for line in file:
                    self.voted_ids.add(line.strip())
        except (FileNotFoundError, ValueError):
            pass

    def save_ids(self):
        # save used ids so they can't vote again next time
        try:
            with open(self.ids_filename, mode='w') as file:
                for vid in self.voted_ids:
                    file.write(f"{vid}\n")
        except Exception as e:
            print(f"Error saving ids: {e}")

    def has_voted(self, voter_id):
        # check if id exists
        return voter_id in self.voted_ids

    def cast_vote(self, candidate, voter_id):
        # tally the vote counts and register the ID
        if candidate in self.votes and voter_id not in self.voted_ids:
            self.votes[candidate] += 1
            self.voted_ids.add(voter_id)
            self.save_data()
            self.save_ids()

    def get_results(self):
        # returns f string for voting result
        total = sum(self.votes.values())
        results = [f"{c} - {v}" for c, v in self.votes.items()]
        return "\n".join(results) + f"\n\nTotal Votes: {total}"


def main():
    # main app
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    # pass window manager to the gui app
    data_manager = VoteManager()
    window = VoteApp(data_manager)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()