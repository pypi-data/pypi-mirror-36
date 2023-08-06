Flask extension for grouped log lines for Google Cloud Logging
==============================================================

Flask extension that allows log lines emitted within a request handler
to display/render together.

Normally, when using Google Cloud Logging libraries (
`google-cloud-logging`_ and `CloudLoggingHander`_), each log entry that
gets emitted is displayed separately within the Logging UI. However, its
desireable to group all logs together that logically belong that way in
an HTTP Request. For a given HTTP Request into FLask, this extension
displays all the logs ‘together’ below the parent request.

.. code:: python

   @app.route('/')
   def default():
     app.logger.setLevel(logging.INFO)
     app.logger.info("I met a traveller from an antique land,")
     app.logger.info("Who said: Two vast and trunkless legs of stone")
     return 'ok'

as in

.. image:: log_entry.png
   :target: https://raw.githubusercontent.com/salrashid123/flask-gcp-log-groups/master/images/log_entry.png

--------------

Usage
-----
.. code:: python

   from flask_gcp_log_groups import GCPHandler
   app = Flask(__name__)

   g = GCPHandler(app, parentLogName="request",
        childLogName="application",
        traceHeaderName='X-Cloud-Trace-Context',
        labels= {'foo': 'bar', 'baz': 'qux'},
        resource='global')
   g.setLevel(logging.INFO)
   app.logger.addHandler(g)

   @app.route('/')
   def default():
     app.logger.setLevel(logging.INFO)
     app.logger.info("I met a traveller from an antique land,")
     app.logger.info("Who said: Two vast and trunkless legs of stone")