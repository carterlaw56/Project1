# gui.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QButtonGroup, QStackedWidget, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class VoteApp(QWidget):
    """main gui."""

    def __init__(self, data_manager: 'VoteManager') -> None:
        """Initializes the main window, stores the data manager, and sets up the UI."""
        super().__init__()

        # Data hiding
        self._data_manager: 'VoteManager' = data_manager
        self._current_voter_id: str = ""
        self._current_candidate: str = ""

        self.setup_ui()

    def setup_ui(self) -> None:
        """Creates screen and layout."""
        self.setWindowTitle("Vote Counter")
        self.resize(320, 500)
        self.setStyleSheet("background-color: #1a0a14; color: #f9d4e8;")

        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("vote counter")
        title_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # widgets
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Main menu
        self.menu_page = QWidget()
        menu_layout = QVBoxLayout()

        menu_label = QLabel("MAIN MENU")
        menu_label.setFont(QFont("Georgia", 10, italic=True))
        menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(menu_label)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #a8f0c6; font-weight: bold;")
        menu_layout.addWidget(self.status_label)

        self.btn_goto_vote = QPushButton("VOTE")
        self.btn_goto_vote.setStyleSheet(
            "background-color: #5a0830; padding: 15px; font-weight: bold; border-radius: 5px;")
        self.btn_goto_vote.clicked.connect(self.show_id_page)
        menu_layout.addWidget(self.btn_goto_vote)

        self.btn_exit = QPushButton("EXIT / RESULTS")
        self.btn_exit.setStyleSheet(
            "background-color: #1e0a2e; padding: 15px; font-weight: bold; border-radius: 5px;")
        self.btn_exit.clicked.connect(self.exit_app)
        menu_layout.addWidget(self.btn_exit)

        self.menu_page.setLayout(menu_layout)
        self.stacked_widget.addWidget(self.menu_page)

        # Voter id check
        self.id_page = QWidget()
        id_layout = QVBoxLayout()

        id_label = QLabel("Voter Auth")
        id_label.setFont(QFont("Georgia", 10, italic=True))
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        id_layout.addWidget(id_label)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter 4-Digit Voter ID")
        self.id_input.setMaxLength(4)
        self.id_input.setStyleSheet(
            "background-color: #2d1228; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 10px;")
        self.id_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        id_layout.addWidget(self.id_input)

        self.id_error_label = QLabel("")
        self.id_error_label.setStyleSheet("color: #ff6666;")
        self.id_error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        id_layout.addWidget(self.id_error_label)

        self.btn_verify = QPushButton("CONTINUE")
        self.btn_verify.setStyleSheet(
            "background-color: #5a0830; padding: 10px; font-weight: bold; margin-top: 10px; border-radius: 5px;")
        self.btn_verify.clicked.connect(self.verify_id)
        id_layout.addWidget(self.btn_verify)

        self.btn_cancel_id = QPushButton("CANCEL")
        self.btn_cancel_id.setStyleSheet(
            "background-color: #333333; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.btn_cancel_id.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        id_layout.addWidget(self.btn_cancel_id)

        self.id_page.setLayout(id_layout)
        self.stacked_widget.addWidget(self.id_page)

        # voter page
        self.vote_page = QWidget()
        vote_layout = QVBoxLayout()

        cand_label = QLabel("CANDIDATE MENU")
        cand_label.setFont(QFont("Georgia", 10, italic=True))
        cand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vote_layout.addWidget(cand_label)

        self.candidate_group = QButtonGroup(self)
        self.box_isa = QPushButton("William Taft")
        self.box_gen = QPushButton("Margaret Thatcher")
        self.box_han = QPushButton("David")
        self.box_ira = QPushButton("Ira")

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

        for box in [self.box_isa, self.box_gen, self.box_han, self.box_ira]:
            box.setCheckable(True)
            box.setStyleSheet(box_style)
            box.setCursor(Qt.CursorShape.PointingHandCursor)
            vote_layout.addWidget(box)

        self.candidate_group.addButton(self.box_isa, 1)
        self.candidate_group.addButton(self.box_gen, 2)
        self.candidate_group.addButton(self.box_han, 3)
        self.candidate_group.addButton(self.box_ira, 4)

        self.btn_submit = QPushButton("submit...")
        self.btn_submit.setStyleSheet(
            "background-color: #5a0830; padding: 10px; font-weight: bold; margin-top: 10px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_vote)
        vote_layout.addWidget(self.btn_submit)

        self.btn_cancel_vote = QPushButton("CANCEL")
        self.btn_cancel_vote.setStyleSheet(
            "background-color: #333333; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.btn_cancel_vote.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        vote_layout.addWidget(self.btn_cancel_vote)

        self.vote_page.setLayout(vote_layout)
        self.stacked_widget.addWidget(self.vote_page)

        # deter anti-ira voters
        self.confirm_page = QWidget()
        confirm_layout = QVBoxLayout()

        self.confirm_label = QLabel("")
        self.confirm_label.setWordWrap(True)
        self.confirm_label.setFont(QFont("Georgia", 11, italic=True))
        self.confirm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        confirm_layout.addWidget(self.confirm_label)

        self.btn_yes = QPushButton("yes")
        self.btn_yes.setStyleSheet(
            "background-color: #5a0830; padding: 15px; font-weight: bold; border-radius: 5px; margin-top: 20px;")
        self.btn_yes.clicked.connect(self.confirm_yes)
        confirm_layout.addWidget(self.btn_yes)

        self.btn_no = QPushButton("no, VOTE IRA INSTEAD")
        self.btn_no.setStyleSheet("background-color: #1e0a2e; padding: 15px; font-weight: bold; border-radius: 5px;")
        self.btn_no.clicked.connect(self.confirm_no)
        confirm_layout.addWidget(self.btn_no)
        self.confirm_page.setLayout(confirm_layout)
        self.stacked_widget.addWidget(self.confirm_page)

        # show results
        self.results_page = QWidget()
        results_layout = QVBoxLayout()

        results_title = QLabel("final result")
        results_title.setFont(QFont("Georgia", 12, QFont.Weight.Bold))
        results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        results_layout.addWidget(results_title)

        self.results_label = QLabel("")
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setFont(QFont("Georgia", 12))
        results_layout.addWidget(self.results_label)

        self.btn_close = QPushButton("close application")
        self.btn_close.setStyleSheet(
            "background-color: #5a0830; padding: 15px; font-weight: bold; border-radius: 5px; margin-top: 20px;")
        self.btn_close.clicked.connect(self.close)
        results_layout.addWidget(self.btn_close)

        self.results_page.setLayout(results_layout)
        self.stacked_widget.addWidget(self.results_page)
        self.setLayout(main_layout)

    def show_id_page(self) -> None:
        """clear previous inputs."""
        self.id_input.clear()
        self.id_error_label.setText("")
        self.status_label.setText("")
        self.stacked_widget.setCurrentIndex(1)

    def verify_id(self) -> None:
        """Validates the entered voter ID."""
        voter_id = self.id_input.text().strip()
        if not voter_id.isdigit() or len(voter_id) != 4:
            self.id_error_label.setText("id must be 4 numbers.")
            return

        if self._data_manager.has_voted(voter_id):
            self.id_error_label.setText("Error: vote id alr voted.")
            return

        self._current_voter_id = voter_id
        self.box_ira.setChecked(True)  # Default vote Ira
        self.stacked_widget.setCurrentIndex(2)

    def submit_vote(self) -> None:
        """Reads the selected candidate"""
        selected_id = self.candidate_group.checkedId()
        candidate_map = {1: "William Taft", 2: "Margaret Thatcher", 3: "David", 4: "Ira"}
        candidate = candidate_map.get(selected_id)

        self._current_candidate = candidate

        if candidate != "Ira":
            self.confirm_label.setText(
                f"\n\n you SURE you want to vote for {candidate}?")
            self.stacked_widget.setCurrentIndex(3)
        else:
            self.finalize_vote(candidate)

    def confirm_yes(self) -> None:
        """proceeds vote."""
        self.finalize_vote(self._current_candidate)

    def confirm_no(self) -> None:
        """gives the vote to ira."""
        self.finalize_vote("Ira")

    def finalize_vote(self, candidate: str) -> None:
        """saves the vote and gives to csv writer data manager."""
        self._data_manager.cast_vote(candidate, self._current_voter_id)
        self.status_label.setText(f"Success: Vote saved for {candidate}!")
        self.stacked_widget.setCurrentIndex(0)

    def exit_app(self) -> None:
        """pulls voting data from csv or stored data."""
        results = self._data_manager.get_results()
        self.results_label.setText(results)
        self.stacked_widget.setCurrentIndex(4)