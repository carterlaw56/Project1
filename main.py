import sys
import csv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui import VoteApp


class VoteManager:
    """Manages vote data, file I/O operations, and handles voting logic."""

    def __init__(self, filename: str = "votes.csv") -> None:
        self.__filename: str = filename
        self.__votes: dict[str, int] = {"Isabella": 0, "Genji": 0, "Hannah": 0, "Ira": 0}
        self.__load_data()

    def __load_data(self) -> None:
        """Loads previous vote counts from the CSV file if it exists."""
        try:
            with open(self.__filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        candidate, count = row
                        if candidate in self.__votes:
                            self.__votes[candidate] = int(count)
        except (FileNotFoundError, ValueError):
            pass

    def __save_data(self) -> None:
        """Saves the current dictionary of votes to the CSV file."""
        try:
            with open(self.__filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                for candidate, count in self.__votes.items():
                    writer.writerow([candidate, count])
        except Exception as e:
            print(f"Error saving data: {e}")

    def cast_vote(self, candidate: str) -> None:
        """Increments the vote count for a given candidate and saves to CSV."""
        if candidate in self.__votes:
            self.__votes[candidate] += 1
            self.__save_data()

    def get_results(self) -> str:
        """Returns a formatted string containing all current vote totals."""
        total = sum(self.__votes.values())
        results = [f"{c} - {v}" for c, v in self.__votes.items()]
        return ", ".join(results) + f"\n\nTotal Votes: {total}"


def main() -> None:
    """Main entry point for the Vote Counter application."""
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    # Initialize the data manager and pass it to the GUI
    data_manager = VoteManager()
    window = VoteApp(data_manager)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()