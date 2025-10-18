import pytest
from ldumpj.ldumpj import grammar, fixup
from ldumpj.model import LauchctlService

problem_cases = dict(
    zip(
        [
            "test/problem1",
            "test/problem2",
            "test/problem3"
        ],
        [
            "Malformed key=value for entry `panic on consecutive crashes (0)`"
            "Non int jetsam memory limits `(unlimited)"
            "Empty value for `PRODUCT_INFO_FILTER_DISABLE =>`"
        ]
    )
)

test_cases = dict(
    zip(
        [
            "test/ipadOS18.txt",
            "test/macOS15-5.v1.txt",
            "test/macOS15-5.v2.txt",
            "test/macos26.txt"
        ],
        [
            "ipadOS18",
            "macOS15-5.v1",
            "macOS15-5.v2",
            "macos26"
        ]
    )
)


@pytest.mark.parametrize("problem_case",problem_cases.items())
def test_problem_files(problem_case):
    problem_file = problem_case[0]
    problem_desc = problem_case[1]
    with open(problem_file, "r") as f:
        data = f.read()
    
    data = fixup(data)
    parsed_data = grammar.parse("{" + data + "}")
    
    try:
        for service_name, service_json in parsed_data.items():
            LauchctlService(**service_json)
    except:
        assert False, f"Error for {service_name} in test case {problem_desc}"

@pytest.mark.parametrize("test_case",test_cases.items())
def test_test_files(test_case):
    problem_file = test_case[0]
    problem_desc = test_case[1]
    with open(problem_file, "r") as f:
        data = f.read()
    
    try:
        data = fixup(data)
        parsed_data = grammar.parse("{" + data + "}")
    except:
        assert False, f"Parsing error in test case {problem_desc}"

@pytest.mark.parametrize("test_case",test_cases.items())
def model_test_files(test_case):
    problem_file = test_case[0]
    problem_desc = test_case[1]
    with open(problem_file, "r") as f:
        data = f.read()
    
    data = fixup(data)
    parsed_data = grammar.parse("{" + data + "}")
    
    try:
        for service_name, service_json in parsed_data.items():
            LauchctlService(**service_json)
    except:
        assert False, f"Error for {service_name} in test case {problem_desc}"