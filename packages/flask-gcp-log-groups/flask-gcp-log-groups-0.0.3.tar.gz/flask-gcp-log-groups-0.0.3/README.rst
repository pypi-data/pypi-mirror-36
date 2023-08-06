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

For example, in the following snippet, all log lines will appear under
one top-level HTTP Request within `Google Cloud Logging`_:

.. code:: python

   @app.route('/')
   def default():
     app.logger.setLevel(logging.INFO)
     app.logger.info("I met a traveller from an antique land,")
     app.logger.info("Who said: Two vast and trunkless legs of stone")
     app.logger.info("Stand in the desert... near them, on the sand,")
     app.logger.info("Half sunk, a shattered visage lies, whose frown,")
     app.logger.info("And wrinkled lip, and sneer of cold command,")
     app.logger.info("Tell that its sculptor well those passions read")
     app.logger.info("Which yet survive, stamped on these lifeless things,")
     app.logger.info("The hand that mocked them and the heart that fed;")

     app.logger.info("And on the pedestal these words appear:")
     app.logger.error("'My name is Ozymandias, king of kings;")
     app.logger.error("Look on my works, ye Mighty, and despair!'")
     app.logger.info("Nothing beside remains. Round the decay")
     app.logger.info("Of that colossal wreck, boundless and bare")
     app.logger.info("The lone and level sands stretch far away.")

     app.logger.info( { "author": {
                                    "firstName": "PERCY",
                                    "lastName": "SHELLEY"
                                  },
                        "title": "Ozymandias"
                      } )
     return 'ok'

as in

.. image:: log_entry.png
   :target: https://raw.githubusercontent.com/salrashid123/flask-gcp-log-groups/master/images/log_entry.png

Note, that the application log entry does appear in the unfiltered logs
still but users will ‘see’ all the log lines associated with the parent
http_request.

What makes this possible is attaching the ``traceID`` field to each
application log entry as well as emitting the parent ``http_request``.
Google cloud logging will use the traceID and “collapse” them together.

--------------

Usage
-----

To use this, you need a Google Cloud Platform project first.

Install `gcloud sdk`_ to test locally or run in an envionment where
`Application Default Credentials`_ is setup.

A trace header value must also get sent

.. _google-cloud-logging: https://pypi.org/project/google-cloud-logging/
.. _CloudLoggingHander: https://googlecloudplatform.github.io/google-cloud-python/latest/logging/handlers.html
.. _Google Cloud Logging: https://cloud.google.com/logging/
.. _gcloud sdk: https://cloud.google.com/sdk/docs/quickstarts
.. _Application Default Credentials: https://cloud.google.com/docs/authentication/production#obtaining_credentials_on_compute_engine_kubernetes_engine_app_engine_flexible_environment_and_cloud_functions

.. |images/log_entry.png| image:: images/log_entry.png