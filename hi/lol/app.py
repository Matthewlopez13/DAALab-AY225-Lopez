import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import os

# Global variable to store dataset
data = []

def load_dataset():
    """Load data from dataset.txt"""
    global data
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_path = os.path.join(script_dir, 'dataset.txt')
        
        with open(dataset_path, 'r') as f:
            data = [int(line.strip()) for line in f if line.strip()]
        print(f"✓ Loaded {len(data)} elements from {dataset_path}")
        return True
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def bubble_sort(arr):
    """
    Sorts an array using the bubble sort algorithm in descending order.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    n = len(arr)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    
    end_time = time.time()
    return arr, end_time - start_time


def insertion_sort(arr):
    """
    Sorts an array using the insertion sort algorithm in descending order.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    end_time = time.time()
    return arr, end_time - start_time


def merge_sort(arr):
    """
    Sorts an array using the merge sort algorithm in descending order.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])
        return merge(left, right)
    
    sorted_arr = merge_sort_helper(arr)
    end_time = time.time()
    return sorted_arr, end_time - start_time


class SortingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Advanced Sorting Algorithm Analyzer")
        self.root.geometry("1200x900")
        self.root.configure(bg="#0a0e27")
        
        # Modern gradient-like color scheme
        self.bg_color = "#0a0e27"
        self.accent_color = "#1a2847"
        self.text_color = "#ffffff"
        self.button_colors = {
            "bubble": "#00d4ff",
            "insertion": "#ff006e",
            "merge": "#00ff41"
        }
        
        # ===== PREMIUM HEADER WITH 3D EFFECT =====
        header_frame = tk.Frame(root, bg="#0f1535", highlightthickness=3, highlightcolor="#00d4ff", highlightbackground="#00d4ff")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Shadow effect
        shadow1 = tk.Frame(header_frame, bg="#1a2555", height=2)
        shadow1.pack(fill=tk.X, side=tk.TOP)
        
        title = tk.Label(header_frame, text="⚡ SORTING ALGORITHM ANALYZER", 
                         font=("Segoe UI", 28, "bold"), 
                         bg="#0f1535", fg="#00d4ff")
        title.pack(pady=20, padx=20)
        
        subtitle = tk.Label(header_frame, text="Professional Performance Analysis Tool | Real-time Processing", 
                           font=("Segoe UI", 11, "italic"), 
                           bg="#0f1535", fg="#00ffff")
        subtitle.pack(pady=(0, 15), padx=20)
        
        # Shadow effect
        shadow2 = tk.Frame(header_frame, bg="#1a2555", height=2)
        shadow2.pack(fill=tk.X, side=tk.BOTTOM)
        
        # ===== MODERN BUTTONS SECTION WITH 3D EFFECT =====
        button_container = tk.Frame(root, bg="#0a0e27", highlightthickness=0)
        button_container.pack(pady=25)
        
        # Create 3D button effect with shadow
        button_frame = tk.Frame(button_container, bg="#0a0e27")
        button_frame.pack(side=tk.TOP, padx=20)
        
        self.bubble_btn = self.create_3d_button(
            button_frame, 
            "🔄\nBUBBLE\nSORT", 
            lambda: self.run_sort("bubble"), 
            self.button_colors["bubble"],
            0
        )
        
        self.insertion_btn = self.create_3d_button(
            button_frame, 
            "➡️\nINSERTION\nSORT", 
            lambda: self.run_sort("insertion"), 
            self.button_colors["insertion"],
            1
        )
        
        self.merge_btn = self.create_3d_button(
            button_frame, 
            "⛓️\nMERGE\nSORT", 
            lambda: self.run_sort("merge"), 
            self.button_colors["merge"],
            2
        )
        
        # ===== RESULTS LABEL WITH GRADIENT EFFECT =====
        results_header = tk.Frame(root, bg="#1a2847", highlightthickness=2, highlightcolor="#00d4ff")
        results_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        
        results_label = tk.Label(results_header, text="📊 SORTED OUTPUT:", 
                                 font=("Segoe UI", 13, "bold"), 
                                 bg="#1a2847", fg="#00ff41")
        results_label.pack(anchor="w", padx=15, pady=10)
        
        # ===== MODERN RESULTS TEXT AREA WITH 3D BORDERS =====
        text_container = tk.Frame(root, bg="#0a0e27")
        text_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Outer border for 3D effect
        outer_border = tk.Frame(text_container, bg="#00d4ff", highlightthickness=0)
        outer_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Inner frame
        inner_frame = tk.Frame(outer_border, bg="#1a2555")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        self.result_text = scrolledtext.ScrolledText(
            inner_frame, 
            height=28, 
            width=142,
            font=("Consolas", 9),
            bg="#121a3a",
            fg="#00ff41",
            insertbackground="#00ff41",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def create_3d_button(self, parent, text, command, color, column):
        """Create a 3D styled button"""
        # Outer shadow frame
        shadow_frame = tk.Frame(parent, bg="#000000")
        shadow_frame.grid(row=0, column=column, padx=12, pady=12, sticky="nsew")
        
        # Main button
        btn = tk.Button(
            shadow_frame,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg="#000000",
            padx=22, pady=24,
            border=0,
            cursor="hand2",
            activebackground=self.lighten_color(color),
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=2
        )
        btn.pack(padx=3, pady=3)
        
        return btn
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 40)
        g = min(255, g + 40)
        b = min(255, b + 40)
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        
    def run_sort(self, sort_type):
        """Run sorting algorithm in a separate thread"""
        self.disable_buttons()
        thread = threading.Thread(target=self.execute_sort, args=(sort_type,))
        thread.start()
    
    def disable_buttons(self):
        self.bubble_btn.config(state="disabled")
        self.insertion_btn.config(state="disabled")
        self.merge_btn.config(state="disabled")
    
    def enable_buttons(self):
        self.bubble_btn.config(state="normal")
        self.insertion_btn.config(state="normal")
        self.merge_btn.config(state="normal")
    
    def execute_sort(self, sort_type):
        """Execute the selected sorting algorithm"""
        if not data:
            messagebox.showerror("Error", "No data loaded!")
            self.enable_buttons()
            return
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        
        emoji = {"bubble": "🔄", "insertion": "➡️", "merge": "⛓️"}[sort_type]
        
        self.result_text.insert(tk.END, f"{emoji} {sort_type.upper()} SORT - PROCESSING\n")
        self.result_text.insert(tk.END, "█" * 142 + "\n\n")
        self.result_text.insert(tk.END, "⏳ Sorting in progress...\n")
        self.result_text.update()
        
        try:
            arr_copy = data.copy()
            
            if sort_type == "bubble":
                sorted_arr, time_taken = bubble_sort(arr_copy)
            elif sort_type == "insertion":
                sorted_arr, time_taken = insertion_sort(arr_copy)
            elif sort_type == "merge":
                sorted_arr, time_taken = merge_sort(arr_copy)
            
            # Clear and display results
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"{emoji} {sort_type.upper()} SORT - COMPLETED\n")
            self.result_text.insert(tk.END, "█" * 142 + "\n\n")
            self.result_text.insert(tk.END, f"⏱️  Time: {time_taken:.6f}s ({time_taken*1000:.2f}ms)\n\n")
            self.result_text.insert(tk.END, str(sorted_arr))
            
        except Exception as e:
            self.result_text.insert(tk.END, f"❌ ERROR: {str(e)}\n")
        
        self.result_text.config(state="disabled")
        self.enable_buttons()


if __name__ == "__main__":
    # Load dataset
    if not load_dataset():
        print("Error: dataset.txt not found!")
        exit(1)
    
    # Create GUI
    root = tk.Tk()
    gui = SortingGUI(root)
    root.mainloop()