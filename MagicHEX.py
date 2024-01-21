import sys
import os

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def print_hex_header(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(8)  # Reading the first 8 bytes

        # Convert bytes to hexadecimal
        hex_header = ' '.join([hex(byte)[2:].zfill(2).upper() for byte in header])
        print(f"Hexadecimal representation of the file header: {hex_header}")
    except IOError:
        print(f"{RED}Error: File not found.{RESET}")

def change_header(file_path, new_header_hex, new_extension):
    try:
        with open(file_path, 'rb') as file:
            original_content = file.read()

        new_header = bytes.fromhex(new_header_hex)
        modified_content = new_header + original_content[8:]  # Keep rest of the content intact

        new_file_path = f"{file_path[:-4]}_modified.{new_extension.lower()}"
        with open(new_file_path, 'wb') as new_file:
            new_file.write(modified_content)

        print(f"{GREEN}Header changed successfully. New file saved as '{new_file_path}'{RESET}")
    except IOError:
        print(f"{RED}Error: File not found.{RESET}")
    except ValueError:
        print(f"{RED}Invalid hexadecimal input.{RESET}")

def identify_file_type(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(8)  # Reading the first 8 bytes

        # Convert bytes to hexadecimal
        hex_header = ''.join([hex(byte)[2:].zfill(2).upper() for byte in header])

        # Define magic headers
        magic_headers = {
            'PNG': '89504E470D0A1A0A',
            'JPEG': 'FFD8FFE0',
            'PDF': '255044462D',
            'DOCX': '504B0304'
        }

        # Check against magic headers
        file_type = None
        for key, value in magic_headers.items():
            if hex_header.startswith(value):
                file_type = key
                break

        if file_type:
            print(f"{GREEN}The file '{file_path}' is a {file_type} file.{RESET}")
        else:
            print(f"{RED}File type of '{file_path}' is not recognized.{RESET}")
            print_hex_header(file_path)
    except IOError:
        print(f"{RED}Error: File not found.{RESET}")

def reverse_hex_and_check(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(8)  # Reading the first 8 bytes

        # Convert bytes to hexadecimal and reverse
        reversed_hex_header = ''.join([hex(byte)[2:].zfill(2).upper() for byte in header])[::-1]

        # Check if reversed hex satisfies to make the file valid
        file_path_temp = file_path + "_reversed_temp"
        with open(file_path_temp, 'wb') as file:
            file.write(bytes.fromhex(reversed_hex_header))
        print(f"{GREEN}Reversed hex saved as '{file_path_temp}'{RESET}")
    except IOError:
        print(f"{RED}Error creating temporary file.{RESET}")
    except ValueError:
        print(f"{RED}Invalid hexadecimal input.{RESET}")
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")

def change_all_headers(file_path):
    headers = {
        'JPEG': 'FFD8FFE0',
        'PNG': '89504E470D0A1A0A',
        'PDF': '255044462D',
        'DOCX': '504B0304'
    }
    try:
        with open(file_path, 'rb') as file:
            original_content = file.read()

        for header_type, header_value in headers.items():
            new_header = bytes.fromhex(header_value)
            modified_content = new_header + original_content[8:]  # Keep rest of the content intact

            new_file_path = f"{file_path[:-4]}_{header_type.lower()}.{header_type.lower()}"
            with open(new_file_path, 'wb') as new_file:
                new_file.write(modified_content)
            print(f"{GREEN}Header changed successfully for {header_type}. New file saved as '{new_file_path}'{RESET}")
    except IOError:
        print(f"{RED}Error: File not found.{RESET}")
    except ValueError:
        print(f"{RED}Invalid hexadecimal input.{RESET}")

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    print(f"{GREEN}'{file_path}' file is opened.{RESET}")
    while True:
        print("Options:")
        print("1. Check file type by direct header")
        print("2. Print hexadecimal representation of header")
        print("3. Header Operations (Change headers individually)")
        print("4. Reverse hex and check / Save reversed hex as copy")
        print("5. Save all headers as separate files")
        print("6. Quit")
        option = input("Choose an option (1-6): ")

        if option == '1':
            identify_file_type(file_path)
        elif option == '2':
            print_hex_header(file_path)
        elif option == '3':
            while True:
                print("Header Operations:")
                print("1. Change header to JPG")
                print("2. Change header to PNG")
                print("3. Change header to PDF")
                print("4. Change header to DOCX")
                print("5. Go back")
                sub_option = input("Choose an option (1-5): ")

                if sub_option in ['1', '2', '3', '4']:
                    new_headers = {
                        '1': ('FFD8FFE0', 'JPEG'),  # JPEG
                        '2': ('89504E470D0A1A0A', 'PNG'),  # PNG
                        '3': ('255044462D', 'PDF'),  # PDF
                        '4': ('504B0304', 'DOCX')  # DOCX
                    }
                    new_header_hex, new_extension = new_headers[sub_option]
                    change_header(file_path, new_header_hex, new_extension)
                elif sub_option == '5':
                    break
                else:
                    print(f"{RED}Invalid option selected.{RESET}")
        elif option == '4':
            reverse_hex_and_check(file_path)
        elif option == '5':
            change_all_headers(file_path)
        elif option == '6':
            break
        else:
            print(f"{RED}Invalid option selected.{RESET}")
else:
    print(f"{RED}Please provide a file path as an argument.{RESET}")
