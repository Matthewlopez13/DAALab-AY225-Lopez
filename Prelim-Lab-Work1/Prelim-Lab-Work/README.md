# Bubble Sort Descending

A Python implementation of the bubble sort algorithm that sorts data in **descending order**.

## Description

This project demonstrates the bubble sort algorithm with an optimization flag to detect when the array is already sorted. The algorithm sorts numbers from a dataset file in descending order and measures the time taken.

## Features

- Sorts data in descending order
- Includes optimization to detect already-sorted arrays
- Measures and displays sorting performance
- Loads numbers from `dataset.txt`

## Requirements

- Python 3.x

## Usage

1. Ensure `dataset.txt` is in the same directory as `app.py`
2. Format `dataset.txt` with one number per line
3. Run the script:

```bash
python app.py
```

## Output

The script will display:
- Number of elements loaded
- First and last 10 numbers
- Sorted array in descending order
- Time taken to sort

## File Structure

```
.
├── app.py          # Main bubble sort implementation
├── dataset.txt     # Input data file (one number per line)
└── README.md       # This file
```

## Algorithm Explanation

Bubble sort works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they're in the wrong order. This continues until no more swaps are needed, indicating the list is sorted.

For **descending order**, elements are swapped if the left element is **less than** the right element.
