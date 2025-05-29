import pytest
import os
from proto.anki import import_export_pb2
from google.protobuf.json_format import MessageToDict

current_dir = os.path.dirname(__file__)
file_path_legacy_2 = os.path.join(current_dir, "meta_VERSION_LEGACY_2")
file_path_latest = os.path.join(current_dir, "meta_VERSION_LATEST")

def test_meta_version_VERSION_LEGACY_2():
    """
    This function tests whether the 'meta_VERSION_LEGACY_2' file exists and verifies its version number or contents using protobuf.
    """
    # Ensure the meta_VERSION_LEGACY_2 file exists
    assert os.path.exists(file_path_legacy_2), f"'meta_VERSION_LEGACY_2' file not found at {file_path_legacy_2}"

    with open(file_path_legacy_2, "rb") as meta_file:
        # Assuming the meta_VERSION_LEGACY_2 file contains protobuf data that can be parsed with `import_export_pb2`
        meta_data = import_export_pb2.PackageMetadata()
        meta_data.ParseFromString(meta_file.read())

        # Convert protobuf to dictionary for easier handling
        meta_dict = MessageToDict(meta_data)


        # Perform checks (adjust these according to your versioning needs)
        assert 'version' in meta_dict, "Meta file does not contain a 'version' field"
        # Get version from protobuf
        version = meta_dict.get('version', None)
        # Check if version is'VERSION_LEGACY_2'
        assert version == 'VERSION_LEGACY_2', f"Expected version 'VERSION_LEGACY_2', but got '{version}'"
    print("Meta VERSION_LEGACY_2 test passed!")

def test_meta_version_VERSION_LATEST():
    """
    This function tests whether the 'meta_VERSION_LATEST' file exists and verifies its version number or contents using protobuf.
    """
    # Ensure the meta_VERSION_LATEST file exists
    assert os.path.exists(file_path_latest), f"'meta_VERSION_LATEST' file not found at {file_path_latest}"

    with open(file_path_latest, "rb") as meta_file:
        # Assuming the meta_VERSION_LATEST file contains protobuf data that can be parsed with `import_export_pb2`
        meta_data = import_export_pb2.PackageMetadata()
        meta_data.ParseFromString(meta_file.read())

        # Convert protobuf to dictionary for easier handling
        meta_dict = MessageToDict(meta_data)

        # Perform checks (adjust these according to your versioning needs)
        assert 'version' in meta_dict, "Meta file does not contain a 'version' field"
        # Get version from protobuf
        version = meta_dict.get('version', None)
        # Check if version is 'VERSION_LEGACY_1'
        assert version == 'VERSION_LATEST', f"Expected version 'VERSION_LATEST', but got '{version}'"
    print("Meta VERSION_LATEST test passed!")
