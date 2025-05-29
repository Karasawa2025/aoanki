from google.protobuf.json_format import MessageToDict

from aoanki.meta import MetaVersion
from proto.anki import import_export_pb2


def from_apkg_bytes(apkg_bytes: bytes) -> MetaVersion:
    """
    Read an Anki package file and return the metadata.
    """
    import zipfile
    import io

    # Create a BytesIO object from the bytes
    with zipfile.ZipFile(io.BytesIO(apkg_bytes)) as zf:
        # Try to read metadata from the file
        try:
            with zf.open("meta") as meta_file:
                meta_bytes = meta_file.read()
                return from_meta_bytes(meta_bytes)
        except zipfile.BadZipfile:
            raise ValueError("Invalid zip file.")
        except KeyError:
            # If the meta file is not found, try to read the collection file
            pass
        # Can't found meta
        # Try find collection.anki21
        try:
            with zf.open("collection.anki21") as collection_file:
                return MetaVersion.LEGACY2
        except KeyError:
                return MetaVersion.LEGACY1
    return MetaVersion.UNKNOWN

def from_apkg_file(apkg_file: str) -> MetaVersion:
    """
    Read an Anki package file and return the metadata.
    """
    with open(apkg_file, "rb") as f:
        apkg_bytes = f.read()
        return from_apkg_bytes(apkg_bytes)

def from_meta_bytes(meta_bytes: bytes) -> MetaVersion:
    """
    Read an Anki package file and return the metadata.
    """
    meta_data = import_export_pb2.PackageMetadata()
    meta_data.ParseFromString(meta_bytes)
    # Convert protobuf to dictionary for easier handling
    meta_dict = MessageToDict(meta_data)
    # Get version
    version = meta_dict.get('version', None)
    meta_version = MetaVersion(version)
    return meta_version

def from_meta_file(meta_file: str) -> MetaVersion:
    """
    Read an Anki package file and return the metadata.
    """
    with open(meta_file, "rb") as f:
        meta_bytes = f.read()
        return from_meta_bytes(meta_bytes)