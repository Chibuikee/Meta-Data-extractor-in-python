import os


def log_saver(filename, file):

    # Create the output directory if it doesn't exist
    if not os.path.exists("./output"):
        os.makedirs("./output")

    # Create the full path for the output file
    output_filename = os.path.join("./output", f"{filename}.txt")

    # Write the file content
    with open(output_filename, "w") as f:
        f.write(file)

    print(f"Text extracted from {filename} and saved to {output_filename}")


# log_saver("chibs1", "I am just testing this stuff")
