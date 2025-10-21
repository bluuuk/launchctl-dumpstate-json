import pytest
from ldumpj.core import parse_launchctl_output
import glob
import os

# Get the absolute path of the current file
# and use it to construct the absolute path to the test directory
# This makes the test independent of the current working directory
basedir = os.path.dirname(os.path.abspath(__file__))
test_files = glob.glob(os.path.join(basedir, "*.txt"))
test_files.extend(glob.glob(os.path.join(basedir, "problem*")))

@pytest.mark.parametrize("test_file", test_files)
def test_parse_launchctl_output_with_all_test_cases_and_validate(test_file):
    with open(test_file, "r") as f:
        data = f.read()
    
    try:
        parse_launchctl_output(data,validate_model=True)
    except Exception as e:
        assert False, f"Parsing failed for {test_file} with error: {e}"
        
@pytest.mark.parametrize("test_file", test_files)
def test_parse_launchctl_output_with_all_test_cases(test_file):
    with open(test_file, "r") as f:
        data = f.read()
    
    try:
        parse_launchctl_output(data,validate_model=False)
    except Exception as e:
        assert False, f"Parsing failed for {test_file} with error: {e}"
