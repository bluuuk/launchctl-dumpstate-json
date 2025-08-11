import pytest
from ldumpj.ldumpj import grammar, fixup
from ldumpj.model import LauchctlService

test_cases = dict(
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


@pytest.mark.parametrize("problem_case",test_cases.items())
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
        assert True == False, problem_desc
