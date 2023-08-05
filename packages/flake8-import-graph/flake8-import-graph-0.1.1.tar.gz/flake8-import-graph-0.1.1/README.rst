Flake8 Import Graph
===================

A flake8 lint to enforce that some modules can't be imported from other
modules.


::

    pip install flake8-import-graph==0.1.1


Configure it, by putting ``.flake8`` file in the package root:

::

    [flake8]
    deny-imports =
        # Don't allow models importing controllers
        myapp.models=myapp.controllers
        # Don't allow controllers to import sqlalchemy directly
        myapp.controllers=sqlalchemy


License
=======

Licensed under either of

* Apache License, Version 2.0,
  (./LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
* MIT license (./LICENSE-MIT or http://opensource.org/licenses/MIT)
  at your option.

------------
Contribution
------------

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be dual licensed as above, without any additional terms or
conditions.
