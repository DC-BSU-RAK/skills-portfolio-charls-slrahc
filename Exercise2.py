import tkinter as tk
from tkinter import messagebox
import random

class JokeTellingAssistant:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa - Joke Teller")
        self.root.geometry("1000x700")  # Increased window size for better visibility
        self.root.resizable(False, False)  # Prevent resizing to maintain layout
        
        # Load jokes from file into a list
        self.jokes = self.load_jokes()
        self.current_joke = None  # Will hold the currently selected joke string
        self.current_setup = ""   # Setup part of the current joke
        self.current_punchline = ""  # Punchline part of the current joke
        
        # Define color scheme for the GUI (Alexa-inspired)
        self.bg_color = "#232f3e"  # Dark blue background
        self.button_color = "#ff9900"  # Orange for primary buttons
        self.text_color = "white"  # White text for contrast
        self.setup_color = "#00a8e1"  # Light blue for joke setup
        self.punchline_color = "#ff9900"  # Orange for punchline
        
        self.root.configure(bg=self.bg_color)  # Apply background color to root
        
        # Create and place all GUI widgets
        self.create_widgets()
        
    def load_jokes(self):
        with open('randomJokes.txt', 'r', encoding='utf-8') as file:
            jokes = [line.strip() for line in file if line.strip()]  # Strip and filter non-empty lines
        return jokes
    
    def create_widgets(self):
        # Main title label - Centered and prominent
        self.title_label = tk.Label(
            self.root, 
            text="Alexa Joke Teller", 
            font=("Arial", 32, "bold"),  # Large bold font for title
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.title_label.pack(pady=40)  # Add vertical padding
        
        # Subtitle label - Smaller than title, descriptive
        self.subtitle_label = tk.Label(
            self.root,
            text="Your personal joke-telling assistant",
            font=("Arial", 18),  # Medium font for subtitle
            bg=self.bg_color,
            fg=self.text_color
        )
        self.subtitle_label.pack(pady=10)
        
        # Frame to hold the joke display labels, centered with padding
        self.joke_frame = tk.Frame(self.root, bg=self.bg_color)
        self.joke_frame.pack(pady=50, padx=50, fill='both', expand=True)
        
        # Label for displaying the joke setup (question part)
        self.setup_label = tk.Label(
            self.joke_frame,
            text="Click 'Tell me a Joke' to hear a joke!",
            font=("Arial", 20, "bold"),  # Bold font for setup
            bg=self.bg_color,
            fg=self.setup_color,
            wraplength=700,  # Wrap text at 700 pixels for readability
            justify='center'  # Center-align text
        )
        self.setup_label.pack(expand=True, pady=20)
        
        # Label for displaying the punchline (answer part)
        self.punchline_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Arial", 18, "italic"),  # Italic font for punchline
            bg=self.bg_color,
            fg=self.punchline_color,
            wraplength=700,  # Wrap text at 700 pixels
            justify='center'
        )
        self.punchline_label.pack(expand=True, pady=20)
        
        # Frame to hold the buttons, centered
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=40)
        
        # Common style dictionary for buttons (consistent sizing and appearance)
        button_style = {
            'font': ("Arial", 16, "bold"),  # Bold font for buttons
            'width': 20,  # Fixed width for uniformity
            'height': 2,  # Fixed height
            'bd': 3,      # Border thickness
            'relief': 'raised'  # Raised appearance
        }
        
        # Button to tell a new joke (starts the process)
        self.tell_joke_btn = tk.Button(
            self.button_frame,
            text="🎤 Alexa tell me a Joke",
            command=self.tell_joke,  # Calls tell_joke method
            bg=self.button_color,
            fg="white",
            **button_style
        )
        self.tell_joke_btn.grid(row=0, column=0, padx=15, pady=15)  # Position in grid
        
        # Button to reveal the punchline (initially disabled)
        self.punchline_btn = tk.Button(
            self.button_frame,
            text="😂 Show Punchline",
            command=self.show_punchline,  # Calls show_punchline method
            bg="#32a852",  # Green color
            fg="white",
            state='disabled',  # Disabled until a joke is told
            **button_style
        )
        self.punchline_btn.grid(row=0, column=1, padx=15, pady=15)
        
        # Button to get the next joke (initially disabled)
        self.next_joke_btn = tk.Button(
            self.button_frame,
            text="➡️ Next Joke",
            command=self.next_joke,  # Calls next_joke method
            bg="#007bff",  # Blue color
            fg="white",
            state='disabled',  # Disabled until a joke is told
            **button_style
        )
        self.next_joke_btn.grid(row=1, column=0, padx=15, pady=15)
        
        # Button to quit the application
        self.quit_btn = tk.Button(
            self.button_frame,
            text="🚪 Quit",
            command=self.quit_app,  # Calls quit_app method
            bg="#dc3545",  # Red color
            fg="white",
            **button_style
        )
        self.quit_btn.grid(row=1, column=1, padx=15, pady=15)
        
        # Status label at the bottom to show app state or messages
        self.status_label = tk.Label(
            self.root,
            text=f"📚 Loaded {len(self.jokes)} jokes - Ready to make you laugh!",
            font=("Arial", 14),  # Medium font for status
            bg=self.bg_color,
            fg=self.text_color
        )
        self.status_label.pack(pady=20)
        
        # Configure grid weights for centering (though not strictly necessary here)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        
        # Center the button frame content (rows)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)
    
    def tell_joke(self):
        if not self.jokes:
            messagebox.showerror("Error", "No jokes available!")  # Error if no jokes loaded
            return
        
        # Select a random joke from the list
        self.current_joke = random.choice(self.jokes)
        
        # Split the joke into setup and punchline based on the first '?'
        if '?' in self.current_joke:
            parts = self.current_joke.split('?', 1)  # Split only on first '?'
            self.current_setup = parts[0] + "?"  # Include the '?' in setup
            self.current_punchline = parts[1] if len(parts) > 1 else ""  # Punchline after '?'
        else:
            # Fallback if no '?' found (treat whole as setup)
            self.current_setup = self.current_joke
            self.current_punchline = "(Punchline not available)"
        
        # Update the setup label with the setup text
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")  # Clear punchline label
        
        # Enable punchline and next joke buttons, disable tell joke button
        self.punchline_btn.config(state='normal')
        self.next_joke_btn.config(state='normal')
        self.tell_joke_btn.config(state='disabled')
        
        # Update status to prompt user for next action
        self.status_label.config(text="🎭 Joke ready! Click 'Show Punchline' for the funny part!")
    
    def show_punchline(self):
        if self.current_punchline:
            self.punchline_label.config(text=self.current_punchline)  # Show punchline
            self.punchline_btn.config(state='disabled')  # Disable button after use
            self.status_label.config(text="😄 Hope that made you smile! Try another joke?")
        else:
            messagebox.showinfo("Info", "No punchline available for this joke.")  # Info if no punchline
    
    def next_joke(self):
        # Reset labels to indicate loading/next action
        self.setup_label.config(text="🔄 Getting another joke...")
        self.punchline_label.config(text="")
        
        # Reset button states: enable tell joke, disable others
        self.tell_joke_btn.config(state='normal')
        self.punchline_btn.config(state='disabled')
        self.next_joke_btn.config(state='disabled')
        
        # Update status
        self.status_label.config(text="🔄 Ready for another joke!")
        
        # After 500ms delay, update setup label to prompt for new joke
        self.root.after(500, lambda: self.setup_label.config(text="🎤 Click 'Alexa tell me a Joke' for another joke!"))
    
    def quit_app(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):  # Confirm quit
            self.root.quit()  # Close the Tkinter main loop

def main():
    root = tk.Tk()  # Create root window
    app = JokeTellingAssistant(root)  # Instantiate the app
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()  
