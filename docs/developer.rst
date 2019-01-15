.. _developer:

Developer's manual
===================

.. module:: traffic_info

| traffic_info is developed as a Python package so you can include it to your own code.
| Here is a quick example:

.. code:: python

   from traffic_info import Location, MapScreenshot, send_email

   location = Location(43.6037834, 1.4402123, 16)
   screenshot = MapScreenshot("/usr/local/bin/chromedriver")
   screenshot.take(location)
   send_email("trafficinfo@example.com", "user@example.com", location, screenshot)


Reference
---------

Location object
~~~~~~~~~~~~~~~

.. autoclass:: traffic_info.Location
   :members:
   :inherited-members:

MapScreenshot object
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: traffic_info.MapScreenshot
   :members:
   :inherited-members:

Utility functions
~~~~~~~~~~~~~~~~~

.. autofunction:: get_chromedriver_path

.. autofunction:: send_email
