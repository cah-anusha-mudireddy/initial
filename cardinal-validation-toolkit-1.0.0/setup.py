# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cardinal_validation_toolkit',
 'cardinal_validation_toolkit.schemas',
 'cardinal_validation_toolkit.schemas.v1']

package_data = \
{'': ['*']}

install_requires = \
['fastjsonschema>=2.15.3,<3.0.0', 'importlib-resources>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'cardinal-validation-toolkit',
    'version': '1.0.0',
    'description': 'Validates Cardinal CSV files',
    'long_description': None,
    'author': 'Product Engineering',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
