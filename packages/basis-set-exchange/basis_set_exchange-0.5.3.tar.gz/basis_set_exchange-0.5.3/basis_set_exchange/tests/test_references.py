"""
Tests for reference handling
"""

import glob
import json
import os

import pytest
from basis_set_exchange import api, refconverters, misc, fileio

_data_dir = api._default_data_dir

# _all_files shouldn't contain .table. files
_all_files = glob.glob(os.path.join(_data_dir, '*', '*.json'))
_all_component_files = fileio.get_all_filelist(_data_dir)[2]


@pytest.mark.parametrize("elements, expected", 
                         [ ([1], "H"),
                           ([1,2], "H,He"),
                           ([1,10], "H,Ne"),
                           ([1,2,3,11,23,24], "H-Li,Na,V,Cr")])
def test_compact_string(elements, expected):
    assert misc.compact_elements(elements) == expected


@pytest.mark.parametrize('file_path', _all_component_files)
def test_filenames(file_path):
    full_path = os.path.join(_data_dir, file_path)
    with open(full_path, 'r') as f:
        file_refs = json.load(f)['basis_set_references'] 
        if len(file_refs) > 0:
            ref_str = '_'.join(file_refs)
        else:
            ref_str = 'noref'
        ref_str = '_' + ref_str

        # Strip off '.0.json', '.1.json', etc
        base_name = os.path.splitext(file_path)[0]
        base_name = os.path.splitext(base_name)[0]

        # Base name should end with the reference string
        print(base_name)
        print(ref_str)
        assert base_name.endswith(ref_str)
