import os


_HERE = os.path.abspath(os.path.dirname(__file__))


def get_fixture_abspath(filename: str) -> str:
    """Get the absolute path name for the given relative fixture file name.

    :param filename: The relative fixture file name
    :return: The absolute path for the fixture file.
    """
    return os.path.join(_HERE, 'fixtures', filename)
