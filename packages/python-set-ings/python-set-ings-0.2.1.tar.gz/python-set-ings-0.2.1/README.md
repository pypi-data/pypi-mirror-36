# Python set-ings

Load configuration from the environment for your python app. Supports typecasting and default values. Settings are made available in a way which plays nicely with IDEs and is easy to read.

## Installation

* `pipenv install python-set-ings` or `pip install python-set-ings`

## Usage

```python
# my_app/settings.py

from set_ings import Property
from set_ings import Settings as SettingsBase


Settings(SettingsBase):
    _PREFIX = 'YOUR_PREFIX'

    FOO = Property(10, cast=int)
    BAR = Property()


settings = Settings()
```

Then make sure you set the environment variables defined in your settings.
For the example above you would have to set `YOUR_PREFIX_BAR` and optionally
`YOUR_PREFIX_FOO`.

To use the settings anywhere in your app:
```python
from my_app.settings import settings

print(settings.FOO + 2)
```

## Contributing

### Installation

* `git clone git@github.com:evocount/python-set-ings.git`
* `cd python-set-ings`
* `pipenv install --dev`

### Running tests

* `pipenv run pytest`
or `pipenv run pytest --cov set_ings`

## License

This project is licensed under the [MIT License](LICENSE.md).
