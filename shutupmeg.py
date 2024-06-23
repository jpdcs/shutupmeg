def extract_files(megmid):
    with open(megmid, 'rb') as file:
        data = file.read()

    file_start_pattern1 = b'\xF2\x0D\xC9\x48\x61\x60\x60\x60\x63'
    file_start_pattern2 = b'\xF3\x0D\xC9\x48\x61\x60\x60\x60\x63'

    file_start_index = 0
    file_number = 1

    print("MEGMID BINARY EXTRACTION TOOL. WARNING: This script will extract files. Do you want to proceed? Type Y and hit ENTER to continue extract or type N and hit ENTER to cancel and exit. (y/n)")
    user_input = input().lower()

    if user_input != 'y':
        print("Extraction canceled.")
        return

    while file_start_index < len(data):
        start_offset1 = data.find(file_start_pattern1, file_start_index)
        start_offset2 = data.find(file_start_pattern2, file_start_index)

        if start_offset1 == -1 and start_offset2 == -1:
            break

        if start_offset1 == -1 or (start_offset2 != -1 and start_offset2 < start_offset1):
            start_offset = start_offset2
        else:
            start_offset = start_offset1

        next_start_offset1 = data.find(file_start_pattern1, start_offset + 1)
        next_start_offset2 = data.find(file_start_pattern2, start_offset + 1)

        next_start_offset = min(offset for offset in [next_start_offset1, next_start_offset2] if offset != -1)

        end_offset = next_start_offset if next_start_offset != -1 else len(data)

        file_content = data[start_offset:end_offset]
        # Constructing the file name with hexadecimal offset
        hex_offset = hex(start_offset)[2:].zfill(8)  # Convert to hex and format to 8 characters
        with open(f"{file_number}_{hex_offset}.pop", 'wb') as output_file:
            output_file.write(file_content)

        file_start_index = end_offset
        file_number += 1

    print(f"{file_number - 1} files extracted successfully.")

# Usage example
archive_path = 'megmid'  # Replace with your actual archive file path
extract_files(archive_path)