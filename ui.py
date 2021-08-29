import tkinter
from random import choice
from tkinter import *
from tkinter import messagebox

from words import words


class UI:
    def __init__(self, data, time):
        self.font_name = 'Magneto'
        self.font_color = 'white'
        self.words = words(data)
        self.word = choice(self.words)
        self.time = time
        self.timer = None
        self.word_correct = 0
        self.character_correct = 0
        self.result = {}
        self.review = tkinter.Label
        # Root
        self.background_color = 'gray'
        self.root = Tk()
        self.root.title('Typing Speed Test👽')
        self.root.config(padx=15, pady=15, bg=self.background_color)
        # Canvas
        self.canvas = Canvas(self.root, width=400, height=100, bg=self.background_color, highlightthickness=0)
        self.cv_word = self.canvas.create_text(200, 25, text=self.word, fill=self.font_color,
                                               font=(self.font_name, 35, 'bold'))
        self.cv_time = self.canvas.create_text(200, 60, text=f'Time left: {self.time}', fill=self.font_color,
                                               font=(self.font_name, 35, 'bold'))
        self.canvas.grid(row=0, column=0, columnspan=2)
        # Label
        self.cpm_count = IntVar()
        self.cpm = Label(textvariable=self.cpm_count, font=self.font_name, bg=self.background_color,
                         highlightthickness=0)
        self.cpm_count.set(f'CPM: 0')
        self.cpm.grid(row=1, column=0)
        self.wpm_count = IntVar()
        self.wpm = Label(textvariable=self.wpm_count, font=self.font_name, bg=self.background_color,
                         highlightthickness=0)
        self.wpm_count.set(f'WPM: 0')
        self.wpm.grid(row=1, column=1)
        # Entry
        self.entry = Entry(width=50)
        self.entry.bind('<Key>', lambda event, second=self.time: self.count_down(second))
        self.entry.bind('<space>', self.do_check, add='+')
        self.entry.bind('<space>', self.next_word, add='+')
        self.entry.grid(row=2, column=0, columnspan=2, pady=15)
        # Run
        self.root.mainloop()

    # Function
    def count_down(self, second):
        self.entry.unbind('<Key>')
        if second > 0:
            self.timer = self.root.after(1000, self.count_down, second - 1)
            second_text = f'{second}'
        if second < 10:
            second_text = f'0{second}'
            self.canvas.itemconfig(self.cv_time, fill='red')
        self.canvas.itemconfig(self.cv_time, text=f'Time left: {second_text}')
        if second == 0:
            self.root.after_cancel(self.timer)
            self.see_review()

    def next_word(self, event):
        self.word = choice(self.words)
        self.canvas.itemconfig(self.cv_word, text=self.word, fill=self.font_color)
        self.entry.delete(0, 'end')

    def do_check(self, event):
        if self.entry.get().strip() == self.word:
            self.word_correct += 1
            self.wpm_count.set(f'WPM: {self.word_correct}')
            self.character_correct += len(self.word)
            self.cpm_count.set(f'WPM: {self.character_correct}')
        elif self.entry.get().strip() != "":
            self.result[self.word] = self.entry.get().strip()

    def see_review(self):
        messagebox.showinfo(title='Result🌞', message=f'CPM: {self.character_correct}, WPM: {self.word_correct}\n'
                                                      f'Review the result in app.👀')
        result = '\n'.join([f"It's {word[0]} instead of {word[1]}" for word in self.result.items()])
        self.canvas.itemconfig(self.cv_word, text="🧸🧸🧸🧸🧸", fill=self.font_color)
        self.canvas.itemconfig(self.cv_time, text=f"Time's up❗️")
        self.entry.config(state='disabled')
        self.review = Label(text=result, font=self.font_name)
        self.review.grid(row=3, column=0, columnspan=2)
