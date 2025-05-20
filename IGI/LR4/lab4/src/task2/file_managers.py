import os
import zipfile


class FileManager(object):
    """Provides methods to handle file operations such as loading and saving data."""

    @staticmethod
    def load(filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save(data, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)


class ZipManager(object):
    """Handles operations related to ZIP archive files."""

    @staticmethod
    def save(filename: str, archive_name: str):
        """
        Save a specified file into a ZIP archive.

        :param filename: The name of the file to be saved into the archive.
        :param archive_name: The name of the ZIP archive where the file will be stored.
        """

        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(filename, arcname=os.path.basename(filename))

    @staticmethod
    def load(archive_name: str, filename: str):
        """
        Load a file's content from a given ZIP archive and decode it as a UTF-8 string.
        This method reads the archived file without extracting it.

        :param archive_name: The name of the ZIP archive file to read from.
        :param filename: The name of the file within the ZIP archive whose content is to be read.

        :return: The UTF-8 decoded content of the specified file.
        """

        with zipfile.ZipFile(archive_name, 'r', zipfile.ZIP_DEFLATED) as zf:
            return zf.read(filename).decode('utf-8')

    @staticmethod
    def file_info(archive_name: str, filename: str):
        """
        Retrieves information about a specific file within a ZIP archive.

        :param archive_name: The name of the ZIP archive file to be opened.
        :param filename: The name of the file within the ZIP archive whose information is desired.

        :return: zipfile.ZipInfo. An object containing metadata about the specified file in the ZIP
                archive, such as file size, modification time, and other details.
        """

        with zipfile.ZipFile(archive_name, 'r', zipfile.ZIP_DEFLATED) as zf:
            return zf.getinfo(filename)
