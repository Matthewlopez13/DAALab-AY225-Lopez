import time
import os

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
    
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize by detecting if array is already sorted
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is less than the next element (descending)
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps occurred, array is sorted
        if not swapped:
            break
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return arr, time_taken


# Example usage 
if __name__ == "__main__":
    # Load data from dataset.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, 'dataset.txt')
    
    try:
        with open(dataset_path, 'r') as f:
            data = [int(line.strip()) for line in f if line.strip()]
        
        print(f"Loaded {len(data)} numbers from dataset.txt")
        print(f"First 10 numbers: {data[:10]}")
        print(f"Last 10 numbers: {data[-10:]}\n")
        
        # Perform bubble sort in descending order
        print("Sorting in descending order...")
        sorted_arr, time_taken = bubble_sort(data.copy())
        
        # Display results
        print(f"\nSorted array (descending order):")
        print(sorted_arr)
        print(f"\nTime spent: {time_taken:.6f} seconds")
        print(f"Time spent: {time_taken*1000:.2f} milliseconds")
        
    except FileNotFoundError:
        print("Error: dataset.txt not found!")
        
        # Fallback to test arrays
        test_arrays = [
            [64, 34, 25, 12, 22, 11, 90],
            [5, 1, 4, 2, 8],
            [1, 2, 3, 4, 5],  # Already sorted
            [5, 4, 3, 2, 1],  # Reverse sorted
        ]
        
        for arr in test_arrays:
            print(f"Original: {arr}")
            sorted_arr, time_taken = bubble_sort(arr.copy())
            print(f"Sorted (descending): {sorted_arr}")
            print(f"Time taken: {time_taken:.6f} seconds\n")
        print(f"Sorted:   {sorted_arr}")
        print(f"Time:     {time_taken:.6f} seconds\n")