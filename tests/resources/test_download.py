import pytest
from elfen.resources import (
    RESOURCE_MAP,
    download_lexicon,
)
import requests

def test_resource_downloads(tmp_path):
    """
    Test the resource downloads.
    """
    for resource in RESOURCE_MAP.keys():
        if "nrc" not in resource:
            tmp_file_path = tmp_path / RESOURCE_MAP[resource]['filename']
            link = RESOURCE_MAP[resource]['link']
            download_lexicon(link,
                            tmp_path,
                            filename=RESOURCE_MAP[resource]['filename'])
            
            # Check if the file exists
            assert tmp_file_path.exists(), f"Resource {resource} not downloaded."
            # Check if the file is not empty
            assert tmp_file_path.stat().st_size > 0, f"Resource {resource} is empty."

