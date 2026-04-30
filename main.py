# main.py
import sys
import csv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui import VoteApp


class VoteManager:
    """Handles CSV file operations, voting tallies, and voter ID tracking."""

    def __init__(self, filename: str = "votes.csv", ids_filename: str = "voted_ids.txt") -> None:
        """Initializes the VoteManager with target files and empty data structures."""
        # Data hiding: using protected variables (prefixed with _)
        self._filename: str = filename
        self._ids_filename: str = ids_filename
        self._votes: dict[str, int] = {"William Taft": 0, "Margaret Thatcher": 0, "David": 0, "Ira": 0}
        self._voted_ids: set[str] = set()

        self.load_data()
        self.load_ids()

    def load_data(self) -> None:
        """Checks if voting information was already saved and loads it into the dictionary."""
        try:
            with open(self._filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        candidate, count = row
                        if candidate in self._votes:
                            self._votes[candidate] = int(count)
        except (FileNotFoundError, ValueError):
            pass

    def save_data(self) -> None:
        """Saves the current vote tallies to the specified CSV file."""
        try:
            with open(self._filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                for candidate, count in self._votes.items():
                    writer.writerow([candidate, count])
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_ids(self) -> None:
        """Loads previously used voter IDs from the text file into the set."""
        try:
            with open(self._ids_filename, mode='r') as file:
                for line in file:
                    self._voted_ids.add(line.strip())
        except (FileNotFoundError, ValueError):
            pass

    def save_ids(self) -> None:
        """Saves the set of used voter IDs to the text file to prevent duplicate voting."""
        try:
            with open(self._ids_filename, mode='w') as file:
                for vid in self._voted_ids:
                    file.write(f"{vid}\n")
        except Exception as e:
            print(f"Error saving ids: {e}")

    def has_voted(self, voter_id: str) -> bool:
        """Checks if a given voter ID exists in the set of already voted IDs."""
        return voter_id in self._voted_ids

    def cast_vote(self, candidate: str, voter_id: str) -> None:
        """Tallies the vote for the given candidate and registers the voter ID."""
        if candidate in self._votes and voter_id not in self._voted_ids:
            self._votes[candidate] += 1
            self._voted_ids.add(voter_id)
            self.save_data()
            self.save_ids()

    def get_results(self) -> str:
        """Returns a formatted string containing the voting results and total vote count."""
        total = sum(self._votes.values())
        results = [f"{c} - {v}" for c, v in self._votes.items()]
        return "\n".join(results) + f"\n\nTotal Votes: {total}"


def main() -> None:
    """Main execution block to launch the PyQt6 application."""
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    # Pass window manager to the gui app
    data_manager = VoteManager()
    window = VoteApp(data_manager)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()