# pytest_expectr

pytest-expectr is a plugin for [pytest](https://docs.pytest.org/en/latest/) that provide expect to tests/fixtures for multiple assert use.

## Requirements

You will need the following prerequisites in order to use pytest-variables:

- Python 2.7, 3.6, PyPy, or PyPy3
- pytest 2.6 or newer

## How to install

To install pytest-expectr:

```bash
pip install git+https://github.com/Benabra/pytest_expectr.git
```

## How to use

```python
def test_hello(expect):
    expect(1==2, 'your error message 1')
    expect(1==3, 'your error message 2')
    ...
```
