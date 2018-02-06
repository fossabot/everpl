Installation
============

Preface
-------

As was mentioned [#f1]_, you need two pieces of software to use
the platform:

- the platform itself;
- and some client application.

This tutorial is mostly related to the platform itself. For details
about the installation and usage of client applications, please
visit the :doc:`./client_applications` page.


System Requirements
-------------------

Minimum System Requirements:

- Python 3.5 [#f2]_
- bash

Recommended System Requirements:

- Python 3.5 or newer
- UNIX-like operating system (like macOS and Linux-based systems)
- hardware support of protocols like Bluetooth, ZigBee and so on
  for different :doc:`./integrations`


Automatic Installation Steps
----------------------------

1. Download an archive with the latest stable release of platform
   from its repository: https://github.com/s-kostyuk/adpl/releases

.. NOTE::
    You can also download the latest development (unstable) version
    here: https://github.com/s-kostyuk/adpl by clicking a 'clone or
    download' button.

2. Extract archive content to some directory. Remember its
   placement (path).

3. Open terminal emulator, switch to the everpl's project directory::

    cd /path/to/everpls/directory

4. Install an everpl package using pip::

    pip3 install .

5. Now it's possible to run everpl application by simply calling
   an ``everpl`` command::

    everpl

Installation finished!

.. NOTE::
    You can also install everpl package in the "Development Mode".
    Why you may need it and what with mode provides is described
    by the following link: [#f4]_

Manual Installation Steps
-------------------------

1. Download an archive with the latest stable release of platform
   from its repository: https://github.com/s-kostyuk/adpl/releases

2. Extract archive content to some directory. Remember its
   placement (path).

3. Open terminal emulator, switch to the platform's directory::

    cd /path/to/platforms/directory

4. Install all needed dependencies that are listed in
   ``requirements.txt`` [#f3]_ file. The most simple way to do this
   is to use pip::

    pip3 install -r requirements.txt

5. Now it's possible to run the main execution file::

    bash ./dpl/run.sh

Installation finished!

.. rubric:: Footnotes

.. [#f1] Documentation page: :doc:`./getting_started`
.. [#f2] async/await expressions which are commonly used
        in the platform was introduced only in Python 3.5.

        In a case if you need a support of older versions of python -
        please, endorse this issue: `#22 <https://github.com/s-kostyuk/adpl/issues/22>`_.
.. [#f3] Requirements file is placed in the root of platform's directory,
         for example: https://github.com/s-kostyuk/adpl/blob/devel/requirements.txt

.. [#f4] Information about "Development Mode" of package
         installation process:
         https://packaging.python.org/tutorials/distributing-packages/#working-in-development-mode
