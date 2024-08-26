import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Timer:
    def __init__(self, label, checkbox_var):
        self.label = label
        self.checkbox_var = checkbox_var  # Track the checkbox state
        self.running = False
        self.time_elapsed = 0

    def start(self):
        if not self.running:
            self.running = True
            self.update()

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.time_elapsed = 0
        self.update_display()

    def reset(self):
        self.stop()  # Stop the timer and reset the time_elapsed to 0

    def update(self):
        if self.running:
            self.time_elapsed += 1
            self.update_display()
            self.label.after(1000, self.update)

    def update_display(self):
        mins, secs = divmod(self.time_elapsed, 60)
        hours, mins = divmod(mins, 60)
        self.label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timers")
        self.geometry("600x350")
        self.timers = []

        # Specify Grid
        """
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)
        """

        numberOfTimers = 7

        for i in range(numberOfTimers):
            col = 0
            tableText = "Table " + str(i+1);
            tableLabel = ttk.Label(self, text=tableText, font=("Helvetica", 16))
            tableLabel.grid(row=i, column=col,sticky="NSEW", padx=0, pady=0)

            col = col + 1
            checkbox_var = tk.BooleanVar()  # Variable to track the checkbox state
            checkbox = tk.Checkbutton(self, variable=checkbox_var)
            checkbox.grid(row=i, column=col,sticky="NSEW", padx=5)

            col = col + 1
            label = ttk.Label(self, text="00:00:00", font=("Helvetica", 16))
            label.grid(row=i, column=col,sticky="NSEW", pady=0, padx=5)

            col = col + 1
            start_button = ttk.Button(self, text="Start", command=lambda i=i: self.start_timer(i))
            start_button.grid(row=i, column=col,sticky="NSEW", padx=5)

            col = col + 1
            pause_button = ttk.Button(self, text="Pause", command=lambda i=i: self.pause_timer(i))
            pause_button.grid(row=i, column=col,sticky="NSEW", padx=5)

            col = col + 1
            stop_button = ttk.Button(self, text="Stop", command=lambda i=i: self.stop_timer(i))
            stop_button.grid(row=i, column=col,sticky="NSEW", padx=5)

            col = col + 1
            reset_button = ttk.Button(self, text="Reset", command=lambda i=i: self.reset_timer(i))
            reset_button.grid(row=i, column=col,sticky="NSEW", padx=5)

            self.timers.append(Timer(label, checkbox_var))

        # General buutons (applicable to all timers)
        genCol = 1
        genRow = numberOfTimers + 1
        pad = 10
        start_all = ttk.Button(self, text="Start All", command=self.start_all)
        start_all.grid(row=genRow, column=genCol, pady=pad)

        genCol = genCol + 1
        pause_all = ttk.Button(self, text="Pause All", command=self.pause_all)
        pause_all.grid(row=genRow, column=genCol, pady=pad)

        genCol = genCol + 1
        stop_all = ttk.Button(self, text="Stop All", command=self.stop_all)
        stop_all.grid(row=genRow, column=genCol, pady=pad)

        genCol = genCol + 1
        reset_all = ttk.Button(self, text="Reset All", command=self.reset_selected)
        reset_all.grid(row=genRow, column=genCol, pady=pad)

        genCol = genCol + 1
        reset_all = ttk.Button(self, text="Reset Selected", command=self.reset_selected)
        reset_all.grid(row=genRow, column=genCol, pady=pad)

    def start_timer(self, i):
        self.timers[i].start()

    def pause_timer(self, i):
        self.timers[i].pause()

    def stop_timer(self, i):
        self.timers[i].stop()

    def reset_timer(self, i):
        self.timers[i].reset()

    def reset_selected(self):
        for timer in self.timers:
            if timer.checkbox_var.get():  # Check if the timer is selected
                timer.reset()

    def start_all(self):
        for timer in self.timers:
            timer.start()

    def pause_all(self):
        for timer in self.timers:
            timer.pause()

    def stop_all(self):
        for timer in self.timers:
            timer.stop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
