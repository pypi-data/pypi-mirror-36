# Health Checker
Verifies if several checks are ok within a class.

# Install
`pip install -r requirements-dev.txt`

# Run tests
Simple: `py.test`  
With coverage: `py.test --cov=healthchecker --cov-report term-missing`

# Usage
Install via `pip install health-checker`.

Extend `CheckCase` on you class and decorate all check methods with `check`
decorator. If the method raises an exception or returns any falsy value,
the check is considered a failure, otherwise it's considered a success.

```python
from healthchecker import CheckCase, check


class MyClass(CheckCase):
    def my_method(self):
        self.check()
        if self.has_succeeded():
            ''' do something '''
        else:
            ''' do something else '''

    @check
    def my_dummy_check(self):
        return False

    @check
    def another_check(self):
        raise Exception()

    @check
    def i_am_good(self):
        return 'can be a string'

    @check
    def also_good(self):
        return True
```

`self.has_succeeded()` returns `False` for the above code due to `my_dummy_check` and `another_check` check methods.  
`self.check_report` will be `{'my_dummy_check': False, 'another_check': False, 'i_am_good': 'can_be_string', 'also_good': True}`
