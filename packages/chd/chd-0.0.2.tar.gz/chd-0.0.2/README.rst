##############################################
CHD - Courses downloader for coursehunters.net
##############################################

Requirements
============

* `Python 3.6 <https://www.python.org/downloads/release/python-366/>`_ or higher. 


Installation
============


.. code-block:: bash

    pip install chd

Usage
-----

.. code-block:: bash

    chd url [-p path] [-s start_lesson] [-e end_lesson]

.. code-block:: bash

    url course url
    -p, --path download path, default is ~/downloads/course-name
    -s, --start the lesson number from which to start the download
    -e, --end the lesson number at which the download will be completed