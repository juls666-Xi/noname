import pandas as pd
import sys
import os

def text_to_excel(input_txt_path: str, output_xlsx_path: str, delimiter: str = None, header: bool = False):
    """
    Convert a text file to Excel (.xlsx).
    Guesses delimiter if not provided: tab, comma, semicolon, or space.
    """
    if not os.path.isfile(input_txt_path):
        raise FileNotFoundError(f"Input file not found: {input_txt_path}")

    # Auto-detect delimiter if not specified
    if delimiter is None:
        with open(input_txt_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if '\t' in first_line:
                delimiter = '\t'
            elif ',' in first_line:
                delimiter = ','
            elif ';' in first_line:
                delimiter = ';'
            elif ' ' in first_line:
                delimiter = ' '
            else:
                delimiter = None  # single column

    # Read text file
    if delimiter:
        df = pd.read_csv(input_txt_path, delimiter=delimiter, header=None if not header else 0, encoding='utf-8')
    else:
        # Single column
        df = pd.read_csv(input_txt_path, header=None, names=['Data'], encoding='utf-8')

    # Write to Excel
    df.to_excel(output_xlsx_path, index=False, engine='openpyxl')
    print(f"Converted {input_txt_path} to {output_xlsx_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python txt2excel.py <input.txt> <output.xlsx> [delimiter] [header]")
        print("  delimiter: optional, e.g. ',' ';' '\\t' ' '")
        print("  header: optional, 1 if first row is column names, else 0 (default)")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    delim = sys.argv[3] if len(sys.argv) > 3 else None
    hdr = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False

    try:
        text_to_excel(in_path, out_path, delimiter=delim, header=hdr)
    except Exception as e:
        print(f"Error: {e}")