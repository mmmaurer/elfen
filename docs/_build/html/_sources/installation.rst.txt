Installation
============

Package installation
--------------------

To install the current release of the package, you can use ``pip``

.. code-block:: bash

    python -m pip install elfen

or ``conda``

.. code-block:: bash

    conda install -c conda-forge elfen

Alternatively, you can install the package from source:

.. code-block:: bash

    python -m pip install git+https://github.com/mmmaurer/elfen.git

To install an editable version of the package, you can use the following command:

.. code-block:: bash

    python -m pip install -e git+https://github.com/mmmaurer/elfen.git


All of these options will install the package and all its dependencies.

Additional resources and models
-----------------------------------

To use the package, you will need to install additional resources and models.

Backbone models
~~~~~~~~~~~~~~~~

Since the NLP backbones are built on top of `spaCy`_ and `stanza`_, you will need to install the respective models for the languages you want to use. You can find the installation instructions for `spacy here <https://spacy.io/usage/models>`_ and for `stanza here <https://stanfordnlp.github.io/stanza/models.html>`_.

.. _spaCy: https://spacy.io
.. _stanza: https://stanfordnlp.github.io/stanza/

For the default small English spacy model, you can install it using the following command:

.. code-block:: bash

    python -m spacy download en_core_web_sm

The default stanza model will be downloaded automatically when you first use it.

Third-party resources
~~~~~~~~~~~~~~~~~~~~~

If you want to use the wordnet-based semantic features, you will need to download the respective open multilingual wordnet database. Consult the `wn package documentation`_ for more information.

.. _wn package documentation: https://wn.readthedocs.io/en/latest/

To install the full open multilingual wordnet database, you can use the following command:

.. code-block:: bash

    python -m wn download omw:1.4

Default norms and lexicons
~~~~~~~~~~~~~~~~~~~~~~~~~~

The package uses some established norms and lexicons for some features (psycholinguistic norms, sentiment/emotion lexicons, etc.). These will be downloaded automatically when you first use the respective features via the ``extractor`` functionality [#f1]_ . Please note that the usage of these norms and lexicons is subject to their respective licenses. 

.. important::

    We only provide download functionality, and the user is responsible for complying with the respective licenses.

.. [#f1] For more information on the extractor functionality, see the :ref:`elfen.extractor` documentation or the :ref:`quickstart` and  :ref:`tutorials` sections.