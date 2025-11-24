import tkinter as tk
from tkinter import simpledialog, messagebox
import random, string

# ---------------- Word + Hint Collection ----------------
WORD_HINTS = {
    # Programming / Tech
    "PYTHON": "It's an animal  but also a programming language.",
    "COMPUTER": "An electronic device you are using right now .",
    "PROGRAM": "Set of instructions for computer to follow .",
    "HANGMAN": "Classic word guessing game .",
    "PUZZLE": "Something tricky you solve for fun .",
    "KEYBOARD": "Used to type letters on computer ️.",
    "MOUSE": "Used with computer to point and click ️.",

    # Countries
    "INDIA": "Country known for the Taj Mahal .",
    "NEPAL": "Country with Mount Everest.",
    "JAPAN": "Country of sushi  and anime .",
    "FRANCE": "Country of Eiffel Tower .",
    "BRAZIL": "Country famous for football  and carnival .",
    "CANADA": "Country known for maple leaf .",
    "EGYPT": "Country of pyramids and the Nile River ️.",
    "AUSTRALIA": "Country of kangaroos .",
    "CHINA": "Country of the Great Wall .",
    "RUSSIA": "Largest country in the world .",

    # Capitals
    "DELHI": "Capital city of India.",
    "KATHMANDU": "Capital city of Nepal.",
    "TOKYO": "Capital city of Japan.",
    "PARIS": "Capital city of France.",
    "OTTAWA": "Capital city of Canada.",
    "CAIRO": "Capital city of Egypt.",
    "MOSCOW": "Capital city of Russia.",

    # Fruits
    "APPLE": "A fruit that keeps the doctor away .",
    "MANGO": "King of fruits .",
    "BANANA": "Monkeys love it .",
    "ORANGE": "Citrus fruit rich in Vitamin C .",
    "GRAPES": "Small fruits that grow in bunches.",
    "PINEAPPLE": "Tropical fruit with a spiky shell .",
    "WATERMELON": "Large fruit with juicy red inside .",

    # Sports
    "CRICKET": "Most popular sport in India .",
    "FOOTBALL": "Called soccer in the USA .",
    "TENNIS": "Played with a racket .",
    "HOCKEY": "Played on grass or ice with a stick.",
    "CHESS": "Board game of kings and queens.",

    # Brands & Misc
    "RADHEZONE": "Your own shopping brand.",
    "NIKE": "Sports brand with the famous swoosh.",
    "ADIDAS": "Brand with three stripes.",
    "PUMA": "Sports brand named after a wild cat .",
    "SAMSUNG": "Electronics brand (phones, TVs) .",
    "APPLEINC": "Company that makes iPhones .",

    # General
    "FRIENDS": "People who make life beautiful .",
    "MUSIC": "We listen to it for relaxation .",
    "GARDEN": "A place where flowers and plants grow .",
    "RAINBOW": "Colorful arc after rain .",
    "RIVER": "Flows from mountains to the sea .",
    "MOON": "Shines at night .",
    "SUN": "Our daytime star ."
}
# -------------------------------------------------------

class PuzzleGame:
    def __init__(self, master):
        self.master = master
        master.title("Word Puzzle — Best of 10")
        master.attributes("-fullscreen", True)
        master.bind("<Escape>", lambda e: master.attributes("-fullscreen", False))

        # Tournament config
        self.max_rounds = 10
        self.round_number = 0

        # Player selection (2-4)
        self.num_players = simpledialog.askinteger(
            "Players", "Enter number of players (2-4):", parent=master, minvalue=2, maxvalue=4
        )
        if not self.num_players:
            self.num_players = 2

        # Game state
        self.word = ""
        self.hint = ""
        self.guessed = []
        self.scores = [0] * self.num_players
        self.current_player = 0
        self.guessed_letters = set()
        self.player_names = [f"Player {i+1}" for i in range(self.num_players)]
        self.ask_player_names()

        # Word pool management to avoid repeats until exhausted
        self.word_pool = list(WORD_HINTS.keys())
        random.shuffle(self.word_pool)

        # === UI ===
        self.top_info = tk.Frame(master, pady=10)
        self.top_info.pack()
        self.round_label = tk.Label(self.top_info, text=f"Round: {self.round_number}/{self.max_rounds}",
                                    font=("Helvetica", 20))
        self.round_label.pack()

        self.word_label = tk.Label(master, text="", font=("Helvetica", 64, "bold"), pady=20)
        self.word_label.pack()

        self.hint_label = tk.Label(master, text="", font=("Helvetica", 22, "italic"), fg="darkgreen", pady=8)
        self.hint_label.pack()

        self.guessed_label = tk.Label(master, text="Guessed: ", font=("Helvetica", 18))
        self.guessed_label.pack()

        self.players_frame = tk.Frame(master, pady=20)
        self.players_frame.pack()
        self.player_labels = []
        for i in range(self.num_players):
            lbl = tk.Label(self.players_frame,
                           text=self._player_text(i),
                           font=("Helvetica", 18),
                           bd=4, relief="groove", padx=18, pady=12, width=22)
            lbl.grid(row=0, column=i, padx=12, pady=6)
            self.player_labels.append(lbl)

        input_frame = tk.Frame(master, pady=14)
        input_frame.pack()
        tk.Label(input_frame, text="Enter a letter:", font=("Helvetica", 18)).pack(side="left", padx=6)
        self.letter_entry = tk.Entry(input_frame, width=3, font=("Helvetica", 30))
        self.letter_entry.pack(side="left", padx=10)
        self.letter_entry.bind("<Return>", lambda e: self.make_guess())

        guess_button = tk.Button(input_frame, text="Guess", command=self.make_guess,
                                 font=("Helvetica", 16), bg="lightblue", padx=10)
        guess_button.pack(side="left", padx=8)

        hint_button = tk.Button(input_frame, text="Show Hint (-1 point)", command=self.show_hint,
                                font=("Helvetica", 16), bg="orange", padx=10)
        hint_button.pack(side="left", padx=8)

        self.message_label = tk.Label(master, text="", font=("Helvetica", 18), fg="blue", pady=12)
        self.message_label.pack()

        control_frame = tk.Frame(master, pady=8)
        control_frame.pack()
        tk.Button(control_frame, text="New Random Word", command=self.force_new_round,
                  font=("Helvetica", 14), bg="lightgreen").pack(side="left", padx=8)
        tk.Button(control_frame, text="Set Custom Word", command=self.set_custom_word,
                  font=("Helvetica", 14), bg="lightyellow").pack(side="left", padx=8)
        tk.Button(control_frame, text="Restart Tournament", command=self.restart_tournament,
                  font=("Helvetica", 14), bg="lightcoral").pack(side="left", padx=8)
        tk.Button(control_frame, text="Quit", command=master.quit,
                  font=("Helvetica", 14), bg="lightgray").pack(side="left", padx=8)

        # Start first round
        self.new_round()

    def ask_player_names(self):
        for i in range(self.num_players):
            name = simpledialog.askstring("Player Name", f"Enter name for Player {i+1}:", parent=self.master)
            if name and name.strip():
                self.player_names[i] = name.strip()

    def _player_text(self, i):
        label = f"{self.player_names[i]}: {self.scores[i]}"
        return f"> {label} <" if i == self.current_player else label

    def update_ui(self):
        self.round_label.config(text=f"Round: {self.round_number}/{self.max_rounds}")
        self.word_label.config(text=" ".join(self.guessed))
        guessed_txt = ", ".join(sorted(self.guessed_letters)) if self.guessed_letters else "(none)"
        self.guessed_label.config(text="Guessed: " + guessed_txt)
        self.hint_label.config(text=f"💡 Hint: {self.hint}")
        for i, lbl in enumerate(self.player_labels):
            lbl.config(text=self._player_text(i))
        self.message_label.config(text=f"{self.player_names[self.current_player]}'s turn")
        self.letter_entry.focus_set()

    def draw_word_from_pool(self):
        if not self.word_pool:
            # refill pool if exhausted
            self.word_pool = list(WORD_HINTS.keys())
            random.shuffle(self.word_pool)
        return self.word_pool.pop()

    def new_round(self):
        # increment round counter and start next round
        self.round_number += 1
        if self.round_number > self.max_rounds:
            self.show_final_scoreboard()
            return

        word_key = self.draw_word_from_pool()
        hint = WORD_HINTS.get(word_key, "No hint available.")
        self._start_game(word_key, hint)
        self.update_ui()

    def force_new_round(self):
        """Manual new word (useful for testing) — does not change round count."""
        word_key = self.draw_word_from_pool()
        hint = WORD_HINTS.get(word_key, "No hint available.")
        self._start_game(word_key, hint)
        self.update_ui()

    def set_custom_word(self):
        dlg = simpledialog.askstring("Custom word", "Enter a word (letters only):", parent=self.master)
        if dlg:
            word = "".join(ch for ch in dlg.strip().upper() if ch.isalpha())
            if len(word) < 1:
                messagebox.showerror("Invalid", "Please enter at least one letter.")
                return
            hint = simpledialog.askstring("Custom Hint", f"Enter a hint for '{word}':", parent=self.master)
            if not hint:
                hint = "No hint provided."
            # Custom word does not alter word_pool; set as current round's word
            self._start_game(word, hint)
            self.update_ui()

    def restart_tournament(self):
        if not messagebox.askyesno("Restart", "Restart the Best-of-10 tournament? Scores will be reset."):
            return
        self.scores = [0] * self.num_players
        self.current_player = 0
        self.guessed_letters = set()
        self.round_number = 0
        self.word_pool = list(WORD_HINTS.keys())
        random.shuffle(self.word_pool)
        self.new_round()

    def _start_game(self, word, hint):
        self.word = word
        self.hint = hint
        self.guessed = ["_" for _ in word]
        self.guessed_letters = set()
        # Do NOT reveal any letters automatically (per request)
        self.update_ui()

    def make_guess(self):
        raw = self.letter_entry.get().strip().upper()
        self.letter_entry.delete(0, tk.END)
        if not raw or len(raw) != 1 or raw not in string.ascii_uppercase:
            self.message_label.config(text="Enter a single English letter (A–Z).")
            return

        letter = raw
        if letter in self.guessed_letters:
            self.message_label.config(text=f"'{letter}' already guessed. Try another.")
            return

        self.guessed_letters.add(letter)
        correct = False
        occurrences = 0
        for idx, ch in enumerate(self.word):
            if ch == letter and self.guessed[idx] == "_":
                self.guessed[idx] = letter
                correct = True
                occurrences += 1

        if correct:
            self.scores[self.current_player] += occurrences
            self.message_label.config(
                text=f"✅ {self.player_names[self.current_player]} found {occurrences} '{letter}'!"
            )
            self.animate_label(self.player_labels[self.current_player], "lightgreen")
            if "_" not in self.guessed:
                # round finished — proceed to next round (after small pause)
                self.master.after(500, self.finish_round_and_continue)
                return
        else:
            self.message_label.config(
                text=f"❌ {self.player_names[self.current_player]} missed! Next player's turn."
            )
            self.animate_label(self.player_labels[self.current_player], "tomato")
            self.current_player = (self.current_player + 1) % self.num_players

        self.update_ui()

    def show_hint(self):
        # reveal one random hidden letter, apply -1 penalty to current player
        hidden_indices = [i for i, l in enumerate(self.guessed) if l == "_"]
        if not hidden_indices:
            self.message_label.config(text="No more hints available.")
            return

        idx = random.choice(hidden_indices)
        letter = self.word[idx]
        self.guessed[idx] = letter
        self.guessed_letters.add(letter)
        self.scores[self.current_player] -= 1
        self.message_label.config(text=f"💡 Hint used! Letter '{letter}' revealed. -1 point.")
        self.animate_label(self.player_labels[self.current_player], "yellow")
        if "_" not in self.guessed:
            self.master.after(500, self.finish_round_and_continue)
            return
        self.update_ui()

    def finish_round_and_continue(self):
        """Called when a round ends naturally — shows short info and then starts next round."""
        # Notify which player found the last letter (optional)
        self.update_ui()
        # proceed to next round: current_player moves to next to start the next round
        self.current_player = (self.current_player + 1) % self.num_players
        self.new_round()

    def show_final_scoreboard(self):
        # Build sorted scoreboard
        players = [(self.player_names[i], self.scores[i]) for i in range(self.num_players)]
        players_sorted = sorted(players, key=lambda x: x[1], reverse=True)

        # Create modal window
        top = tk.Toplevel(self.master)
        top.title("Final Scoreboard — Best of 10")
        top.geometry("700x500")
        # Center-ish
        x = (top.winfo_screenwidth() // 2) - 350
        y = (top.winfo_screenheight() // 2) - 250
        top.geometry(f"+{x}+{y}")

        tk.Label(top, text="🏆 Final Scoreboard (Best of 10) 🏆", font=("Helvetica", 20, "bold"), pady=12).pack()

        # Display ranking
        frame = tk.Frame(top, pady=8)
        frame.pack()
        for rank, (name, score) in enumerate(players_sorted, start=1):
            tk.Label(frame, text=f"{rank}. {name} — {score} points", font=("Helvetica", 18)).pack(anchor="w", padx=20, pady=4)

        # Summary text
        winner_names = [p for p, s in players_sorted if s == players_sorted[0][1]]
        if len(winner_names) == 1:
            summary = f"Winner: {winner_names[0]}"
        else:
            summary = "It's a tie between: " + ", ".join(winner_names)
        tk.Label(top, text=summary, font=("Helvetica", 16, "italic"), fg="darkgreen", pady=8).pack()

        btn_frame = tk.Frame(top, pady=12)
        btn_frame.pack()
        tk.Button(btn_frame, text="Restart Tournament", font=("Helvetica", 14),
                  command=lambda: (top.destroy(), self.restart_tournament())).pack(side="left", padx=12)
        tk.Button(btn_frame, text="Quit", font=("Helvetica", 14),
                  command=self.master.quit).pack(side="left", padx=12)

        # make modal
        top.transient(self.master)
        top.grab_set()
        self.master.wait_window(top)

    def animate_label(self, label, color, steps=8, delay=120):
        default_bg = label.cget("bg")
        def step(c=0):
            if c < steps:
                label.config(bg=color if c % 2 == 0 else default_bg)
                self.master.after(delay, step, c+1)
            else:
                label.config(bg=default_bg)
        step()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGame(root)
    root.mainloop()
