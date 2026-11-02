import os
import sys

def split_text(input_file):
    output_dir = os.getcwd()

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        output_file = os.path.join(output_dir, f'line_{i + 1}.txt')
        with open(output_file, 'w') as out_file:
            out_file.write(line.strip())
        
        print(f"Line {i + 1} saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_text.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    split_text(input_file)

