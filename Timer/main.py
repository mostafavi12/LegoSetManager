import tkinter as tk
from tkinter import ttk

class Timer:
    def __init__(self, label, checkbox_var, update_callback):
        self.label = label
        self.checkbox_var = checkbox_var
        self.running = False
        self.time_elapsed = 0
        self.update_callback = update_callback

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
        self.update_callback()

    def reset(self):
        self.stop()

    def update(self):
        if self.running:
            self.time_elapsed += 1
            self.update_display()
            self.update_callback()
            self.label.after(1000, self.update)

    def update_display(self):
        mins, secs = divmod(self.time_elapsed, 60)
        hours, mins = divmod(mins, 60)
        self.label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timers")
        self.geometry("1000x350")
        self.timers = []

        numberOfTimers = 7

        for i in range(numberOfTimers):
            col = 0
            tableText = "Table " + str(i+1)
            tableLabel = ttk.Label(self, text=tableText, font=("Helvetica", 16))
            tableLabel.grid(row=i, column=col, sticky="NSEW", padx=0, pady=0)

            col += 1
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self, variable=checkbox_var)
            checkbox.grid(row=i, column=col, sticky="NSEW", padx=5)

            col += 1
            label = ttk.Label(self, text="00:00:00", font=("Helvetica", 16))
            label.grid(row=i, column=col, sticky="NSEW", pady=0, padx=5)

            col += 1
            base_price_var = tk.IntVar(value=120)
            base_price_entry = ttk.Entry(self, textvariable=base_price_var, width=10)
            base_price_entry.grid(row=i, column=col, padx=5)

            col += 1
            total_price_var = tk.StringVar(value="0.00")
            total_price_entry = ttk.Entry(self, textvariable=total_price_var, width=10, state='readonly')
            total_price_entry.grid(row=i, column=col, padx=5)

            col += 1
            start_button = ttk.Button(self, text="Start", command=lambda i=i: self.start_timer(i))
            start_button.grid(row=i, column=col, sticky="NSEW", padx=5)

            col += 1
            pause_button = ttk.Button(self, text="Pause", command=lambda i=i: self.pause_timer(i))
            pause_button.grid(row=i, column=col, sticky="NSEW", padx=5)

            col += 1
            stop_button = ttk.Button(self, text="Stop", command=lambda i=i: self.stop_timer(i))
            stop_button.grid(row=i, column=col, sticky="NSEW", padx=5)

            timer_obj = Timer(label, checkbox_var, lambda i=i: self.calculate_price(i))

            self.timers.append({
                'timer': timer_obj,
                'base_price_var': base_price_var,
                'total_price_var': total_price_var
            })

        genCol = 1
        genRow = numberOfTimers + 1
        pad = 10
        start_all = ttk.Button(self, text="Start All", command=self.start_all)
        start_all.grid(row=genRow, column=genCol, pady=pad)

        genCol += 1
        pause_all = ttk.Button(self, text="Pause All", command=self.pause_all)
        pause_all.grid(row=genRow, column=genCol, pady=pad)

        genCol += 1
        stop_all = ttk.Button(self, text="Stop All", command=self.stop_all)
        stop_all.grid(row=genRow, column=genCol, pady=pad)

        genCol += 1
        reset_all = ttk.Button(self, text="Reset Selected", command=self.reset_selected)
        reset_all.grid(row=genRow, column=genCol, pady=pad)

    def start_timer(self, i):
        self.timers[i]['timer'].start()

    def pause_timer(self, i):
        self.timers[i]['timer'].pause()

    def stop_timer(self, i):
        self.timers[i]['timer'].stop()

    def reset_selected(self):
        for timer_data in self.timers:
            if timer_data['timer'].checkbox_var.get():
                timer_data['timer'].reset()

    def start_all(self):
        for timer_data in self.timers:
            timer_data['timer'].start()

    def pause_all(self):
        for timer_data in self.timers:
            timer_data['timer'].pause()

    def stop_all(self):
        for timer_data in self.timers:
            timer_data['timer'].stop()

    def calculate_price(self, i):
        timer_data = self.timers[i]
        seconds = timer_data['timer'].time_elapsed
        base_price = timer_data['base_price_var'].get()

        if seconds <= 3600:
            total_price = base_price
        else:
            extra_seconds = seconds - 3600
            ten_min_blocks = extra_seconds // 600
            total_price = base_price + (ten_min_blocks * (base_price / 6))

        timer_data['total_price_var'].set(f"{total_price:.2f}")


if __name__ == "__main__":
    app = App()
    app.mainloop()