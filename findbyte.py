file_path = "C:\\Users\\JanRudolfGuiamoy\\Downloads\\ADDeltekdev_04152024 (1).csv"
position_to_find = 5665

# Function to count lines until a given position
def count_lines_until_position(file_path, position):
    line_count = 0
    with open(file_path, "rb") as file:
        for line in file:
            line_count += 1
            if file.tell() >= position:
                break
    return line_count

line_number = count_lines_until_position(file_path, position_to_find)
print("Line number:", line_number)
