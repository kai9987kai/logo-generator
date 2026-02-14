import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import glob

# Ensure Cairo DLLs are loaded
if os.name == 'nt':
    os.add_dll_directory(os.getcwd())

from logo_generator import LogoGenerator, ColorPalette

class LogoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Logo Generator")
        self.root.geometry("700x800")
        self.root.configure(bg="#1e1e2e")
        
        self.generator = LogoGenerator(width=500, height=500)
        self.current_batch = []
        self.current_index = 0
        self.output_dir = "gui_logos"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.setup_ui()

    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e2e")
        style.configure("TLabel", background="#1e1e2e", foreground="#ffffff", font=("Arial", 12))
        style.configure("TEntry", fieldbackground="#2e2e3e", foreground="#ffffff", borderwidth=0)
        style.configure("TButton", font=("Arial", 10, "bold"))

        # Main Container
        main_frame = tk.Frame(self.root, bg="#1e1e2e", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Header / Input Area
        input_frame = tk.Frame(main_frame, bg="#1e1e2e")
        input_frame.pack(fill="x", pady=(0, 20))

        tk.Label(input_frame, text="Enter Logo Text:", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#ffffff").pack(side="left", padx=(0, 10))
        self.text_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#2e2e3e", fg="#ffffff", insertbackground="white", borderwidth=5, relief="flat")
        self.text_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.text_entry.insert(0, "LOGO")

        self.gen_button = tk.Button(input_frame, text="GENERATE", command=self.generate_logos, bg="#4a4ae2", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=20, pady=10, cursor="hand2")
        self.gen_button.pack(side="right")

        # Viewport Area (Carousel)
        self.viewport_frame = tk.Frame(main_frame, bg="#1a1a2e", bd=2, relief="flat")
        self.viewport_frame.pack(expand=True, fill="both")

        # Navigation Buttons (overlay-style layout)
        nav_frame = tk.Frame(self.viewport_frame, bg="#1a1a2e")
        nav_frame.pack(fill="x", side="top", pady=10)

        self.prev_btn = tk.Button(nav_frame, text="Previous", command=self.show_prev, bg="#3b3b4f", fg="#a0a0b0", font=("Arial", 10, "bold"), relief="flat", padx=15, pady=5, cursor="hand2", state="disabled")
        self.prev_btn.pack(side="left", padx=20)

        # Dot indicators
        self.dots_frame = tk.Frame(nav_frame, bg="#1a1a2e")
        self.dots_frame.pack(side="left", expand=True)
        self.dot_labels = []

        self.next_btn = tk.Button(nav_frame, text="Next", command=self.show_next, bg="#2d6e35", fg="#ffffff", font=("Arial", 10, "bold"), relief="flat", padx=20, pady=5, cursor="hand2", state="disabled")
        self.next_btn.pack(side="right", padx=20)

        # Image Display
        self.image_label = tk.Label(self.viewport_frame, bg="#1a1a2e")
        self.image_label.pack(expand=True, pady=20)

        # Status / Instructions
        self.status_label = tk.Label(main_frame, text="Enter text and click Generate to start", font=("Arial", 10, "italic"), bg="#1e1e2e", fg="#6272a4")
        self.status_label.pack(pady=10)

    def update_dots(self):
        # Clear old dots
        for d in self.dot_labels:
            d.destroy()
        self.dot_labels = []
        
        num_logos = len(self.current_batch)
        if num_logos == 0: return
        
        for i in range(num_logos):
            color = "#4ade80" if i == self.current_index else "#4a4a5e"
            dot = tk.Label(self.dots_frame, text="●", font=("Arial", 12), bg="#1a1a2e", fg=color)
            dot.pack(side="left", padx=5)
            self.dot_labels.append(dot)

    def generate_logos(self):
        text = self.text_entry.get().strip() or "LOGO"
        self.gen_button.config(state="disabled", text="GENERATING...")
        self.status_label.config(text="Creating variants, please wait...")
        
        # Run generation in a separate thread to keep UI responsive
        threading.Thread(target=self._run_generation, args=(text,), daemon=True).start()

    def _run_generation(self, text):
        try:
            # Clear previous files in output dir
            files = glob.glob(os.path.join(self.output_dir, "*.png"))
            for f in files:
                try: os.remove(f)
                except: pass
            
            new_batch = []
            for i in range(5):
                config = self.generator._random_config()
                config["text"] = text
                surface = self.generator.generate(config)
                path = os.path.join(self.output_dir, f"logo_{i}.png")
                self.generator.save(surface, path)
                new_batch.append(path)
            
            self.root.after(0, self._on_generation_complete, new_batch)
        except Exception as e:
            import traceback
            with open("gui_error.log", "w") as f:
                traceback.print_exc(file=f)
            traceback.print_exc()
            error_msg = f"{type(e).__name__}: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", f"Generation failed: {error_msg}"))
            self.root.after(0, lambda: self.gen_button.config(state="normal", text="GENERATE"))

    def _on_generation_complete(self, batch):
        self.current_batch = batch
        self.current_index = 0
        self.gen_button.config(state="normal", text="GENERATE")
        self.status_label.config(text=f"Generated {len(batch)} variations")
        self.update_nav_buttons()
        self.display_current_logo()

    def display_current_logo(self):
        if not self.current_batch: return
        
        path = self.current_batch[self.current_index]
        img = Image.open(path)
        # Resize to fit display if needed
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)
        self.update_dots()

    def update_nav_buttons(self):
        if not self.current_batch:
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            return
            
        self.prev_btn.config(state="normal" if self.current_index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.current_index < len(self.current_batch) - 1 else "disabled")
        
        # Highlight next button like in image (green)
        if self.current_index < len(self.current_batch) - 1:
            self.next_btn.config(bg="#2d6e35")
        else:
            self.next_btn.config(bg="#3b3b4f")

    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current_logo()
            self.update_nav_buttons()

    def show_next(self):
        if self.current_index < len(self.current_batch) - 1:
            self.current_index += 1
            self.display_current_logo()
            self.update_nav_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    app = LogoGUI(root)
    root.mainloop()
