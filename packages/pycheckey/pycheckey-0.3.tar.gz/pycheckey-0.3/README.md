# PyChecKey

Ever have JSON or a large dictionary that you want to validate before you jump deeper into it? PyChecKey allows you to check a dictionary-like object against a defined structure.

This works with Python 3.5+.

## Components

Below are the components and common examples of how to use them.

### KeyEnsurer

A `KeyEnsurer` allows checking against a dictionary-like structure. 

```python
from pycheckey import KeyEnsurer


data = {
    "key1": 4,
    "key2": {
        "innerKey": "hi"
    }
}

ensurer = KeyEnsurer(data=data, required_keys=['key1', 'key2.innerKey', 'key3'])

ensurer.validate()  # Will return false because key3 does not exist!
print(ensurer.missing)  # ['key3']

ensurer.key_exists(data, 'key2.inner')  # Returns true because data[key2][inner] exists

```

## Local Development

To work on this repository, you need `virtualenv`. Clone it first, then run the following two commands.

```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

### Running Tests

Run `pytest` from the root directory to run all tests.

### Linting

Run `pylint` from the root directory to lint the code files.