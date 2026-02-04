"""
Sorting Algorithm Stress Test - All-in-One Application
Design & Analysis of Algorithms Lab - Prelim Exam

Complete implementation with sorting algorithms, CSV processing, and GUI
"""

import time
import csv
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
from typing import List, Tuple, Callable, Any


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class Record:
    """Represents a single CSV record"""
    def __init__(self, id_val: int, first_name: str, last_name: str):
        self.id = id_val
        self.first_name = first_name
        self.last_name = last_name
    
    def __repr__(self):
        return f"Record(ID={self.id}, First={self.first_name}, Last={self.last_name})"


# ============================================================================
# SORTING ALGORITHMS
# ============================================================================

def bubble_sort(arr: List[Record], key_func: Callable[[Record], Any], reverse: bool = False) -> Tuple[List[Record], float]:
    """
    Bubble Sort - O(n²) complexity
    Sorts records based on key function in ascending order (or descending if reverse=True)
    """
    start_time = time.time()
    n = len(arr)
    arr_copy = arr.copy()
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            key_j = key_func(arr_copy[j])
            key_j_next = key_func(arr_copy[j + 1])
            
            if reverse:
                should_swap = key_j < key_j_next
            else:
                should_swap = key_j > key_j_next
            
            if should_swap:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        if not swapped:
            break
    
    end_time = time.time()
    return arr_copy, end_time - start_time


def insertion_sort(arr: List[Record], key_func: Callable[[Record], Any], reverse: bool = False) -> Tuple[List[Record], float]:
    """
    Insertion Sort - O(n²) complexity
    Sorts records based on key function
    """
    start_time = time.time()
    n = len(arr)
    arr_copy = arr.copy()
    
    for i in range(1, n):
        key = arr_copy[i]
        key_val = key_func(key)
        j = i - 1
        
        while j >= 0:
            key_j = key_func(arr_copy[j])
            
            if reverse:
                should_insert = key_j < key_val
            else:
                should_insert = key_j > key_val
            
            if should_insert:
                arr_copy[j + 1] = arr_copy[j]
                j -= 1
            else:
                break
        
        arr_copy[j + 1] = key
    
    end_time = time.time()
    return arr_copy, end_time - start_time


def merge_sort(arr: List[Record], key_func: Callable[[Record], Any], reverse: bool = False) -> Tuple[List[Record], float]:
    """
    Merge Sort - O(n log n) complexity
    Sorts records based on key function using divide and conquer
    """
    start_time = time.time()
    
    def merge(left: List[Record], right: List[Record]) -> List[Record]:
        """Merge two sorted lists"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            left_key = key_func(left[i])
            right_key = key_func(right[j])
            
            if reverse:
                should_take_left = left_key >= right_key
            else:
                should_take_left = left_key <= right_key
            
            if should_take_left:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort_helper(arr_slice: List[Record]) -> List[Record]:
        """Recursive merge sort helper"""
        if len(arr_slice) <= 1:
            return arr_slice
        
        mid = len(arr_slice) // 2
        left = merge_sort_helper(arr_slice[:mid])
        right = merge_sort_helper(arr_slice[mid:])
        return merge(left, right)
    
    sorted_arr = merge_sort_helper(arr)
    end_time = time.time()
    return sorted_arr, end_time - start_time


# ============================================================================
# CSV DATA MANAGER
# ============================================================================

class CSVDataManager:
    """Manages loading and accessing CSV data"""
    
    def __init__(self, csv_path: str):
        """Initialize with CSV file path"""
        self.csv_path = csv_path
        self.all_records: List[Record] = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load first 10 records from CSV file"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        self.all_records = []
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                if idx >= 10:  # Only load first 10 records
                    break
                try:
                    record = Record(
                        id_val=int(row['ID']),
                        first_name=row['FirstName'],
                        last_name=row['LastName']
                    )
                    self.all_records.append(record)
                except (ValueError, KeyError) as e:
                    print(f"Warning: Skipping row due to error: {e}")
    
    def get_records(self, n: int) -> List[Record]:
        """Get first N records"""
        return self.all_records[:min(n, len(self.all_records))]
    
    def get_total_count(self) -> int:
        """Get total number of records loaded"""
        return len(self.all_records)
    
    def get_column_keys(self):
        """Return available columns for sorting"""
        return {
            'ID': lambda r: r.id,
            'FirstName': lambda r: r.first_name,
            'LastName': lambda r: r.last_name
        }


# ============================================================================
# GUI APPLICATION
# ============================================================================

class SortingBenchmarkGUI:
    """Professional GUI for sorting algorithm benchmarking"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ SORTING ALGORITHM STRESS TEST")
        self.root.geometry("1400x1050")
        self.root.configure(bg="#0a0e27")
        
        # Modern color scheme
        self.bg_color = "#0a0e27"
        self.accent_color = "#1a2847"
        self.text_color = "#ffffff"
        self.button_colors = {
            "bubble": "#ff6b6b",
            "insertion": "#4ecdc4",
            "merge": "#45b7d1"
        }
        
        # Load CSV data
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Try multiple paths
            csv_paths = [
                os.path.join(script_dir, 'generated_data.csv'),  # In root folder
                os.path.join(script_dir, 'data', 'generated_data.csv'),  # In data folder
            ]
            csv_path = None
            for path in csv_paths:
                if os.path.exists(path):
                    csv_path = path
                    break
            
            if not csv_path:
                raise FileNotFoundError(f"CSV file not found in: {', '.join(csv_paths)}")
            
            self.data_manager = CSVDataManager(csv_path)
            print(f"✓ Loaded {self.data_manager.get_total_count():,} records from CSV at {csv_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
            self.data_manager = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface with modern design"""
        # ===== HEADER =====
        header_frame = tk.Frame(self.root, bg="#0f1535", highlightthickness=0)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Gradient effect with border
        border = tk.Frame(header_frame, bg="#45b7d1", height=3)
        border.pack(fill=tk.X, side=tk.TOP)
        
        title = tk.Label(header_frame, text="⚡ SORTING ALGORITHM STRESS TEST", 
                        font=("Segoe UI", 26, "bold"), 
                        bg="#0f1535", fg="#45b7d1")
        title.pack(pady=18, padx=20)
        
        subtitle = tk.Label(header_frame, 
                           text=f"📊 Processing {self.data_manager.get_total_count():,} Records | Professional CSV Benchmarking Tool", 
                           font=("Segoe UI", 11, "italic"), 
                           bg="#0f1535", fg="#00ffff")
        subtitle.pack(pady=(0, 18), padx=20)
        
        # ===== CONTROL PANEL (Modern Design) =====
        control_frame = tk.Frame(self.root, bg="#1a2847", highlightthickness=0)
        control_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Add subtle border
        control_border = tk.Frame(self.root, bg="#45b7d1", height=1)
        control_border.pack(fill=tk.X, padx=15, pady=(0, 0))
        
        # Column selection
        col_frame = tk.Frame(control_frame, bg="#1a2847")
        col_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(col_frame, text="📁 Sort Column:", font=("Segoe UI", 11, "bold"), 
                bg="#1a2847", fg="#45b7d1").pack(side=tk.LEFT, padx=(0, 10))
        
        self.column_var = tk.StringVar(value="ID")
        self.column_menu = ttk.Combobox(col_frame, textvariable=self.column_var, 
                                        values=["ID", "FirstName", "LastName"],
                                        state="readonly", width=12, font=("Segoe UI", 10))
        self.column_menu.pack(side=tk.LEFT, padx=5)
        self.column_menu.configure(foreground="black")
        
        # Row count selection
        row_frame = tk.Frame(control_frame, bg="#1a2847")
        row_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(row_frame, text="🔢 Rows (N):", font=("Segoe UI", 11, "bold"), 
                bg="#1a2847", fg="#45b7d1").pack(side=tk.LEFT, padx=(0, 10))
        
        self.row_var = tk.StringVar(value="1000")
        self.row_menu = ttk.Combobox(row_frame, textvariable=self.row_var, 
                                     values=["1000", "10000", "100000"],
                                     state="readonly", width=12, font=("Segoe UI", 10))
        self.row_menu.pack(side=tk.LEFT, padx=5)
        self.row_menu.configure(foreground="black")
        
        # Sort order
        order_frame = tk.Frame(control_frame, bg="#1a2847")
        order_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(order_frame, text="⬆️ Order:", font=("Segoe UI", 11, "bold"), 
                bg="#1a2847", fg="#45b7d1").pack(side=tk.LEFT, padx=(0, 10))
        
        self.order_var = tk.StringVar(value="Ascending")
        self.order_menu = ttk.Combobox(order_frame, textvariable=self.order_var, 
                                       values=["Ascending", "Descending"],
                                       state="readonly", width=12, font=("Segoe UI", 10))
        self.order_menu.pack(side=tk.LEFT, padx=5)
        self.order_menu.configure(foreground="black")
        
        # ===== BUTTON PANEL (Modern Buttons) =====
        button_frame = tk.Frame(self.root, bg="#0a0e27")
        button_frame.pack(pady=20)
        
        self.bubble_btn = self.create_modern_button(button_frame, "🔄\nBUBBLE\nSORT", 
                                            lambda: self.run_sort("bubble"), 
                                            self.button_colors["bubble"], 0)
        
        self.insertion_btn = self.create_modern_button(button_frame, "➡️\nINSERTION\nSORT", 
                                               lambda: self.run_sort("insertion"), 
                                               self.button_colors["insertion"], 1)
        
        self.merge_btn = self.create_modern_button(button_frame, "⛓️\nMERGE\nSORT", 
                                           lambda: self.run_sort("merge"), 
                                           self.button_colors["merge"], 2)
        
        # ===== LOADING & STATUS AREA =====
        self.status_frame = tk.Frame(self.root, bg="#0a0e27")
        self.status_frame.pack(pady=(5, 10))
        
        self.loading_label = tk.Label(self.status_frame, text="", font=("Segoe UI", 10), 
                                      bg="#0a0e27", fg="#45b7d1")
        self.loading_label.pack()
        
        # ===== PROGRESS BAR =====
        self.progress_frame = tk.Frame(self.root, bg="#0a0e27")
        self.progress_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.progress_bar = tk.Canvas(self.progress_frame, height=6, bg="#1a2847", highlightthickness=0)
        self.progress_bar.pack(fill=tk.X)
        
        # ===== WARNING LABEL =====
        self.warning_label = tk.Label(self.root, text="", font=("Segoe UI", 10), 
                                      bg="#0a0e27", fg="#ffaa00")
        self.warning_label.pack(pady=(0, 10))
        
        # ===== OUTPUT AREA (Modern Design) =====
        output_header = tk.Frame(self.root, bg="#0a0e27")
        output_header.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        output_label = tk.Label(output_header, text="📊 SORTED RESULTS:", 
                               font=("Segoe UI", 13, "bold"), 
                               bg="#0a0e27", fg="#45b7d1")
        output_label.pack(anchor="w", padx=0, pady=(0, 8))
        
        # Output text area with modern styling
        text_container = tk.Frame(self.root, bg="#0a0e27")
        text_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Modern border effect
        outer_border = tk.Frame(text_container, bg="#45b7d1", highlightthickness=0)
        outer_border.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        inner_frame = tk.Frame(outer_border, bg="#121a3a")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.result_text = scrolledtext.ScrolledText(
            inner_frame, 
            height=15, 
            width=165,
            font=("Consolas", 9),
            bg="#121a3a",
            fg="#45b7d1",
            insertbackground="#45b7d1",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def create_modern_button(self, parent, text, command, color, column):
        """Create a modern styled button with hover effect"""
        btn_frame = tk.Frame(parent, bg="#0a0e27")
        btn_frame.grid(row=0, column=column, padx=15, pady=0, sticky="nsew")
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="#000000",
            padx=25, pady=25,
            border=0,
            cursor="hand2",
            activebackground=self.lighten_color(color),
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=1,
            highlightthickness=0
        )
        btn.pack()
        
        # Add hover effects
        btn.bind("<Enter>", lambda e: btn.config(relief=tk.SUNKEN, bd=3))
        btn.bind("<Leave>", lambda e: btn.config(relief=tk.RAISED, bd=1))
        
        return btn
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 40)
        g = min(255, g + 40)
        b = min(255, b + 40)
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    def update_progress(self, percentage):
        """Update progress bar"""
        self.progress_bar.delete("all")
        bar_width = self.progress_bar.winfo_width()
        if bar_width > 1:
            filled_width = (percentage / 100) * bar_width
            self.progress_bar.create_rectangle(0, 0, filled_width, 6, fill="#45b7d1", outline="")
    
    def disable_buttons(self):
        """Disable all buttons during sorting"""
        self.bubble_btn.config(state="disabled")
        self.insertion_btn.config(state="disabled")
        self.merge_btn.config(state="disabled")
        self.column_menu.config(state="disabled")
        self.row_menu.config(state="disabled")
        self.order_menu.config(state="disabled")
    
    def enable_buttons(self):
        """Enable all buttons"""
        self.bubble_btn.config(state="normal")
        self.insertion_btn.config(state="normal")
        self.merge_btn.config(state="normal")
        self.column_menu.config(state="readonly")
        self.row_menu.config(state="readonly")
        self.order_menu.config(state="readonly")
    
    def run_sort(self, sort_type):
        """Run sorting in separate thread"""
        self.disable_buttons()
        thread = threading.Thread(target=self.execute_sort, args=(sort_type,))
        thread.start()
    
    def execute_sort(self, sort_type):
        """Execute the selected sorting algorithm with real-time loading feedback"""
        if not self.data_manager:
            messagebox.showerror("Error", "Data not loaded!")
            self.enable_buttons()
            return
        
        try:
            # Get parameters
            column = self.column_var.get()
            n = int(self.row_var.get())
            order = self.order_var.get()
            reverse = order == "Descending"
            
            # Check if N exceeds available data
            total = self.data_manager.get_total_count()
            if n > total:
                n = total
            
            # Get key function
            key_funcs = self.data_manager.get_column_keys()
            key_func = key_funcs[column]
            
            emoji = {"bubble": "🔄", "insertion": "➡️", "merge": "⛓️"}[sort_type]
            algo_name = {"bubble": "BUBBLE SORT", "insertion": "INSERTION SORT", "merge": "MERGE SORT"}[sort_type]
            
            # ===== PHASE 1: LOADING CSV =====
            self.loading_label.config(text="⏳ Loading CSV data...", fg="#ffaa00")
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"{emoji} {algo_name} - PROCESSING\n")
            self.result_text.insert(tk.END, "=" * 150 + "\n\n")
            self.result_text.insert(tk.END, f"📋 Parameters:\n")
            self.result_text.insert(tk.END, f"   • Column: {column}\n")
            self.result_text.insert(tk.END, f"   • Rows (N): {n:,}\n")
            self.result_text.insert(tk.END, f"   • Order: {order}\n\n")
            self.result_text.insert(tk.END, f"⏳ Loading CSV...\n")
            self.result_text.config(state="disabled")
            self.root.update()
            
            # Load data with timing
            load_start = time.time()
            records = self.data_manager.get_records(n)
            load_time = time.time() - load_start
            
            # ===== PHASE 2: SORTING =====
            self.loading_label.config(text=f"⏳ Sorting {n:,} records with {algo_name}...", fg="#ffaa00")
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"{emoji} {algo_name} - SORTING IN PROGRESS\n")
            self.result_text.insert(tk.END, "=" * 150 + "\n\n")
            self.result_text.insert(tk.END, f"📋 Parameters:\n")
            self.result_text.insert(tk.END, f"   • Column: {column}\n")
            self.result_text.insert(tk.END, f"   • Rows (N): {n:,}\n")
            self.result_text.insert(tk.END, f"   • Order: {order}\n")
            self.result_text.insert(tk.END, f"   • Data Load Time: {load_time*1000:.3f} ms\n\n")
            self.result_text.insert(tk.END, f"⏳ Sorting in progress...\n")
            self.result_text.config(state="disabled")
            self.root.update()
            
            # Check for O(n²) warnings
            if n > 10000 and sort_type in ["bubble", "insertion"]:
                warning = f"⚠️  WARNING: {algo_name} on {n:,} records will take several minutes!"
                self.warning_label.config(text=warning, fg="#ff6b6b")
                self.root.update()
            else:
                self.warning_label.config(text="")
            
            # Animate progress
            for i in range(0, 90, 10):
                self.update_progress(i)
                self.root.update()
                time.sleep(0.05)
            
            # Sort with timing
            sort_start = time.time()
            if sort_type == "bubble":
                sorted_records, sort_time = bubble_sort(records, key_func, reverse)
            elif sort_type == "insertion":
                sorted_records, sort_time = insertion_sort(records, key_func, reverse)
            elif sort_type == "merge":
                sorted_records, sort_time = merge_sort(records, key_func, reverse)
            sort_end = time.time()
            
            # Complete progress bar
            self.update_progress(100)
            
            # ===== PHASE 3: DISPLAY RESULTS =====
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"{emoji} {algo_name} - ✅ COMPLETED\n")
            self.result_text.insert(tk.END, "=" * 150 + "\n\n")
            
            self.result_text.insert(tk.END, f"⏱️  TIMING RESULTS:\n")
            self.result_text.insert(tk.END, f"   • CSV Load Time:   {load_time*1000:.3f} ms\n")
            self.result_text.insert(tk.END, f"   • Sort Time:       {sort_time:.6f} seconds ({sort_time*1000:.3f} ms)\n")
            self.result_text.insert(tk.END, f"   • Total Time:      {load_time + sort_time:.6f} seconds\n\n")
            
            # Algorithm analysis
            complexity = "O(n²)" if sort_type in ["bubble", "insertion"] else "O(n log n)"
            self.result_text.insert(tk.END, f"🔍 ALGORITHM ANALYSIS:\n")
            self.result_text.insert(tk.END, f"   • Complexity: {complexity}\n")
            self.result_text.insert(tk.END, f"   • Records Sorted: {len(sorted_records):,}\n\n")
            
            # Display all sorted records
            self.result_text.insert(tk.END, f"📊 ALL {len(sorted_records):,} SORTED RECORDS (Sorted by {column}):\n")
            self.result_text.insert(tk.END, "-" * 150 + "\n")
            self.result_text.insert(tk.END, f"{'#':<5} {'ID':<10} {'FirstName':<20} {'LastName':<20}\n")
            self.result_text.insert(tk.END, "-" * 150 + "\n")
            
            for i, record in enumerate(sorted_records, 1):
                self.result_text.insert(tk.END, f"{i:<5} {record.id:<10} {record.first_name:<20} {record.last_name:<20}\n")
            
            self.result_text.insert(tk.END, "\n" + "=" * 150 + "\n")
            self.result_text.insert(tk.END, "✅ Sorting completed successfully!\n")
            
            self.result_text.config(state="disabled")
            self.warning_label.config(text="")
            self.loading_label.config(text="✅ Ready for new sort", fg="#45b7d1")
            
            # Reset progress bar after brief delay
            time.sleep(0.5)
            self.update_progress(0)
            
        except Exception as e:
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"❌ ERROR: {str(e)}\n")
            self.result_text.config(state="disabled")
            self.loading_label.config(text="❌ Error occurred", fg="#ff6b6b")
            messagebox.showerror("Error", f"Sorting failed: {str(e)}")
        
        finally:
            self.enable_buttons()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = SortingBenchmarkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
