import tkinter as tk
from tkinter import filedialog
from docx import Document

def select_file():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename()  
    return file_path

def select_folder():
    root = tk.Tk()
    root.withdraw() 
    folder_path = filedialog.asksaveasfilename(defaultextension='.txt')  
    return folder_path

def read_word_file(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        line = para.text.strip()  # Elimina espacios y tabulaciones al inicio y final
        line = line.replace("REEL: 1", "")  # Elimina 'REEL: 1'
        if line:  # Solo añade la línea si contiene texto
            text.append(line)
    return text

def save_to_txt(text, folder_path):
    with open(folder_path, "w") as txt_file:
        for line in text:
            txt_file.write(line+"\n")

def main():
    print("Selecciona el archivo .docx")
    file_path = select_file()
    print("Selecciona el directorio para guardar el archivo .txt")
    folder_path = select_folder()

    text = read_word_file(file_path)
    save_to_txt(text, folder_path)

if __name__ == "__main__":
    main()
