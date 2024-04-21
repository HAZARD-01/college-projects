import tkinter as tk
from tkinter import ttk
from googletrans import Translator

languages = [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("ja", "Japanese"),
    ("hi", "Hindi"),
    ("mr", "Marathi"),
]

def translate_text():
    text = input_text.get("1.0", "end-1c")
    destination_lang_code = language_box.get()
    translator = Translator()
    translated_text = translator.translate(text, dest=destination_lang_code)
    output_text.delete("1.0", "end")
    output_text.insert("1.0", translated_text.text)

app = tk.Tk()
app.title("Language Translator")
app.configure(bg="lightblue")  

frame = ttk.Frame(app, padding=10)
frame.grid(row=0, column=0)

input_label = ttk.Label(frame, text="Enter text to translate:", background="lightyellow")
input_label.grid(row=0, column=0, pady=(10, 0))

input_text = tk.Text(frame, height=5, width=40)
input_text.grid(row=1, column=0)

output_label = ttk.Label(frame, text="Translated text:", background="lightyellow")
output_label.grid(row=2, column=0, pady=(10, 0))

output_text = tk.Text(frame, height=5, width=40)
output_text.grid(row=3, column=0)

destination_language_label = ttk.Label(frame, text="Select language:", background="lightyellow")
destination_language_label.grid(row=4, column=0, pady=(10, 0))

language_box = ttk.Combobox(frame, values=[name for _, name in languages], width=37)
language_box.grid(row=5, column=0, pady=(0, 10))
language_box.set(languages[0][1])  

translate_button = ttk.Button(frame, text="Translate", command=translate_text, style="TButton")
translate_button.grid(row=6, column=0, pady=(0, 10))

style = ttk.Style()
style.configure("TButton", foreground="red", background="blue", font=("Helvetica", 12, "bold"))

app.mainloop()
