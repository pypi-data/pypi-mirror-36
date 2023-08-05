# Simpl Authenticator

WAMP Authenticator Component for Simpl

## Installation

    $ pip install git+https://github.com/simplworld/simpl-authenticator.git@master#egg=authenticator

## Setup environment

    $ mkvirtualenv simpl-authenticator
    $ pip install -e .

## Development versioning

Install `bumpversion`:

    $ pip install bumpversion

Then, to release a new version, increment the version number with:

    $ bumpversion patch

Then push to the repo:

    $ git push && git push --tags

Copyright © 2018 The Wharton School,  The University of Pennsylvania 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
