import random
import time
import sys

# Increase recursion depth because Deterministic Quicksort will hit 
# maximum recursion depth on already sorted/reverse-sorted arrays of larger sizes.
sys.setrecursionlimit(20000)

# ==========================================
# 1. QUICKSORT IMPLEMENTATIONS
# ==========================================

def partition_3way(arr, low, high):
    """
    Partitions the array into three segments:
    < pivot, == pivot, and > pivot.
    This efficiently handles arrays with many repeated elements.
    """
    pivot = arr[low]
    lt = low       # elements < pivot
    gt = high      # elements > pivot
    i = low + 1    # current element
    
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1
            
    return lt, gt

def _randomized_quicksort(arr, low, high):
    if low < high:
        # Choose pivot uniformly at random from the subarray
        pivot_idx = random.randint(low, high)
        # Swap random pivot with the first element
        arr[low], arr[pivot_idx] = arr[pivot_idx], arr[low]
        
        # Partition
        m1, m2 = partition_3way(arr, low, high)
        
        # Recursive calls
        _randomized_quicksort(arr, low, m1 - 1)
        _randomized_quicksort(arr, m2 + 1, high)

def randomized_quicksort(arr):
    """Sorts an array using Randomized Quicksort."""
    if not arr: # Handle empty array edge case
        return arr
    _randomized_quicksort(arr, 0, len(arr) - 1)


def _deterministic_quicksort(arr, low, high):
    if low < high:
        # Pivot is ALWAYS the first element
        m1, m2 = partition_3way(arr, low, high)
        
        # Recursive calls
        _deterministic_quicksort(arr, low, m1 - 1)
        _deterministic_quicksort(arr, m2 + 1, high)

def deterministic_quicksort(arr):
    """Sorts an array using Deterministic Quicksort (first element as pivot)."""
    if not arr: # Handle empty array edge case
        return arr
    _deterministic_quicksort(arr, 0, len(arr) - 1)


# ==========================================
# 2. EMPIRICAL COMPARISON FRAMEWORK
# ==========================================

def generate_test_arrays(size):
    """Generates the four required distribution types for a given size."""
    # 1. Randomly generated arrays
    random_arr = [random.randint(0, 10000) for _ in range(size)]
    
    # 2. Already sorted arrays
    sorted_arr = list(range(size))
    
    # 3. Reverse-sorted arrays
    reverse_sorted_arr = list(range(size, 0, -1))
    
    # 4. Arrays with repeated elements (mostly 3s, with a few others)
    repeated_arr = [random.choice([3, 3, 3, 3, 3, 1, 5, 7, 3]) for _ in range(size)]
    
    return {
        "Random": random_arr,
        "Sorted": sorted_arr,
        "Reverse-Sorted": reverse_sorted_arr,
        "Repeated Elements": repeated_arr
    }

def measure_time(sort_function, arr):
    """Measures the execution time of a sorting function on a copy of the array."""
    arr_copy = arr.copy() # Sort a copy to keep the original intact for the next algorithm
    start_time = time.perf_counter()
    sort_function(arr_copy)
    end_time = time.perf_counter()
    return end_time - start_time

def run_empirical_comparison():
    """Runs tests across different input sizes and distributions."""
    sizes = [1000, 5000, 10000] # Adjust sizes based on your machine's capabilities
    
    print(f"{'Array Type':<20} | {'Size':<8} | {'Randomized QS (s)':<20} | {'Deterministic QS (s)':<20}")
    print("-" * 75)
    
    for size in sizes:
        datasets = generate_test_arrays(size)
        
        for name, data in datasets.items():
            # Time Randomized
            rand_time = measure_time(randomized_quicksort, data)
            
            # Time Deterministic
            # Note: For very large sorted/reverse-sorted arrays, Deterministic QS 
            # might hit maximum recursion depth limits even with sys.setrecursionlimit.
            try:
                det_time = measure_time(deterministic_quicksort, data)
            except RecursionError:
                det_time = "RecursionError"
                
            if isinstance(det_time, float):
                print(f"{name:<20} | {size:<8} | {rand_time:<20.6f} | {det_time:<20.6f}")
            else:
                print(f"{name:<20} | {size:<8} | {rand_time:<20.6f} | {det_time:<20}")
        print("-" * 75)

if __name__ == "__main__":
    run_empirical_comparison()