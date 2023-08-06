## Test Junkie [pre-release]

Test Junkie is a classy framework for executing test scenarios.

_This is a pre-release version, documentation may be incomplete and functionality of features is subject to change._

## Table of  content

* [Installation](#installation)
* [Features](#features)
  * [Decorators](#decorators)
    * [@Suite](#suite)
    * [@beforeClass](#beforeclass)
    * [@beforeTest](#beforetest)
    * [@test](#test)
    * [@afterTest](#aftertest)
    * [@afterClass](#afterclass)
  * [Skipping Tests/Suites](#skipping-testssuites)
  * [Retrying Tests/Suites](#retrying-testssuites)
  * [Parameterized Tests](#parameterized-tests)
  * [Test Listeners](#test-listeners)
    * [On Success](#on-success)
    * [On Fail](#on-fail)
    * [On Error](#on-error)
    * [On Ignore](#on-ignore)
    * [On Skip](#on-skip)
    * [On Class Skip](#on-class-skip)
    * [On Before Class Fail](#on-before-class-failure)
    * [On Before Class Error](#on-before-class-error)
    * [On After Class Fail](#on-after-class-failure)
    * [On After Class Error](#on-after-class-error)
    * [Meta](#meta)
  * [Tags]()
* [Examples](#examples)
  * [Test Suite](#test-suite)
  * [Running Test Suite(s)](#executing-test-suites)
    * [Using Runner with Tags](#executing-with-tags)

## Installation
`pip install test_junkie`
##
## Features
### Decorators
#### @Suite
Test Junkie enforces suite based test architecture. Thus all tests must be defined within a class and 
that class must be decorated with @Suite. See example on [Creating Test Suites(s)](). 
```python
from test_junkie.decorators import Suite

@Suite()
class LoginFunctionality:
    ...
```
@Suite decorator supports [Meta](#meta), [Retry](#retrying-testssuites), [Skip](#skipping-testssuites), 
and [Listeners](#test-listeners).

Meta can be passed via `@Suite(meta=...)`, see [Meta](#meta) for more info and examples.

#### @beforeClass
This decorator will prioritize execution of a decorated function at the very beginning of a test suite.
Decorated function will be executed only once at the very beginning of the test suite. Code which produces exception in 
the decorated function will be treated as a class failure which will mark all of the tests in the suite as ignored. 
[On Ignore](#on-ignore) event listener will be called for each of the tests.
```python
from test_junkie.decorators import beforeClass

...
@beforeClass()
def a_function():
    ...
```
@beforeClass decorator does not support any special arguments at this time.

#### @beforeTest
This decorator will prioritize execution of a decorated function before every test case in the suite.
Decorated function will be executed once before every test case in the suite. Code which produces exception in the
decorated function will be treated as a test failure/error and respective [On Error](#on-error) or 
[On Fail](#on-fail) event listener will be called.
```python
from test_junkie.decorators import beforeTest

...
@beforeTest()
def b_function():
    ...
```
@beforeTest decorator does not support any special arguments at this time.

#### @test
Test Junkie enforces suite based test architecture. Thus all tests must be defined within a class and be decorated 
with @test. See example on [Creating Test Suites(s)](). Code which produces exception in the
decorated function will be treated as a test failure/error and respective [On Error](#on-error) or 
[On Fail](#on-fail) event listener will be called. Function decorated with [@afterTest](#aftertest) will not be 
executed if exception is raised in a test case. [On Success](#on-success) event listener will be called if test passes.
```python
from test_junkie.decorators import test

...

@test()
def a_test():
    ...

@test()
def b_test():
    ...
```
@test decorator supports [Meta](#meta), [Retry](#retrying-testssuites), [Skip](#skipping-testssuites), 
and [Parameters](#parameterized-tests)

Meta can be passed via `@test(meta=...)`, see [Meta](#meta) for more info and examples.

#### @afterTest
This decorator will de-prioritize execution of a decorated function for the end of each test case in the suite.
Decorated function will be executed once after every test cases in the suite. Code which produces exception in the
decorated function will be treated as a test failure/error and respective [On Error](#on-error) or 
[On Fail](#on-fail) event listener will be called.
```python
from test_junkie.decorators import afterTest

...
@afterTest()
def c_function():
    ...
```
@afterTest decorator does not support any special arguments at this time.

#### @afterClass
This decorator will de-prioritize execution of a decorated function for the very end of a test suite.
Decorated function will be executed only once at the very end of the test suite.
```python
from test_junkie.decorators import afterClass

...
@afterClass()
def d_function():
    ...
```
@afterClass decorator does not support any special arguments at this time.

### Skipping Tests/Suites
Test Junkie extends skipping functionality at the test level and at the suite level. You can use both at the same time 
or individually.
```python
from test_junkie.decorators import Suite, test

@Suite()
class ExampleSuite:

    @test(skip=True)
    def a_test(self):
    
        assert True is False
```
+ Test level skip takes a boolean value, if True - test will be skipped and [On Skip](#on-skip) event listener will be 
called. Execution of tests will continue as usual if there are any remaining tests in the suite.
+ Test level skip can also take a function as `my_function` or `my_function()` in the earlier, it will 
evaluate the function when appropriate.
    + If your function has `meta` argument in the signature, Test Junkie will pass all of the test function's 
    [Meta](#meta) information to it. All of this support is there in order to ensure that you have maximum flexibility 
    to build business logic for skipping tests.
    + Function must return `boolean` value when evaluation completes.

```python
from test_junkie.decorators import Suite, test

@Suite(skip=True)
class ExampleSuite:

    @test()
    def a_test(self):
    
        assert True is False
```
+ Suite level skip takes a boolean value, if True - all of the decorated functions in the suite will be skipped. 
[On Skip](#on-skip) event listener will NOT be called, instead [On Class Skip](#on-class-skip) will fire.

### Retrying Tests/Suites
Test Junkie extends retry functionality at the test level and at the suite level. You can use both at the same time 
or individually. Code bellow uses both, test and suite, level retries.
```python
from test_junkie.decorators import Suite, test

@Suite(retry=2)
class ExampleSuite:

    @test(retry=2)
    def a_test(self):
    
        assert True is False
```
+ Test level retry will retry the test, until test passes or retry limit is reached, immediately after the failure. 
+ Suite level retry will kick in after all of the tests in the suite have been executed and there is at least one 
unsuccessful test. Test level retries will be honored again during the suite retry. 
Only unsuccessful tests will be retried.

With that said, the above test case will be retried 4 times in total.

### Parameterized Tests
Test Junkie allows you to run parameterized test scenarios out of the box and it allows all data types to be 
used as parameters.
```python
from test_junkie.decorators import Suite, test

@Suite()
class ExampleSuite:

    @test(parameters=[{"fruit": "apple"}, None, "blue", [1, 2, 3]])
    def a_test(self, parameter):
    
        assert isinstance(parameter, dict), "Expected dict. Actual data type: {actual}".format(actual=type(parameter)) 
```
+ Any time parameterized test is defined, the decorated function must accept `parameter` in the function signature.
+ If parameterized test fails and [retry](#retrying-testssuites) is used, only the parameter(s) that test failed 
with will be [retried](#retrying-testssuites).

### Test Listeners
Test Junkie allows you to define test listeners which allow to execute your own code on a specific test event. 
Defining listeners is optional. This feature is typically useful when building large frameworks as it allows for 
seamless integration for reporting, post processing of errors, calculation of test metrics, alerts, 
artifact collection etc.

Listeners that you want to use are defined at the suite level and are supported by the [@Suite](#suite) decorator. 
This allows flexibility to support different types of tests without having to add complexity every time 
you need to support a new type of test.

In order to create a test listener you need to create a new class and inherit from `TestListener`. 
After that, you can overwrite functions that you wish to support. Following functions can be overwritten: 
[On Success](#on-success), [On Fail](#on-fail), [On Error](#on-error), [On Ignore](#on-ignore), 
[On Skip](#on-skip), [On Before Class Failure](#on-before-class-failure), 
[On Before Class Error](#on-before-class-error), [On After Class Failure](#on-after-class-failure), 
[On After Class Error](#on-after-class-error), and [On Class Skip](#on-class-skip).
```python
from test_junkie.testlistener import TestListener

class MyTestListener(TestListener):

    def __init__(self, **kwargs):

        TestListener.__init__(self, **kwargs)
    ...
```
#### On Success
On success event is triggered after test has successfully executed, that means [@beforeTest](#beforetest) (if any), 
[@test](#test), and [@afterTest](#aftertest) (if any) decorated functions have ran without producing an exception.
```python
...
    def on_success(self):
        # Write your own code here
        pass 
    ...
```

#### On Fail
On failure event is triggered after test has produced `AssertionError`. `AssertionError` must be unhandled and  
thrown during the code execution in functions decorated with [@beforeTest](#beforetest) (if any), [@test](#test), 
or [@afterTest](#aftertest) (if any). Make sure to include `exception` argument in the method signature, Exception 
object will be accessible through this argument.
```python
...
    def on_failure(self, exception):
        # Write your own code here
        pass 
    ...
```

#### On Error
On error event is triggered after test has produced any exception other than `AssertionError`. Exception must be 
unhandled and thrown during the code execution in functions decorated with [@beforeTest](#beforetest) (if any), 
[@test](#test), or [@afterTest](#aftertest) (if any). Make sure to include `exception` argument in the method signature, 
Exception object will be accessible through this argument.
```python
...
    def on_error(self, exception):
        # Write your own code here
        pass 
    ...
```

#### On Ignore
On ignore event is triggered when a function decorated with [@beforeClass](#beforeclass) 
produces an exception. In this unfortunate event, all of the tests under that particular test suite will be marked as 
ignored. Make sure to include `exception` argument in the method signature, Exception object will be accessible 
through this argument. 

On ignore event can also be triggered by incorrect arguments being passed in to the [@test](#test) decorator.
```python
...
    def on_ignore(self, exception):
        # Write your own code here
        pass 
    ...
```

#### On Skip
On skip event is triggered, well, when tests are skipped. Skip is supported by [@test](#test) & [@Suite](#suite) 
function decorators. See [Skipping Tests/Suites](#skipping-testssuites) for examples. 
Skip event can also be triggered when [Using Runner with tags](#executing-with-tags).
```python
...
    def on_skip(self):
        # Write your own code here
        pass 
    ...
```

#### On Class Skip
On Class Skip event is triggered, when test suites are skipped. Skip is supported by [@test](#test) & [@Suite](#suite) 
function decorators. See [Skipping Tests/Suites](#skipping-testssuites) for examples.
```python
...
    def on_class_skip(self):
        # Write your own code here
        pass 
    ...
```

#### On Before Class Failure
On Before Class Failure event is triggered only when a function decorated with [@beforeClass](#beforeclass) 
produces `AssertionError`. Make sure to include `exception` argument in the method signature, Exception object will be 
accessible through this argument. [On Ignore](#on-ignore) will also fire.
```python
...
    def on_before_class_failure(self, exception):
        # Write your own code here
        pass 
    ...
```

#### On Before Class Error
On Before Class Error event is triggered only when a function decorated with [@beforeClass](#beforeclass) 
produces exception other than `AssertionError`. Make sure to include `exception` argument in the method signature, 
Exception object will be accessible through this argument. [On Ignore](#on-ignore) will also fire.
```python
...
    def on_before_class_error(self, exception):
        # Write your own code here
        pass 
    ...
```


#### On After Class Failure
On After Class Failure event is triggered only when a function decorated with [@afterClass](#afterclass) 
produces `AssertionError`. Make sure to include `exception` argument in the method signature, Exception object will be 
accessible through this argument. No test level event listeners will be fired.
```python
...
    def on_after_class_failure(self, exception):
        # Write your own code here
        pass 
    ...
```

#### On After Class Error
On After Class Error event is triggered only when a function decorated with [@afterClass](#afterclass) 
produces exception other than `AssertionError`. Make sure to include `exception` argument in the method signature, 
Exception object will be accessible through this argument. No test level event listeners will be fired.
```python
...
    def on_after_class_error(self, exception):
        # Write your own code here
        pass 
    ...
```


#### Meta
All of the TestListener class instance functions have access to the test's and suite's meta information if such 
was passed in to the [@Suite](#suite) or [@test](#test) decorator. Metadata can be of any data type. 
You can use meta to set properties such as:
+ Test name, suite name, description, expected results etc - anything that can be useful in reporting
+ Test case IDs - if you have a test management system, leverage it to link test scripts directly 
to the test cases and further integrations can be implemented from there
+ Bug ticket IDs - if you have a bug tracking system, leverage it to link your test case with issues that are already 
known and allow you to process failures in a different manner and/or allow for other integrations with the 
tracking system
```python
from test_junkie.decorators import Suite, test


@Suite(listener=MyTestListener, 
       meta={"name": "Your suite name", 
             "id": 123444})
class ExampleSuite:

    @test(meta={"name": "You test name", 
                "id": 344123, 
                "known_bugs": [11111, 22222, 33333], 
                "expected": "Assertion must pass"})
    def a_test(self):
    
        assert True is True
```
Metadata that was set in the code above can be accessed in any of the event listeners like so:
```python
from test_junkie.testlistener import TestListener


class MyTestListener(TestListener):

    def __init__(self, **kwargs):

        TestListener.__init__(self, **kwargs)

    def on_success(self):
        
        print("Suite name: {name}".format(name=self.kwargs["class_meta"]["name"]))
        print("Suite ID: {id}".format(id=self.kwargs["class_meta"]["id"]))
        print("Test name: {name}".format(name=self.kwargs["test_meta"]["name"]))
        print("Test ID: {id}".format(id=self.kwargs["test_meta"]["id"]))
        print("Expected result: {expected}".format(expected=self.kwargs["test_meta"]["expected"]))
        print("Known bugs: {bugs}".format(bugs=self.kwargs["test_meta"]["known_bugs"]))
```

#### Tags
Test Junkie allows you to tag your test scenarios. You can use the tags to run or skip test cases that match the tags 
when you run your tests. Following tag configurations are supported:
+ `run_on_match_all` - Will run test cases that match all of the tags in the list. 
                       Will trigger [On Skip](#on-skip) event for all of the tests that do not match the tags 
                       or do not have tags.
+ `run_on_match_any` - Will run test cases that match at least one tag in the list
                       Will trigger [On Skip](#on-skip) event for all of the tests that do not match the tags 
                       or do not have tags.
+ `skip_on_match_all` - Will skip test cases that match all of the tags in the list. 
                        Will trigger [On Skip](#on-skip) event.
+ `skip_on_match_any` - Will skip test cases that match at least one tag in the list. 
                        Will trigger [On Skip](#on-skip) event.

All of the configs can be used at the same time. However, this is the order that will be honored:
 
`skip_on_match_all` -> `skip_on_match_any` -> `run_on_match_all` -> `run_on_match_any` 
which ever matches first will be executed or skipped. 

See [Using Runner with Tags](#executing-with-tags) for usage examples.

### Examples
#### Test Suite
```python
from random import randint
from test_junkie.decorators import test, Suite, beforeTest, beforeClass, afterTest, afterClass, meta
from example_package.example_listener import ExampleListener

# Listener here is optional as all of the other parameters
@Suite(listener=ExampleListener, retry=2, 
       meta=meta(suite_name="Demo Suite"))
class ExampleTestSuite(object):

    @beforeClass()
    def before_class(self):  # Functions are not restricted to any naming conventions
        print("BEFORE CLASS!")
        
    @beforeTest()
    def before_test(self):
        print("BEFORE TEST!")

    @afterTest()
    def after_test(self):
        print("AFTER TEST!")

    @afterClass()
    def after_class(self):
        print("AFTER CLASS!")
    
    # meta function is used for metadata, slightly cleaner then using a dict
    # all parameters are optional
    @test(parameters=[1, 2, 3, 4, 5], retry=2,
          meta=meta(name="Test 'A'",
                    test_id=344941,
                    known_bugs=[],
                    expected="Assertion must pass"), 
          tags=["component_a", "critical"])
    def a_test(self, parameter):  # Functions are not restricted to any naming conventions
        print("TEST 'A', param: ", parameter)
        assert randint(1, 5) == parameter, "your error message"

    # regular dict is used for metadata
    @test(meta={"name": "Test 'B'",
                "test_id": 344123,
                "known_bugs": [11111, 22222, 33333],
                "expected": "Assertion must pass"},
          tags=["component_a", "trivial", "known_failure"])
    def b_test(self):
        print("TEST 'B'")
        assert True is True

    @test(skip=True)
    def c_test(self):
        print("TEST 'C'")
```

#### Executing Test Suites
Use `TestRunner.run()` from `test_junkie.suiterunner` to run suites. `run()` takes in a list of suite objects.
```python
from test_junkie.suiterunner import TestRunner
from example_package.example_test_suite import ExampleTestSuite

TestRunner.run([ExampleTestSuite])
```
##### Executing with Tags
`TestRunner.run()` supports `tag_config` keyword that defines the configuration you want to use for the tags. 
All of the supported configurations as well as honor priority are defined in the [Tags](#tags) section.
```python
TestRunner.run([ExampleTestSuite], tag_config={"run_on_match_all": ["component_a", "critical"]})
```
```python
TestRunner.run([ExampleTestSuite], tag_config={"skip_on_match_any": ["trivial", "known_failure"]})
```