from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QMessageBox, QButtonGroup, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class VoteApp(QWidget):
    """Main GUI class for the Vote Counter application using PyQt6."""

    def __init__(self, data_manager) -> None:
        """Initializes the window, layout, and connects to the Data Manager."""
        super().__init__()
        self.__data_manager = data_manager
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """Initializes the UI, including a stacked layout for switching screens."""
        self.setWindowTitle("Vote Counter")
        self.resize(320, 420)  # Made the window slightly taller to fit the big boxes
        self.setStyleSheet("background-color: #1a0a14; color: #f9d4e8;")

        main_layout = QVBoxLayout()

        # Title Header
        title_label = QLabel("VOTE COUNTER")
        title_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # The Stacked Widget allows us to switch between the Menu and the Voting Booth
        self.__stacked_widget = QStackedWidget()
        main_layout.addWidget(self.__stacked_widget)

        # ================= PAGE 0: MAIN MENU =================
        self.__menu_page = QWidget()
        menu_layout = QVBoxLayout()

        menu_label = QLabel("MAIN MENU")
        menu_label.setFont(QFont("Georgia", 10, italic=True))
        menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(menu_label)

        self.__btn_goto_vote = QPushButton("VOTE")
        self.__btn_goto_vote.setStyleSheet(
            "background-color: #5a0830; padding: 15px; font-weight: bold; border-radius: 5px;")
        self.__btn_goto_vote.clicked.connect(self.__show_voting_page)
        menu_layout.addWidget(self.__btn_goto_vote)

        self.__btn_exit = QPushButton("EXIT")
        self.__btn_exit.setStyleSheet(
            "background-color: #1e0a2e; padding: 15px; font-weight: bold; border-radius: 5px;")
        self.__btn_exit.clicked.connect(self.__exit_app)
        menu_layout.addWidget(self.__btn_exit)

        self.__menu_page.setLayout(menu_layout)
        self.__stacked_widget.addWidget(self.__menu_page)

        # ================= PAGE 1: VOTING BOOTH =================
        self.__vote_page = QWidget()
        vote_layout = QVBoxLayout()

        cand_label = QLabel("CANDIDATE MENU")
        cand_label.setFont(QFont("Georgia", 10, italic=True))
        cand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vote_layout.addWidget(cand_label)

        self.__candidate_group = QButtonGroup(self)

        # Switched from QRadioButton to QPushButton to create "Boxes"
        self.__box_isa = QPushButton("Isabella")
        self.__box_gen = QPushButton("Genji")
        self.__box_han = QPushButton("Hannah")
        self.__box_ira = QPushButton("Ira")

        # Styling to make them look like clickable cards that light up when checked
        box_style = """
            QPushButton {
                background-color: #2d1228;
                color: #f9d4e8;
                border: 2px solid #5a0830;
                border-radius: 8px;
                padding: 12px;
                font-family: Georgia;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #8b1a4a;
                border: 2px solid #ffb3d9;
                color: #ffffff;
            }
            QPushButton:hover:!checked {
                background-color: #3d1b38;
            }
        """

        # Apply styling and properties to all candidate boxes
        for box in [self.__box_isa, self.__box_gen, self.__box_han, self.__box_ira]:
            box.setCheckable(True)  # This is the magic that makes it toggle like a radio button
            box.setStyleSheet(box_style)
            box.setCursor(Qt.CursorShape.PointingHandCursor)
            vote_layout.addWidget(box)

        # Map IDs to the buttons
        self.__candidate_group.addButton(self.__box_isa, 1)
        self.__candidate_group.addButton(self.__box_gen, 2)
        self.__candidate_group.addButton(self.__box_han, 3)
        self.__candidate_group.addButton(self.__box_ira, 4)

        self.__btn_submit = QPushButton("SUBMIT VOTE")
        self.__btn_submit.setStyleSheet(
            "background-color: #5a0830; padding: 10px; font-weight: bold; margin-top: 10px; border-radius: 5px;")
        self.__btn_submit.clicked.connect(self.__submit_vote)
        vote_layout.addWidget(self.__btn_submit)

        self.__btn_cancel = QPushButton("CANCEL")
        self.__btn_cancel.setStyleSheet(
            "background-color: #333333; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.__btn_cancel.clicked.connect(lambda: self.__stacked_widget.setCurrentIndex(0))
        vote_layout.addWidget(self.__btn_cancel)

        self.__vote_page.setLayout(vote_layout)
        self.__stacked_widget.addWidget(self.__vote_page)

        self.setLayout(main_layout)

    def __show_voting_page(self) -> None:
        """Transitions to the voting page and defaults the selection to Ira."""
        self.__box_ira.setChecked(True)
        self.__stacked_widget.setCurrentIndex(1)

    def __submit_vote(self) -> None:
        """Handles vote submission, applies the Ira logic, and saves the result."""
        selected_id = self.__candidate_group.checkedId()

        # Map the ID back to the name
        candidate_map = {1: "Isabella", 2: "Genji", 3: "Hannah", 4: "Ira"}
        candidate = candidate_map.get(selected_id)

        # The core logic rule requested: if not Ira, ask if they are sure.
        if candidate != "Ira":
            reply = QMessageBox.question(self, "Hold on a second...",
                                         f"Are you SURE you want to vote for {candidate} instead of Ira?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            # If they say No, override their vote to Ira
            if reply == QMessageBox.StandardButton.No:
                candidate = "Ira"

        # Record vote via Data Manager
        self.__data_manager.cast_vote(candidate)
        QMessageBox.information(self, "Success", f"Vote recorded for {candidate}!")

        # Return to main menu page after voting
        self.__stacked_widget.setCurrentIndex(0)

    def __exit_app(self) -> None:
        """Shows the final results message box and then closes the application."""
        results = self.__data_manager.get_results()
        QMessageBox.information(self, "Final Results", results)
        self.close()