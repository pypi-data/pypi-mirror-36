# How to Install
`pip install pytest-atomic`

# How to use
```python
import pytest


@pytest.mark.atomic
class TestCls:
    def test_1(self):
        assert 0

    @pytest.mark.electronic
    def test_2(self):
        assert 1

    def test_3(self):
        assert 0

    @pytest.mark.electronic
    def test_4(self):
        assert 1

    def test_5(self):
        assert 0
```
```
(.env)$ pytest tests/ -v --tb=no
============================ test session starts =======================
platform darwin -- Python 3.7.0, pytest-3.8.0, py-1.6.0, pluggy-0.7.1 --
plugins: atomic-1.0
collected 5 items

tests/test_atomic.py::TestCls::test_1 FAILED                     [ 20%]
tests/test_atomic.py::TestCls::test_2 PASSED                     [ 40%]
tests/test_atomic.py::TestCls::test_3 SKIPPED                    [ 60%]
tests/test_atomic.py::TestCls::test_4 PASSED                     [ 80%]
tests/test_atomic.py::TestCls::test_5 SKIPPED                    [100%]

=============== 1 failed, 2 passed, 2 skipped in 0.05 seconds ==========
```
# Description
Tests after first `atomic` marked failed test in the same or child level will be skipped.
You can also specify a skip reason by `@pytest.mark.atomic('My weird skip reason')`.

If some test in skip level you want execute, you can easily mark `@pytest.mark.electronic`.
___

Feel free to contribute. If you encounter some bugs or have some advice please address a Issue.
