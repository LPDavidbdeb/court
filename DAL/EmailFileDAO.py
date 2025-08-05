import os

class EmlFileDAO:
    """
    Data Access Object (DAO) for reading raw .eml file content from the local system.
    It does NOT parse the email content, only provides the raw bytes.
    """

    def __init__(self):
        pass

    def get_raw_eml_content(self, file_path: str) -> bytes | None:
        """
        Reads the raw content of an .eml file.

        Args:
            file_path (str): The full path to the .eml file on the local system.

        Returns:
            bytes: The raw byte content of the .eml file, or None if an error occurs.
        """
        if not os.path.exists(file_path):
            print(f"Error: EML file not found at {file_path}")
            return None
        if not os.path.isfile(file_path):
            print(f"Error: Path {file_path} is not a file.")
            return None

        try:
            with open(file_path, 'rb') as f:
                raw_content = f.read()
            print(f"Successfully read raw content from {file_path}")
            return raw_content
        except IOError as e:
            print(f"Error reading EML file {file_path}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while reading EML file {file_path}: {e}")
            return None

