# version : latest legacy1 legacy2
from aoanki.database.legacy1 import Database as Legacy1Database
from aoanki.database.legacy2 import Database as Legacy2Database
from aoanki.database.latest import Database as LatestDatabase

from aoanki.meta import MetaVersion

from pathlib import Path
import platform
import tempfile

from aoanki.meta.reader import from_apkg_file

TEMPDIR = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())

import zipfile

def get_database(dectpath):
    """
    Returns the appropriate database class based on the version.

    :param version: The version of the database.
    :param dectpath: The path to the Anki deck directory.
    :return: An instance of the appropriate Database class.
    """
    # get random temp dir for unzipping
    import random
    import string
    import os
    temp_dir = os.path.join(TEMPDIR, ''.join(random.choices(string.ascii_letters + string.digits, k=10)))
    #unzip in temp dir
    meta_version = from_apkg_file(dectpath)
    with zipfile.ZipFile(dectpath, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    if meta_version == MetaVersion.LEGACY1:
        return Legacy1Database(temp_dir)
    elif meta_version == MetaVersion.LEGACY2:
        return Legacy2Database(temp_dir)
    elif meta_version == MetaVersion.LATEST:
        return LatestDatabase(temp_dir)