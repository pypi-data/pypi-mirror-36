Readme Renderer
===============

Readme Renderer is a library that will safely render arbitrary
``README`` files into HTML. It is designed to be used in Warehouse_ to
render the ``long_description`` for packages. It can handle Markdown,
reStructuredText (``.rst``), and plain text.

.. _Warehouse: https://github.com/pypa/warehouse


Check Description Locally
-------------------------

reStructuredText
~~~~~~~~~~~~~~~~

To locally check whether your reStructuredText long descriptions will render on
PyPI, simply install the ``readme_renderer`` library using:

.. code-block:: console

    $ pip install readme_renderer
    $ python setup.py check -r -s
    running check

If there's a problem rendering your ``long_description``, the check
will tell you. If your ``long_description`` is fine, you'll get no
output.


Markdown
~~~~~~~~

Checking your Markdown long descriptions is unecessary, because unlike rST,
where a properly rendered description is all-or-nothing, PyPI will still render
your Markdown description as Markdown if it has some invalid or incorrect
syntax.


Code of Conduct
---------------

Everyone interacting in the readme_renderer project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
