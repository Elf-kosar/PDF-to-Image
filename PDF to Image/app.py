import fitz  #pdf sayfalarını görüntüye dönüştürmek için, pyMuPDF'in bir parçası
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class PDFToImageConverter:
    def __init__(self, root):
        self.root = root
        self.pdf_path = tk.StringVar()#pdf dosyasının yolunu saklar
        self.output_folder_path = tk.StringVar() #çıktı klasörünün yolunu saklar
        self.initialize_ui() #kullanıcı arayüzünü başlatan fonk.

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="PDF to Image Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_pdf_button = tk.Button(self.root, text="Select PDF", command=self.select_pdf)
        select_pdf_button.pack(pady=(0, 10))

        pdf_label = tk.Label(self.root, textvariable=self.pdf_path)
        pdf_label.pack()

        select_output_folder_button = tk.Button(self.root, text="Select Output Folder", command=self.select_output_folder)
        select_output_folder_button.pack(pady=(0, 10))

        output_folder_label = tk.Label(self.root, textvariable=self.output_folder_path)
        output_folder_label.pack()

        convert_button = tk.Button(self.root, text="Convert to Images", command=self.convert_pdf_to_images)
        convert_button.pack(pady=(20, 40))

    def select_pdf(self):#dosya seçme penceresi açılır
        self.pdf_path.set(filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF files", "*.pdf")]))
    
    def select_output_folder(self):#seçilen klasörün yolunu kaydedilmesi
        self.output_folder_path.set(filedialog.askdirectory(title="Select Output Folder"))
    
    def convert_pdf_to_images(self): #dönüşüm işlemi
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        if not self.output_folder_path.get():
            messagebox.showerror("Error", "Please select an output folder.")
            return

        try:
            # PDF'yi aç
            pdf_document = fitz.open(self.pdf_path.get())
            pdf_name = os.path.splitext(os.path.basename(self.pdf_path.get()))[0]

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)  # Her sayfayı yükle
                pix = page.get_pixmap()  # Sayfayı görüntüye dönüştür 
                image_path = os.path.join(self.output_folder_path.get(), f"{pdf_name}_page_{page_num+1}.png")
                pix.save(image_path)  # Görüntüyü PNG olarak kaydet

            messagebox.showinfo("Success", f"PDF successfully converted to images in {self.output_folder_path.get()}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    root.title("PDF to Image")
    converter = PDFToImageConverter(root)
    root.geometry("400x300")
    root.mainloop()

if __name__ == "__main__":
    main()
