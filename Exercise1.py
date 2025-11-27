import tkinter as tk
import random
from PIL import Image, ImageTk  # PIL is used for image handling (PhotoImage from PIL)
import os  # For file path operations

class ArithmeticQuiz:

    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.WIDTH, self.HEIGHT = 900, 600  # Define window dimensions
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)  # Prevent window resizing
        
        # Define color scheme for the application
        self.bg_color = "#f0f8ff"  # Light blue background
        self.paper_color = "#ffffff"  # White for the "paper" card
        self.button_color = "#4CAF50"  # Green for buttons
        self.accent_color = "#2196F3"  # Blue for accents
        
        # Quiz state variables
        self.difficulty = None  # Current difficulty level (easy, moderate, advanced)
        self.score = 0  # User's current score
        self.current_question = 0  # Current question number
        self.total_questions = 10  # Total number of questions in the quiz
        
        self.setup_gui()  # Set up the GUI components
        self.show_welcome()  # Display the welcome screen initially

    def setup_gui(self):
        self.root.configure(bg=self.bg_color)  # Set background color of root
        self.create_paper_card()  # Create the central paper-like frame
        self.create_frames()  # Create all necessary frames for different screens
        self.create_widgets()  # Create and place all widgets within frames

    def create_paper_card(self):
        # Shadow frame for depth effect
        self.paper_shadow = tk.Frame(self.root, bg='#b0bec5')  # Gray shadow color
        self.paper_shadow.place(relx=0.5, rely=0.5, anchor='center', width=608, height=458)
        
        # Main paper frame (white with ridge border)
        self.paper_frame = tk.Frame(self.root, bg=self.paper_color, bd=2, relief='ridge')
        self.paper_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=450)

    def create_frames(self):
        self.welcome_frame = tk.Frame(self.root, bg=self.bg_color)  # Welcome screen frame
        self.menu_frame = tk.Frame(self.paper_frame, bg=self.paper_color)  # Difficulty selection menu
        self.quiz_frame = tk.Frame(self.paper_frame, bg=self.paper_color)  # Quiz questions frame
        self.results_frame = tk.Frame(self.paper_frame, bg=self.paper_color)  # Results screen frame

    def create_widgets(self):
        # Welcome frame widgets
        try:
            # Attempt to load and display a welcome image
            base_dir = os.path.dirname(__file__)  # Get the directory of the script
            image_path = os.path.join(base_dir, 'Exercise1WelcomePage.png')  # Primary path
            if not os.path.exists(image_path):
                image_path = os.path.join(base_dir, '..', 'Exercise1WelcomePage.png')  # Fallback path
            if os.path.exists(image_path):
                img = Image.open(image_path)  # Open image with PIL
                img = img.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)  # Resize to fit window
                self.welcome_img = ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible image
                self.welcome_bg = tk.Label(self.welcome_frame, image=self.welcome_img)  # Background label with image
                self.welcome_bg.place(x=0, y=0, relwidth=1, relheight=1)  # Cover entire frame
        except Exception:
            # Fallback if image loading fails: display a text label
            tk.Label(self.welcome_frame, text='Welcome to Arithmetic Quiz!', 
                    font=('Arial', 28, 'bold'), bg=self.bg_color, fg=self.accent_color).pack(pady=40)
        
        # Start button on welcome screen
        self.start_btn = self.create_button(self.welcome_frame, 'START QUIZ', self.show_difficulty_menu,
                                          font=('Arial', 16, 'bold'), bg=self.accent_color)
        self.start_btn.place(relx=0.5, rely=0.70, anchor='center')  # Center the button

        # Menu frame widgets (difficulty selection)
        tk.Label(self.menu_frame, text="SELECT DIFFICULTY", font=("Arial", 20, "bold"), 
                bg=self.paper_color, fg=self.accent_color).pack(pady=30)  # Title label
        
        # Difficulty buttons
        self.easy_btn = self.create_button(self.menu_frame, "EASY", lambda: self.start_quiz("easy"),
                                         bg="#4CAF50", font=("Arial", 16, "bold"))
        self.moderate_btn = self.create_button(self.menu_frame, "MODERATE", lambda: self.start_quiz("moderate"),
                                             bg="#FF9800", font=("Arial", 16, "bold"))
        self.advanced_btn = self.create_button(self.menu_frame, "ADVANCED", lambda: self.start_quiz("advanced"),
                                             bg="#F44336", font=("Arial", 16, "bold"))
        
        # Pack buttons with padding
        self.easy_btn.pack(pady=15)
        self.moderate_btn.pack(pady=15)
        self.advanced_btn.pack(pady=15)

        # Quiz frame widgets
        header_frame = tk.Frame(self.quiz_frame, bg=self.paper_color)  # Header for score and question number
        header_frame.pack(pady=10)
        
        # Labels for score and question progress
        self.score_label = tk.Label(header_frame, text="Score: 0", font=("Arial", 16, "bold"), bg=self.paper_color)
        self.question_label = tk.Label(header_frame, text="Question: 1/10", font=("Arial", 16, "bold"), bg=self.paper_color)
        self.score_label.pack(side='left', padx=20)
        self.question_label.pack(side='right', padx=20)
        
        # Label to display the arithmetic problem
        self.problem_label = tk.Label(self.quiz_frame, text="", font=("Arial", 32, "bold"), bg=self.paper_color)
        self.problem_label.pack(expand=True, pady=30)
        
        # Entry field for user's answer
        self.answer_entry = tk.Entry(self.quiz_frame, font=("Arial", 20), width=8, justify='center')
        self.answer_entry.pack(pady=10)
        
        # Submit button to check the answer
        self.submit_btn = self.create_button(self.quiz_frame, "SUBMIT", self.check_answer)
        self.submit_btn.pack(pady=10)
        
        # Feedback label for correct/wrong messages
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Arial", 14), bg=self.paper_color)
        self.feedback_label.pack(pady=10)

        # Results frame widgets
        tk.Label(self.results_frame, text="QUIZ COMPLETED!", font=("Arial", 24, "bold"), 
                bg=self.paper_color, fg=self.accent_color).pack(pady=30)  # Completion title
        
        # Labels for final score and grade
        self.final_score_label = tk.Label(self.results_frame, text="", font=("Arial", 20), bg=self.paper_color)
        self.grade_label = tk.Label(self.results_frame, text="", font=("Arial", 22, "bold"), bg=self.paper_color)
        self.final_score_label.pack(pady=15)
        self.grade_label.pack(pady=15)
        
        # Frame for result buttons
        buttons_frame = tk.Frame(self.results_frame, bg=self.paper_color)
        buttons_frame.pack(pady=30)
        
        # Play again and quit buttons
        self.play_again_btn = self.create_button(buttons_frame, "PLAY AGAIN", self.restart_quiz)
        self.quit_btn = self.create_button(buttons_frame, "QUIT", self.root.quit, bg="#f44336")
        self.play_again_btn.pack(side='left', padx=10)
        self.quit_btn.pack(side='right', padx=10)

    def create_button(self, parent, text, command, **kwargs):
        btn = tk.Button(parent, text=text, command=command, 
                       font=kwargs.get('font', ("Arial", 14, "bold")),  # Default font
                       bg=kwargs.get('bg', self.button_color),  # Default background color
                       fg='white', width=12, height=1)  # White text, fixed size
        return btn

    def show_welcome(self):
        self.hide_all_frames()  # Hide all frames first
        self.welcome_frame.pack(expand=True, fill='both')  # Show welcome frame

    def show_difficulty_menu(self):
        self.hide_all_frames()
        self.menu_frame.pack(expand=True, fill='both')

    def start_quiz(self, difficulty):
        self.difficulty = difficulty  # Set difficulty
        self.score = 0  # Reset score
        self.current_question = 0  # Reset question counter
        self.hide_all_frames()
        self.quiz_frame.pack(expand=True, fill='both')  # Show quiz frame
        self.next_question()  # Load the first question

    def next_question(self):
        if self.current_question >= self.total_questions:
            self.show_results()  # Quiz finished, show results
            return
        
        self.current_question += 1  # Increment question number
        self.feedback_label.config(text="")  # Clear previous feedback
        self.answer_entry.delete(0, tk.END)  # Clear answer entry
        
        # Update score and question labels
        self.score_label.config(text=f"Score: {self.score}")
        self.question_label.config(text=f"Question: {self.current_question}/{self.total_questions}")
        
        # Generate random numbers based on difficulty
        self.num1 = self.generate_number()
        self.num2 = self.generate_number()
        operation = random.choice(['+', '-'])  # Randomly choose addition or subtraction
        
        # Ensure subtraction doesn't result in negative (swap if needed)
        if operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        # Calculate correct answer
        self.correct_answer = self.num1 + self.num2 if operation == '+' else self.num1 - self.num2
        self.problem_label.config(text=f"{self.num1} {operation} {self.num2} = ?")  # Display problem
        self.answer_entry.focus()  # Focus on entry field

    def generate_number(self):
        if self.difficulty == "easy":
            return random.randint(1, 9)  # Single digits
        elif self.difficulty == "moderate":
            return random.randint(10, 99)  # Two digits
        else:  # Advanced
            return random.randint(1000, 9999)  # Four digits

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())  # Parse user input as integer
            
            if user_answer == self.correct_answer:
                self.score += 10  # Award 10 points for correct answer
                self.feedback_label.config(text="Correct! +10 points", fg="green")  # Green feedback
                self.root.after(1000, self.next_question)  # Proceed after 1 second
            else:
                self.feedback_label.config(text=f"Wrong! Answer: {self.correct_answer}", fg="red")  # Red feedback
                self.root.after(1500, self.next_question)  # Proceed after 1.5 seconds
                
        except ValueError:
            # Handle non-numeric input
            self.feedback_label.config(text="Please enter a number", fg="orange")

    def show_results(self):
        self.hide_all_frames()
        self.results_frame.pack(expand=True, fill='both')
        
        percentage = (self.score / 100) * 100  # Calculate percentage (score out of 100)
        grade = self.calculate_grade(percentage)  # Determine grade based on percentage
        
        # Update result labels
        self.final_score_label.config(text=f"Final Score: {self.score}/100")
        self.grade_label.config(text=f"Grade: {grade}")

    def calculate_grade(self, percentage):
        if percentage >= 90: return "A+"
        elif percentage >= 80: return "A"
        elif percentage >= 70: return "B"
        elif percentage >= 60: return "C"
        elif percentage >= 50: return "D"
        else: return "F"

    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.menu_frame, self.quiz_frame, self.results_frame]:
            frame.pack_forget()

    def restart_quiz(self):
        self.show_difficulty_menu()

def main():
    root = tk.Tk()  # Create root window
    app = ArithmeticQuiz(root)  # Instantiate the quiz app
    root.mainloop()  # Start the event loop

if __name__ == "__main__":
    main() 
