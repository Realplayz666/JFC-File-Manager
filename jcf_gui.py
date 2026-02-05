"""
JCF Compressor - Windows GUI Application
A graphical interface for compressing and decompressing .jcf files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pathlib import Path

# Import the JCF compressor library
from jcf_compressor import JCFCompressor, JCFError


class JCFCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JCF Compressor - Windows Edition")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.primary_color = "#667eea"
        self.secondary_color = "#764ba2"
        self.bg_color = "#f5f5f5"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
        
        # Current file
        self.current_file = None
        self.operation_mode = "compress"  # compress or decompress
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🗜️ JCF Compressor",
            font=("Segoe UI", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="JSON Compressed Format - Compress Any File Type",
            font=("Segoe UI", 10),
            bg=self.primary_color,
            fg="white"
        )
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mode selection
        mode_frame = tk.Frame(content_frame, bg=self.bg_color)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            mode_frame,
            text="Select Operation:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        self.mode_var = tk.StringVar(value="compress")
        
        compress_radio = ttk.Radiobutton(
            mode_frame,
            text="Compress File",
            variable=self.mode_var,
            value="compress",
            command=self.on_mode_change
        )
        compress_radio.pack(side=tk.LEFT, padx=5)
        
        decompress_radio = ttk.Radiobutton(
            mode_frame,
            text="Decompress File",
            variable=self.mode_var,
            value="decompress",
            command=self.on_mode_change
        )
        decompress_radio.pack(side=tk.LEFT, padx=5)
        
        # File selection area
        file_frame = tk.LabelFrame(
            content_frame,
            text="File Selection",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Drag and drop area (simulated)
        self.drop_area = tk.Frame(
            file_frame,
            bg="white",
            relief=tk.RIDGE,
            borderwidth=2,
            height=150
        )
        self.drop_area.pack(fill=tk.X, pady=(0, 15))
        self.drop_area.pack_propagate(False)
        
        drop_icon = tk.Label(
            self.drop_area,
            text="📁",
            font=("Segoe UI", 40),
            bg="white"
        )
        drop_icon.pack(pady=(20, 10))
        
        drop_text = tk.Label(
            self.drop_area,
            text="Click 'Browse' to select a file",
            font=("Segoe UI", 11),
            bg="white",
            fg=self.primary_color
        )
        drop_text.pack()
        
        # Browse button
        browse_btn = tk.Button(
            file_frame,
            text="📂 Browse Files",
            font=("Segoe UI", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            cursor="hand2",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            command=self.browse_file
        )
        browse_btn.pack()
        
        # File info display
        self.info_frame = tk.LabelFrame(
            content_frame,
            text="File Information",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            padx=20,
            pady=15
        )
        self.info_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.info_text = tk.Text(
            self.info_frame,
            height=6,
            font=("Consolas", 9),
            bg="white",
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.info_text.pack(fill=tk.X)
        self.info_text.insert("1.0", "No file selected")
        self.info_text.config(state=tk.DISABLED)
        
        # Action buttons
        button_frame = tk.Frame(content_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X)
        
        self.action_btn = tk.Button(
            button_frame,
            text="Compress to .jcf",
            font=("Segoe UI", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            cursor="hand2",
            padx=40,
            pady=15,
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self.perform_action
        )
        self.action_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Segoe UI", 12),
            bg="#e0e0e0",
            fg="#333",
            activebackground="#d0d0d0",
            cursor="hand2",
            padx=20,
            pady=15,
            relief=tk.FLAT,
            command=self.clear_file
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=300
        )
        
        # Footer
        footer = tk.Label(
            self.root,
            text="JCF Format v1.0 - Custom Compression System",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg="#999"
        )
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def on_mode_change(self):
        self.operation_mode = self.mode_var.get()
        self.clear_file()
        
        if self.operation_mode == "compress":
            self.action_btn.config(text="Compress to .jcf")
        else:
            self.action_btn.config(text="Decompress File")
    
    def browse_file(self):
        if self.operation_mode == "compress":
            filename = filedialog.askopenfilename(
                title="Select a file to compress",
                filetypes=[("All Files", "*.*")]
            )
        else:
            filename = filedialog.askopenfilename(
                title="Select a JCF file to decompress",
                filetypes=[("JCF Files", "*.jcf"), ("All Files", "*.*")]
            )
        
        if filename:
            self.load_file(filename)
    
    def load_file(self, filepath):
        self.current_file = filepath
        self.action_btn.config(state=tk.NORMAL)
        
        # Update info display
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        
        file_size = os.path.getsize(filepath)
        file_name = os.path.basename(filepath)
        
        info = f"File Name: {file_name}\n"
        info += f"File Path: {filepath}\n"
        info += f"File Size: {self.format_bytes(file_size)}\n"
        
        if self.operation_mode == "decompress" and filepath.endswith('.jcf'):
            try:
                jcf_info = JCFCompressor.get_info(filepath)
                info += f"\n--- JCF File Info ---\n"
                info += f"Original Filename: {jcf_info['filename']}\n"
                info += f"Original Size: {self.format_bytes(jcf_info['original_size'])}\n"
                info += f"Compressed Size: {self.format_bytes(jcf_info['compressed_size'])}\n"
                info += f"Compression Ratio: {jcf_info['compression_ratio']:.2f}%\n"
            except JCFError as e:
                info += f"\nError reading JCF info: {e}\n"
        
        self.info_text.insert("1.0", info)
        self.info_text.config(state=tk.DISABLED)
    
    def perform_action(self):
        if not self.current_file:
            return
        
        self.action_btn.config(state=tk.DISABLED)
        self.progress.pack(pady=10)
        self.progress.start(10)
        
        # Use after to prevent GUI freezing
        self.root.after(100, self._perform_action_worker)
    
    def _perform_action_worker(self):
        try:
            if self.operation_mode == "compress":
                # Ask for output location
                default_name = os.path.basename(self.current_file) + ".jcf"
                output_file = filedialog.asksaveasfilename(
                    title="Save compressed file as",
                    defaultextension=".jcf",
                    initialfile=default_name,
                    filetypes=[("JCF Files", "*.jcf")]
                )
                
                if output_file:
                    result_path = JCFCompressor.compress_file(self.current_file, output_file)
                    info = JCFCompressor.get_info(result_path)
                    
                    messagebox.showinfo(
                        "Compression Successful",
                        f"File compressed successfully!\n\n"
                        f"Original Size: {self.format_bytes(info['original_size'])}\n"
                        f"Compressed Size: {self.format_bytes(info['compressed_size'])}\n"
                        f"Space Saved: {info['compression_ratio']:.2f}%\n\n"
                        f"Saved to: {result_path}"
                    )
            else:
                # Ask for output location
                try:
                    jcf_info = JCFCompressor.get_info(self.current_file)
                    default_name = jcf_info['filename']
                except:
                    default_name = "decompressed_file"
                
                output_file = filedialog.asksaveasfilename(
                    title="Save decompressed file as",
                    initialfile=default_name
                )
                
                if output_file:
                    result_path = JCFCompressor.decompress_file(self.current_file, output_file)
                    
                    messagebox.showinfo(
                        "Decompression Successful",
                        f"File decompressed successfully!\n\n"
                        f"Saved to: {result_path}"
                    )
        
        except JCFError as e:
            messagebox.showerror("Error", f"Operation failed:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.action_btn.config(state=tk.NORMAL)
    
    def clear_file(self):
        self.current_file = None
        self.action_btn.config(state=tk.DISABLED)
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", "No file selected")
        self.info_text.config(state=tk.DISABLED)
    
    @staticmethod
    def format_bytes(bytes_size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"


def main():
    root = tk.Tk()
    app = JCFCompressorGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
