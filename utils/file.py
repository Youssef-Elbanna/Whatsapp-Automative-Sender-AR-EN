def clean_file(file_path):
    """Clears the contents of the specified file."""
    with open(file_path, "w") as file:
        # Truncate file content
        pass


def read_file(file_path, array=False, encoding='utf-8'):
    """Reads the content of the specified file with UTF-8 encoding by default.

    Args:
        file_path (str): The path to the file.
        array (bool): If True, returns a list of lines. If False, returns the full content as a string.
        encoding (str): The encoding used to read the file (default is UTF-8).

    Returns:
        list or str: File content as a list of lines or a single string.
    """
    with open(file_path, "r", encoding=encoding) as file:
        if array:
            # Return content as a list of lines
            return [line.strip() for line in file.readlines()]
        else:
            # Return full content as a single string
            return file.read().strip()



def write_file(file_path, message):
    """Appends a message to the specified file.

    Args:
        file_path (str): The path to the file.
        message (str): The message to write.

    Returns:
        str: A success message.
    """
    with open(file_path, "a") as file:
        file.write(f"{message}\n")

    return "Success"
