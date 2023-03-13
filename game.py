import tkinter as tk
import json
import time

class QuizGame:
    def __init__(self):
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0
        self.start_time = None
        self.time_remaining = None
        self.window = tk.Tk()
        self.window.title("US History Quiz Game")
        self.window.geometry("500x400")

        # Create widgets for displaying the question and answer options
        self.question_label = tk.Label(self.window, text="")
        self.question_label.pack()

        self.answer_var = tk.StringVar()
        self.answer_var.set("")
        self.option_a = tk.Radiobutton(self.window, text="", variable=self.answer_var, value="A")
        self.option_b = tk.Radiobutton(self.window, text="", variable=self.answer_var, value="B")
        self.option_c = tk.Radiobutton(self.window, text="", variable=self.answer_var, value="C")
        self.option_a.pack()
        self.option_b.pack()
        self.option_c.pack()

        # Create a widget for displaying the timer
        self.timer_label = tk.Label(self.window, text="")
        self.timer_label.pack()

        # Create a button for submitting the answer
        self.submit_button = tk.Button(self.window, text="Submit Answer", command=self.submit_answer)
        self.submit_button.pack()

        # Create a label for displaying the score
        self.score_label = tk.Label(self.window, text=f"Score: {self.score}")
        self.score_label.pack()

        # Create a dictionary to keep track of the player's answers to each question
        self.answered_questions = {}

        # Start the game
        self.display_question()


    # Load the questions from a file
    def load_questions(self):
        with open("questions.json") as f:
            data = json.load(f)
        return data


    # Display the current question and answer options
    
    def display_question(self):
        question_data = self.questions[self.current_question]
        self.question_label.configure(text=f"{self.current_question+1}. {question_data['question']}")
        self.option_a.configure(text=f"A. {question_data['options'][0]}", value=question_data['options'][0])
        self.option_b.configure(text=f"B. {question_data['options'][1]}", value=question_data['options'][1])
        self.option_c.configure(text=f"C. {question_data['options'][2]}", value=question_data['options'][2])

        self.answer_var.set("")
        self.option_a.configure(state=tk.NORMAL)
        self.option_b.configure(state=tk.NORMAL)
        self.option_c.configure(state=tk.NORMAL)
        
        self.start_time = time.time()
        self.time_remaining = 60
        self.update_timer()

        if self.current_question >= len(self.questions):
            self.end_game()


    # Update the timer every second
    def update_timer(self):
        # Calculate the time remaining
        elapsed_time = int(time.time() - self.start_time)
        self.time_remaining = max(0, 60 - elapsed_time)

        # Update the timer label
        self.timer_label.configure(text=f"Time remaining: {self.time_remaining} seconds")

        # If time is up, disable the answer buttons and move on to the next question
        if self.time_remaining == 0:
            self.option_a.configure(state=tk.DISABLED)
            self.option_b.configure(state=tk.DISABLED)
            self.option_c.configure(state=tk.DISABLED)
            self.submit_answer()

        # Update the timer label every second
        self.window.after(1000, self.update_timer)


    # Submit the player's answer and move on to the next question
    def submit_answer(self):
        # Disable the answer buttons to prevent multiple submissions
        self.option_a.configure(state=tk.DISABLED)
        self.option_b.configure(state=tk.DISABLED)
        self.option_c.configure(state=tk.DISABLED)

        # Calculate the player's score for the question and update the total score
        question_data = self.questions[self.current_question]
        if self.answer_var.get() == question_data['answer']:
            self.score += 1
            self.answered_questions[self.current_question] = True
        else:
            self.answered_questions[self.current_question] = False

        # Update the score label
        self.score_label.configure(text=f"Score: {self.score}")

        # Move on to the next question or end the game if all questions have been answered
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.end_game()
        print(self.answer_var.get())
        print(question_data['answer'])
        print(question_data)
        print(self.answer_var.get())




    def restart_game(self):
        self.current_question = 0
        self.score = 0
        self.answered_questions = {}

        # Update the score label
        self.score_label.configure(text=f"Score: {self.score}")

        # Reset the answer option buttons
        self.option_a.configure(state=tk.NORMAL)
        self.option_a.deselect()
        self.option_b.configure(state=tk.NORMAL)
        self.option_b.deselect()
        self.option_c.configure(state=tk.NORMAL)
        self.option_c.deselect()

        # Reset the timer
        self.start_time = None
        self.time_remaining = None

        # Display the first question
        self.display_question()

        # Create a button for restarting the game
        self.restart_button = tk.Button(self.window, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()


    # Reset the game and start again from the beginning
    def restart_game(self):
        self.current_question = 0
        self.score = 0
        self.answered_questions = {}

        # Update the score label
        self.score_label.configure(text=f"Score: {self.score}")

        # Reset the answer option buttons
        self.option_a.configure(state=tk.NORMAL)
        self.option_a.deselect()
        self.option_b.configure(state=tk.NORMAL)
        self.option_b.deselect()
        self.option_c.configure(state=tk.NORMAL)
        self.option_c.deselect()

        # Reset the timer
        self.start_time = None
        self.time_remaining = None

        # Remove the old restart button if it exists
        if hasattr(self, 'restart_button'):
            self.restart_button.pack_forget()

        # Display the first question
        self.display_question()

        # Create a button for restarting the game
        self.restart_button = tk.Button(self.window, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()
    def end_game(self):
    # Disable the answer buttons
        self.option_a.configure(state=tk.DISABLED)
        self.option_b.configure(state=tk.DISABLED)
        self.option_c.configure(state=tk.DISABLED)

        # Display the final score
        self.question_label.configure(text=f"Final Score: {self.score}/{len(self.questions)}")

        # Remove the old restart button if it exists
        if hasattr(self, 'restart_button'):
            self.restart_button.pack_forget()

        # Create a button for restarting the game
        self.restart_button = tk.Button(self.window, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()


game = QuizGame()
game.window.after(0, game.display_question)
game.window.mainloop()