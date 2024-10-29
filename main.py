import customtkinter as ctk
from tkinter import ttk, filedialog
from PIL import Image, TiffImagePlugin
import os

class ImageExtracor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image data Extractor")
        self.geometry("600x550")
        self.resizable(False, False)

        ctk.set_appearance_mode("green")
        ctk.set_default_color_theme("green")

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Size", "Resolution", "Color depth", "Compression"),
                                 show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Resolution", text="Resolution")
        self.tree.heading("Color depth", text="Color depth")
        self.tree.heading("Compression", text="Compression")

        self.tree.column("ID", width=60)
        self.tree.column("Name", width=150)
        self.tree.column("Size", width=100)
        self.tree.column("Resolution", width=100)
        self.tree.column("Color depth", width=100)
        self.tree.column("Compression", width=100)

        self.tree.pack(pady=20)

        self.directory_button = ctk.CTkButton(self, text="Выбрать директорию", command=self.ask_directory_button)
        self.directory_button.pack(pady=30)

        self.file_button = ctk.CTkButton(self, text="Выбрать файл", command=self.ask_file_button)
        self.file_button.pack(pady=10)

        self.counter = 1

    def add_data(self, files):
        for file in files:
            name = os.path.basename(file)
            size = os.path.getsize(file)
            with Image.open(file) as img:
                width, height = img.size
                size = str(width) + 'x' + str(height)
                dpi = img.info.get('dpi')

                color_depth = {
                    '1': '1-bit',
                    'L': '8-bit',
                    'P': '8-bit',
                    'RGB': '3x8-bit',
                    'RGBA': '4x8-bit',
                    'CMYK': '4x8-bit',
                    'YCbCr': '3x8-bit',
                    'LAB': '3x8-bit',
                    'HSV': '3x8-bit',
                    'I': '32-bit',
                    'F': '32-bit'
                }.get(img.mode, f"Unknown ({img.mode})")
                compression = img.info.get('compression', 'No compression info')
                if isinstance(img, TiffImagePlugin.TiffImageFile):
                    compression = TiffImagePlugin.COMPRESSION_INFO.get(img.tag_v2.get(259), "No compression info")
            self.tree.insert("", "end", values=(self.counter, name, size, f'{int(dpi[0])} x {int(dpi[1])}' if dpi else 'N/A', color_depth, compression))
            self.counter += 1
        

    def ask_directory_button(self):
        directory = filedialog.askdirectory()
        files_temp = os.listdir(directory)
        files = []
        for file in files_temp:
            if (file.endswith(('.png', '.PNG')) or file.endswith(('.jpg', '.JPG')) or file.endswith(('.gif', '.GIF')) or 
                file.endswith(('.tif', '.TIF')) or file.endswith(('.bmp', '.BMP')) or file.endswith(('.pcx', '.PCX'))):
                files.append((os.path.join(directory, file)))
        self.add_data(files)
    
    def ask_file_button(self):
        files = []
        files.append(filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.gif;*.tif;*.bmp;*.pcx")]))
        self.add_data(files)

if __name__ == "__main__":
    app = ImageExtracor()
    app.mainloop()