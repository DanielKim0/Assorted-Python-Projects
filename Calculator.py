from tkinter import *
from tkinter import ttk

class Calculator:
    def __init__(self):
        self.expression = ""
        self.num_label = ttk.Label(root)
        self.num_label.grid(row = 0, column = 0, columnspan = 4)
        self.disabled = False

        def text(x):
            return(lambda: add_digit(x))

        def add_digit(num):
            if not self.disabled:
                self.expression += str(num)
                self.num_label.config(text=self.expression)

        def clear_digits():
            self.expression = ""
            self.num_label.config(text=self.expression)
            self.disabled = False

        def backspace():
            if not self.disabled:
                self.expression = self.expression[:-1]
                self.num_label.config(text=self.expression)

        def evaluate(): # errors
            if not self.disabled:
                self.expression.replace("^", "**")
                expression = self.expression.split()
                for num in range(len(expression)):
                    while expression[num][0] == "0":
                        expression[num] = expression[num][1:]
                try: self.expression = str(eval(" ".join(expression)))
                except SyntaxError:
                    self.expression = "Error! Press \"C\" to clear!"
                    self.disabled = True
                self.num_label.config(text=self.expression)

        #All the buttons on the calculator
        ttk.Button(root, text="+", command=lambda: add_digit(" + ")).grid(row=1, column=3)
        ttk.Button(root, text="-", command=lambda: add_digit(" - ")).grid(row=2, column=3)
        ttk.Button(root, text="*", command=lambda: add_digit(" * ")).grid(row=3, column=3)
        ttk.Button(root, text="/", command=lambda: add_digit(" / ")).grid(row=4, column=3)
        ttk.Button(root, text="^", command=lambda: add_digit(" ^ ")).grid(row=5, column=2)
        ttk.Button(root, text=".", command=lambda: add_digit(".")).grid(row=4, column=2)
        ttk.Button(root, text="(", command=lambda: add_digit("(")).grid(row=6, column=0)
        ttk.Button(root, text=")", command=lambda: add_digit(")")).grid(row=6, column=1)
        ttk.Button(root, text="mod", command=lambda: add_digit(" % ")).grid(row=5, column=0)
        ttk.Button(root, text="intdiv", command=lambda: add_digit(" // ")).grid(row=5, column=1)
        for x in range(1, 10):
            ttk.Button(root, text = x, command = text(x)).grid(row=(x - 1) // 3 + 1, column=(x - 1) % 3)
        ttk.Button(root, text="0", command=lambda: add_digit(0)).grid(row=4, column=1)
        ttk.Button(root, text="=", command=lambda: evaluate()).grid(row=5, column=3, rowspan=2, sticky="nsew")
        ttk.Button(root, text="C", command=lambda: clear_digits()).grid(row=6, column=2)
        ttk.Button(root, text="Back", command=lambda: backspace()).grid(row=4, column=0)

root = Tk()
calc = Calculator()
root.mainloop()