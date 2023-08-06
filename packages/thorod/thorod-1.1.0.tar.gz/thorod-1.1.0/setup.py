# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['thorod']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'click-default-group>=1.2,<2.0',
 'click>=6.0,<7.0',
 'colorama>=0.3.9,<0.4.0',
 'crayons>=0.1.2,<0.2.0',
 'pendulum>=2.0,<3.0',
 'sortedcontainers>=2.0,<3.0',
 'toml>=0.9.4,<0.10.0',
 'tqdm>=4.19,<5.0']

extras_require = \
{'dev': ['flake8>=3.5,<4.0',
         'flake8-builtins>=1.0,<2.0',
         'flake8-import-order>=0.18,<0.19',
         'flake8-import-order-tbm>=1.0.0,<2.0.0',
         'poetry>=0.9,<0.10',
         'sphinx>=1.7,<2.0',
         'sphinx-click>=1.0,<2.0'],
 'doc': ['sphinx>=1.7,<2.0', 'sphinx-click>=1.0,<2.0'],
 'lint': ['flake8>=3.5,<4.0',
          'flake8-builtins>=1.0,<2.0',
          'flake8-import-order>=0.18,<0.19',
          'flake8-import-order-tbm>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['thorod = thorod.cli:thorod']}

setup_kwargs = {
    'name': 'thorod',
    'version': '1.1.0',
    'description': 'A CLI utility for torrent creation and manipulation.',
    'long_description': "\n# thorod\n\n[thorod](https://github.com/thebigmunch/thorod) is a CLI utility for torrent creation and manipulation.\n\n## What's a thorod?\n\nThorod means torrent (of water) in the Tolkien Elvish language of Sindarin.\n\n\n## Installation\n\n``pip install thorod``\n\n\n## Usage\n\nSee the [docs](https://thorod.readthedocs.io).\n\n\n## Appreciation\n\nShowing appreciation is always welcome.\n\n#### Thank\n\n[![Say Thanks](https://img.shields.io/badge/thank-thebigmunch-blue.svg?style=flat-square)](https://saythanks.io/to/thebigmunch)\n\nGet your own thanks inbox at [SayThanks.io](https://saythanks.io/).\n\n#### Contribute\n\n[Contribute](https://github.com/thebigmunch/thorod/blob/master/CONTRIBUTING.md) by submitting bug reports, feature requests, or code.\n\n#### Help Others/Stay Informed\n\n[Discourse forum](https://forum.thebigmunch.me/)\n\n#### Referrals/Donations\n\n[![Coinbase](https://img.shields.io/badge/Coinbase-referral-orange.svg?style=flat-square)](https://www.coinbase.com/join/52502f01e0fdd4d3ef000253) [![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-referral-orange.svg?style=flat-square)](https://m.do.co/c/3823208a0597) [![Namecheap](https://img.shields.io/badge/Namecheap-referral-orange.svg?style=flat-square)](https://www.namecheap.com/?aff=67208) [![PayPal](https://img.shields.io/badge/PayPal-donate-brightgreen.svg?style=flat-square)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=DHDVLSYW8V8N4&lc=US&item_name=thebigmunch&currency_code=USD)\n\n**BTC:** ``1BMLCFPcX8YHE1He2t3aBrsNDGr1pKhfFa``  \n**ETH:** ``0x8E3f8d8eAedeA61Bf34A998A2104954FE508D5d0``  \n**LTC:** ``LgsQU1YaY4a4s7m9efjn6m35XhVEpW1xoP``\n",
    'author': 'thebigmunch',
    'author_email': 'mail@thebigmunch.me',
    'url': 'https://github.com/thebigmunch/thorod',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
