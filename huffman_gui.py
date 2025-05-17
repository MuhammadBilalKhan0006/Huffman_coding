import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
import platform

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression GUI")
        self.root.geometry("800x700")  # Reduced height since size info is removed

        # Determine executable extension based on OS
        self.exe_ext = ".exe" if platform.system() == "Windows" else ""

        # Compile C++ programs if executables don't exist
        self.compile_cpp()

        # Input Text
        tk.Label(root, text="Input Text:").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(root, height=20, width=80)
        self.input_text.pack(pady=5)

        # Buttons
        tk.Button(root, text="Compress", command=self.compress).pack(pady=5)
        tk.Button(root, text="Decompress", command=self.decompress).pack(pady=5)

        # Output: Decompressed Text
        tk.Label(root, text="Decompressed Text:").pack(pady=5)
        self.decompressed_text = scrolledtext.ScrolledText(root, height=20, width=80)
        self.decompressed_text.pack(pady=5)
        self.decompressed_text.config(state="disabled")

    def compile_cpp(self):
        for program in ["encoding", "decoding"]:
            if not os.path.exists(f"{program}{self.exe_ext}"):
                try:
                    subprocess.run(
                        ["g++", f"{program}.cpp", "huffman.cpp", "-o", program],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print(f"Compiled {program} successfully")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Failed to compile {program}: {e.stderr}")
                    return

    def compress(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text to compress")
            return

        with open("input.txt", "w") as f:
            f.write(text)

        try:
            subprocess.run(
                [f"./encoding{self.exe_ext}", "input.txt", "compressed.huf"],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Compression failed: {e.stderr}")
            return

        if os.path.exists("compressed.huf"):
            messagebox.showinfo("Success", "Text compressed to compressed.huf")
        else:
            messagebox.showerror("Error", "Compressed file not found")

    def decompress(self):
        if not os.path.exists("compressed.huf"):
            messagebox.showerror("Error", "Compressed file not found")
            return

        try:
            subprocess.run(
                [f"./decoding{self.exe_ext}", "compressed.huf", "decompressed.txt"],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Decompression failed: {e.stderr}")
            return

        if os.path.exists("decompressed.txt"):
            with open("decompressed.txt", "r") as f:
                decompressed = f.read()
            self.decompressed_text.config(state="normal")
            self.decompressed_text.delete("1.0", tk.END)
            self.decompressed_text.insert(tk.END, decompressed)
            self.decompressed_text.config(state="disabled")
            messagebox.showinfo("Success", "Text decompressed successfully")
        else:
            messagebox.showerror("Error", "Decompressed file not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
