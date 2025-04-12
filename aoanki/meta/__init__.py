# meta version
from enum import Enum


class MetaVersion(Enum):
    LEGACY1 = "VERSION_LEGACY_1"
    LEGACY2 = "VERSION_LEGACY_2"
    LATEST = "VERSION_LATEST"
    UNKNOWN = "UNKNOWN"
    # get collection filename
    @staticmethod
    def get_collection_filename(version):
        if version == MetaVersion.LEGACY1:
            return "collection.anki2"
        elif version == MetaVersion.LEGACY2:
            return "collection.anki21"
        elif version == MetaVersion.LATEST:
            return "collection.anki21b"
        else:
            raise ValueError(f"Unknown version: {version}")