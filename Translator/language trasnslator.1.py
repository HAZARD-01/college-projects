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
    try:
        translated_text = translator.translate(text, dest=destination_lang_code)
        output_text.delete("1.0", "end")
        output_text.insert("1.0", translated_text.text)
    except Exception as e:
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Translation error: {str(e)}")



app = tk.Tk()
app.title("Language Translator")
app.configure(bg="lightblue")


frame = ttk.Frame(app, padding=(20, 20))  
frame.grid(row=0, column=0)

style = ttk.Style()
style.configure("TFrame", background="lightblue")  



style.configure("TLabel", background="lightyellow", font=("Helvetica", 12))  

input_label = ttk.Label(frame, text="Enter text to translate:")
input_label.grid(row=0, column=0, pady=(20, 4))

input_text = tk.Text(frame, height=10, width=50, font=("Helvetica", 12))  
input_text.grid(row=1, column=0)

output_label = ttk.Label(frame, text="Translated text:")
output_label.grid(row=2, column=0, pady=(25, 4))

output_text = tk.Text(frame, height=10, width=50, font=("Helvetica", 12))  
output_text.grid(row=3, column=0)

destination_language_label = ttk.Label(frame, text="Select language:")
destination_language_label.grid(row=6, column=0, pady=(20, 4))


style.configure("TCombobox", fieldbackground="white")  

language_box = ttk.Combobox(frame, values=[name for _, name in languages], width=37)
language_box.grid(row=7, column=0, pady=(5, 10))
language_box.set(languages[0][1])


style.configure("Translate.TButton", foreground="Royalblue", background="lightblue", font=("Helvetica", 12, "bold"))


style.configure("Translate.TButton", padding=(20, 10))  

translate_button = ttk.Button(frame, text="Translate", command=translate_text, style="Translate.TButton")
translate_button.grid(row=8, column=0, pady=(0, 10))

app.mainloop()