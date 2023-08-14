import re

def extract_coordinates(text):
    # Define the regular expression pattern to match pairs of numbers
    pattern = r'(\d+\.\d+)\s+(\d+\.\d+)'

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Check if we found exactly 4 pairs of numbers
    if len(matches) != 4:
        raise ValueError("Expected 4 pairs of coordinates, but found {}.".format(len(matches)))

    # Convert the matched strings to pairs of floats
    coordinates = [(float(match[0]), float(match[1])) for match in matches]

    return coordinates

if __name__ == "__main__":
    # Your input text
    input_text = """
    EyBadov: 132.94 r.y.

    457102.01 4431080.27



    Idi6rnra:
    AJA

    panicle icin







    457098.31 4431074.98

    | 457112.07 4431061.75
    457116.83 4431067.30
    """

    try:
        coordinates = extract_coordinates(input_text)
        print("Extracted coordinates:")
        for coord in coordinates:
            print(coord)
    except ValueError as e:
        print("Error:", e)
