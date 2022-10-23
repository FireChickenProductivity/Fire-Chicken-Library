from ..fire_chicken.internal_unit_testing import *
from talon import Module, actions
from ..fire_chicken.path_utilities import *


class FailureTestCaseTest(TestCase):
    def this_should_fail_properly(self):
        raise TestActualNotExpectedException('no actual value', 'failed without crashing')
        
    def this_will_crash(self):
        raise ValueError('crash')

    def failed_version_of_two_plus_two_equals_four(self):
        assert_actual_equals_expected(2+1, 4)

    def true_is_true(self):
        assert_true(True)

    def _this_method_should_not_get_tested(self):
        self.this_will_crash()


def test_and_verify(test_case,name="",dir=""):

    test_name = name
    if test_name == "": test_name = str(min(TestSuite.available_default_instance_list))
    test_suite = TestSuite(name,directory=dir,display_results=False, notify=False)
    verify_testname(test_case,test_name,test_suite.name)
    remove_old_output_file_if_exists(dir, test_name)
    test_suite.insert(FailureTestCaseTest)
    test_suite.run_tests()
    verify_output_file(test_case,dir, test_name)

def remove_old_output_file_if_exists(dir, test_name):
    output_file = get_output_file(dir,test_name)
    if os.path.isfile(output_file): os.remove(output_file)

def verify_testname(test_case,expected_name,actual_name):
    assert expected_name == actual_name, "Error in assigning Test Name for test case " + test_case + " expected " + expected_name + " instead was " + actual_name

def verify_output_file(test_case, dir, test_name):
    output_file = get_output_file(dir,test_name)
    test_file = get_test_output_file() 
    assert_files_have_matching_text_(test_case, output_file, test_file, maximum_file_size = 50000000)

def get_output_file(dir,test_name):
    if dir == "":
        directory_of_this_python_file = compute_file_directory(__file__)
        parent_directory_of_this_python_file = os.path.dirname(directory_of_this_python_file)
        fire_chicken_directory = join_path(parent_directory_of_this_python_file, "fire_chicken")
        data_directory= join_path(fire_chicken_directory, "data")
        dir = join_path(data_directory, "test_output") 
    return join_path(dir, test_name + ".txt")
    
def get_test_output_file():
    python_file_directory = compute_file_directory(__file__)
    return join_path(python_file_directory, "testing_internal_unit_testing_test_output_file" + ".txt")

def assert_files_have_matching_text_(testname,path1, path2, maximum_file_size = 50000000):
    path1_text = get_file_text(path1, maximum_file_size)
    assert_file_contains_expected_text(testname,path2, path1_text, maximum_file_size)

def assert_file_contains_expected_text(testname,path, expected_text, maximum_file_size = 50000000):
    actual_text = get_file_text(path, maximum_file_size)
    assert(actual_text == expected_text), "for testcase " + testname + " file content does not have expected value"

def get_file_text(path, maximum_file_size = 50000000):
    if os.path.getsize(path) > maximum_file_size:
        raise ValueError(f'The file at {path} exceeded the maximum number of bites of {maximum_file_size}!')
    text = ''
    with open(path, 'r') as file:
        text = file.read(maximum_file_size)
    return text

python_file_directory = compute_file_directory(__file__)
data_directory= join_path(python_file_directory, "data")
dir = join_path(data_directory, "test-internal-unit-test")

test_and_verify("test_default_dir_with_name","test_default_dir_with_name")
test_and_verify("test_with_dir_with_name","test_with_dir_with_name",dir)
test_and_verify("test_default_dir_with_default_name")
test_and_verify("test_with_dir_with_default_name","",dir)
