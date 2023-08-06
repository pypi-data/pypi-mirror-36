aerial
===========

A Python library for receiving Unix style signals.


|Build Status| |Coverage Status| |Package Status|

.. |Build Status| image:: https://api.travis-ci.org/chrisbrake/aerial.svg?branch=master
   :target: https://travis-ci.org/chrisbrake/aerial
.. |Coverage Status| image:: https://coveralls.io/repos/github/chrisbrake/aerial/badge.svg?branch=master
   :target: https://coveralls.io/github/chrisbrake/aerial?branch=master
.. |Package Status| image:: https://badge.fury.io/py/aerial.svg
    :target: https://badge.fury.io/py/aerial


.. quick-start-section-marker

This library is meant to be a simple way to deal with handling signals, while avoiding callbacks.

Install it with pip

.. code-block:: bash

    pip install aerial
    
A simple use looks like this:

.. code-block:: python

   >>> import time
   >>> import signal
   >>> 
   >>> import aerial
   >>> def main_loop():
   ...     while not aerial.received(signal.SIGTERM):
   ...         if aerial.received(signal.SIGHUP):
   ...             print('Got a SIGHUP')
   ...         time.sleep(.5)
   ...     print('See you later')
   ... 
   >>> 


And try out the demo by running the module.

.. code-block:: bash

   python -m aerial
   [ PID 10852 ] Hello, send me a SIGTERM to exit, or a SIGHUP for a trick  #  In another terminal 
   [ PID 10852 ] Neat huh?                                                  #  kill -SIGHUP 10852
   [ PID 10852 ] See you later                                              #  kill -SIGTERM 10852


