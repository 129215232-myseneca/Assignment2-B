#!/usr/bin/env python3
"""
DU Improved -- See Disk Usage Report with bar charts

Author: [Your Name]
Date: [Date]
Seneca ID: [Your Seneca ID]

Authorship Declaration:
I declare that this is my original work and follows academic integrity guidelines.

"""

import subprocess
import argparse


def call_du_sub(target_directory):
    """
    Runs the 'du -d 1' command for the specified directory and returns the output as a list.
    Each element in the list corresponds to one line of the 'du' command output.
    """
    try:
        process = subprocess.Popen(
            ['du', '-d', '1', target_directory],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(f"Error: {stderr.strip()}")
        return stdout.strip().split('\n')
    except Exception as e:
        print(f"Error running du: {e}")
        return []


def percent_to_graph(percent, total_chars):
    """
    Converts a percentage into a bar graph string of specified length.
    Example: percent_to_graph(50, 10) -> '=====     '
    """
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    filled_chars = round((percent / 100) * total_chars)
    return '=' * filled_chars + ' ' * (total_chars - filled_chars)


def create_dir_dict(du_list):
    """
    Converts a list of 'du' command output into a dictionary.
    Keys are directory paths, values are sizes in bytes (as integers).
    """
    dir_dict = {}
    for line in du_list:
        size, directory = line.split('\t', 1)
        dir_dict[directory.strip()] = int(size)
    return dir_dict


def human_readable_size(size_in_bytes):
    """
    Converts size in bytes to a human-readable format (e.g., 1K, 23M, 2G).
    """
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} T"


def parse_command_args():
    """
    Parses command-line arguments using argparse.
    Returns an object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts")
    parser.add_argument('target', nargs='?', default='.', help='The directory to scan.')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Print sizes in human-readable format (e.g., 1K 23M 2G).')
    parser.add_argument('-l', '--length', type=int, default=20, help='Specify the length of the graph. Default is 20.')
    return parser.parse_args()


def main():
    """
    Main function to execute the DU Improved script.
    """
    # Parse command-line arguments
    args = parse_command_args()
    target_directory = args.target
    bar_length = args.length
    human_readable = args.human_readable

    # Get the output from 'du' command and create a dictionary
    du_list = call_du_sub(target_directory)
    if not du_list:
        print(f"Error: Could not read directory '{target_directory}'.")
        return
    dir_dict = create_dir_dict(du_list)

    # Calculate the total size and percentages
    total_size = sum(dir_dict.values())
    if human_readable:
        total_size_str = human_readable_size(total_size)
    else:
        total_size_str = f"{total_size} B"

    # Generate and print the output
    print(f"Disk Usage for {target_directory} (Total: {total_size_str})")
    for directory, size in dir_dict.items():
        percent = (size / total_size) * 100
        bar_graph = percent_to_graph(percent, bar_length)
        size_str = human_readable_size(size) if human_readable else f"{size} B"
        print(f"{percent:5.1f}% [{bar_graph}] {size_str:10} {directory}")


if __name__ == "__main__":
    main()
