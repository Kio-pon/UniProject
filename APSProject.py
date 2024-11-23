import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QPlainTextEdit, QListWidget,
    QTextBrowser, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
import subprocess
import json
import os
from datetime import datetime

class User:
    def __init__(self, username):
        self.username = username
        self.solved_problems = set()
        self.current_streak = 0
        
    def solve_problem(self, problem_id):
        self.solved_problems.add(problem_id)
        self.current_streak += 1

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Coding Practice App")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin: 20px;")
        layout.addWidget(title)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 5px; margin: 5px;")
        layout.addWidget(self.username_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 5px; margin: 5px;")
        layout.addWidget(self.password_input)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("padding: 8px; margin: 5px;")
        layout.addWidget(self.login_button)
        
        # Sign up button
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setStyleSheet("padding: 8px; margin: 5px;")
        layout.addWidget(self.signup_button)
        
        layout.addStretch()
        self.setLayout(layout)

class ProblemSelectionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.problems = [
            {"id": 1, "title": "Sum Two Numbers", "difficulty": "Easy",
             "description": "Write a function that returns the sum of two numbers.",
             "test_case": "assert add(2, 3) == 5"},
            {"id": 2, "title": "Fibonacci Sequence", "difficulty": "Medium",
             "description": "Write a function that returns the nth number in the Fibonacci sequence.",
             "test_case": "assert fib(5) == 5"},
            {"id": 3, "title": "Binary Search", "difficulty": "Hard",
             "description": "Implement binary search algorithm.",
             "test_case": "assert binary_search([1,2,3,4,5], 3) == 2"}
        ]
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Select a Problem")
        header.setStyleSheet("font-size: 20px; margin: 10px;")
        layout.addWidget(header)
        
        # Problem list
        self.problem_list = QListWidget()
        for problem in self.problems:
            self.problem_list.addItem(f"{problem['title']} - {problem['difficulty']}")
        layout.addWidget(self.problem_list)
        
        # Start button
        self.start_button = QPushButton("Start Problem")
        self.start_button.setStyleSheet("padding: 8px; margin: 5px;")
        layout.addWidget(self.start_button)
        
        # Progress section
        progress_layout = QHBoxLayout()
        self.problems_solved = QLabel("Problems Solved: 0")
        self.current_streak = QLabel("Current Streak: 0")
        progress_layout.addWidget(self.problems_solved)
        progress_layout.addWidget(self.current_streak)
        layout.addLayout(progress_layout)
        
        self.setLayout(layout)

class CodingWorkspace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_problem = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Problem description
        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setStyleSheet("background-color: #f0f0f0; padding: 10px; margin: 5px;")
        layout.addWidget(self.description)
        
        # Code editor
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("# Write your code here")
        self.editor.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Code")
        self.submit_button = QPushButton("Submit Solution")
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.submit_button)
        layout.addLayout(button_layout)
        
        # Output console
        self.output = QTextBrowser()
        self.output.setStyleSheet("background-color: #f0f0f0; font-family: monospace;")
        layout.addWidget(self.output)
        
        self.setLayout(layout)
        
    def set_problem(self, problem):
        self.current_problem = problem
        self.description.setText(f"{problem['title']}\n\n{problem['description']}")
        self.editor.clear()
        self.output.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coding Practice App")
        self.setGeometry(100, 100, 800, 600)
        self.current_user = None
        
        # Create the stacked widget and screens
        self.stack = QStackedWidget()
        self.login_screen = LoginScreen()
        self.problem_screen = ProblemSelectionScreen()
        self.coding_screen = CodingWorkspace()
        
        # Add screens to stack
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.problem_screen)
        self.stack.addWidget(self.coding_screen)
        
        # Set the central widget
        self.setCentralWidget(self.stack)
        
        # Connect signals
        self.login_screen.login_button.clicked.connect(self.handle_login)
        self.login_screen.signup_button.clicked.connect(self.handle_signup)
        self.problem_screen.start_button.clicked.connect(self.start_problem)
        self.coding_screen.run_button.clicked.connect(self.run_code)
        self.coding_screen.submit_button.clicked.connect(self.submit_solution)
        
    def handle_login(self):
        username = self.login_screen.username_input.text()
        password = self.login_screen.password_input.text()
        
        if username and password:  # Simple validation
            self.current_user = User(username)
            self.stack.setCurrentWidget(self.problem_screen)
        else:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
    
    def handle_signup(self):
        username = self.login_screen.username_input.text()
        password = self.login_screen.password_input.text()
        
        if username and password:  # Simple validation
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.handle_login()
        else:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
    
    def start_problem(self):
        selected_index = self.problem_screen.problem_list.currentRow()
        if selected_index >= 0:
            problem = self.problem_screen.problems[selected_index]
            self.coding_screen.set_problem(problem)
            self.stack.setCurrentWidget(self.coding_screen)
    
    def run_code(self):
        code = self.coding_screen.editor.toPlainText()
        try:
            # Create a temporary file and run it
            with open("temp_code.py", "w") as f:
                f.write(code)
            
            result = subprocess.run(
                ["python", "temp_code.py"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = result.stdout if result.returncode == 0 else result.stderr
            self.coding_screen.output.setText(output)
            
        except subprocess.TimeoutExpired:
            self.coding_screen.output.setText("Error: Code execution timed out")
        except Exception as e:
            self.coding_screen.output.setText(f"Error: {str(e)}")
        finally:
            if os.path.exists("temp_code.py"):
                os.remove("temp_code.py")
    
    def submit_solution(self):
        code = self.coding_screen.editor.toPlainText()
        problem = self.coding_screen.current_problem
        
        try:
            # Create a test file with the user's code and test case
            with open("test_code.py", "w") as f:
                f.write(code + "\n\n" + problem["test_case"])
            
            # Run the test
            result = subprocess.run(
                ["python", "test_code.py"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                QMessageBox.information(self, "Success", "All tests passed! Great job!")
                if self.current_user:
                    self.current_user.solve_problem(problem["id"])
                    self.update_progress()
                self.stack.setCurrentWidget(self.problem_screen)
            else:
                self.coding_screen.output.setText(f"Tests failed:\n{result.stderr}")
            
        except Exception as e:
            self.coding_screen.output.setText(f"Error: {str(e)}")
        finally:
            if os.path.exists("test_code.py"):
                os.remove("test_code.py")
    
    def update_progress(self):
        if self.current_user:
            self.problem_screen.problems_solved.setText(
                f"Problems Solved: {len(self.current_user.solved_problems)}"
            )
            self.problem_screen.current_streak.setText(
                f"Current Streak: {self.current_user.current_streak}"
            )

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
