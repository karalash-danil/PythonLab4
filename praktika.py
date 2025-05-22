import tkinter as tk


MorseCode = {
    " ": "",

    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",

    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",

    ",": "--..--",
    ".": ".-.-.-",
    "!": "-.-.--",
    "?": "..--..",
    "-": "-....-",
    "=": "-...-",
    "+": ".-.-.",
    "(": "-.--.",
    ")": "-.--.-",
    "@": ".--.-.",
    "&": ".-..."
}


def text_to_morse(text=""):
    result = ""

    for i in text:
        result+=" "
        if i.upper() in MorseCode:
            result += MorseCode[i.upper()]

    return result[1:]

def morse_to_text(text=""):
    text = text.strip()+" "

    result = ""

    char = ""
    for i in text:
        if i == " ":
            if char == "":
                result+=" "
            else:
                keys = [key for key, val in MorseCode.items() if val == char]
                if len(keys) > 0:
                    result+=keys[0]
            char = ""
        else:
            char += i

    return result   #.capitalize()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x360")
        self.title("Перекладач тексту в Азбуку Морзе")
        self.eval('tk::PlaceWindow . center')

        # --------------------

        self.title1 = tk.Label(self, text="Латиниця", font=("Segoe UI", 16), bg="lightgray")
        self.VarInput = tk.StringVar()
        self.input = tk.Entry(self, textvariable=self.VarInput, font=("Segoe UI", 16))

        self.title2 = tk.Label(self, text="Азбука Морзе", font=("Segoe UI", 16), bg="lightgray")
        self.VarResult = tk.StringVar()
        self.input2 = tk.Entry(self, textvariable=self.VarResult, font=("Roboto", 18))

        # --------------------

        self.title1.pack( pady=5, side="top", fill="x")
        self.input.pack(padx=5,pady=5,side="top",expand=True, fill="both")

        self.input2.pack(padx=5, pady=5, side="bottom", expand=True, fill="both")
        self.title2.pack(pady=5, side="bottom", fill="x")

        # --------------------

        self.VarInput.trace_add("write", self.callback1)
        self.VarResult.trace_add("write", self.callback2)

    def callback1(self,a,b,c):
        self.update_label1()
    def callback2(self,a,b,c):
        self.update_label2()

    def update_label1(self):
        self.VarResult.trace_remove("write",self.VarResult.trace_info()[0][1])
        self.VarResult.set(text_to_morse(self.VarInput.get()))
        self.VarResult.trace_add("write",self.callback2)

    def update_label2(self):
        self.VarInput.trace_remove("write",self.VarInput.trace_info()[0][1])
        self.VarInput.set(morse_to_text(self.VarResult.get()))
        self.VarInput.trace_add("write", self.callback1)

if __name__ == "__main__":
    root = App()
    root.mainloop()