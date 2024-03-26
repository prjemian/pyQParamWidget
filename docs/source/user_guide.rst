===========
User Guide
===========

TODO

This package simplifies the construction of a ``QWidget`` for the user to edit a
set of parameters (of a PyQt5 application.)  It provides a single
:ref:`guide.ParameterEditorWidget` screen for editing a set of
:ref:`guide.ParameterItem` objects and a :ref:`guide.ParameterEditorTree`
dialog for editing a hierarchical structure with various sets of parameters.

.. _guide.ParameterItem:

``ParameterItem``
==========================

A *parameter* has several pieces of information, as described in the source code
documentation, see :class:`~pyqparamwidget.param_item.ParameterItem`. There are
different widget types, depending on the type of parameter to be edited.

Parameter types
----------------------

======================  ==================  =========
Python symbol           Text name           Qt Widget
======================  ==================  =========
``PARM_TYPE_CHECKBOX``  ``"QPW_checkbox"``  QCheckBox
``PARM_TYPE_CHOICE``    ``"QPW_choice"``    QComboBox
``PARM_TYPE_INDEX``     ``"QPW_index"``     QSpinBox
``PARM_TYPE_DEFAULT``   ``"QPW_default"``   QLineEdit
======================  ==================  =========

For each, show code and example image.

``PARM_TYPE_CHECKBOX``
------------------------------------

.. code-block:: python

    ParameterItem(
        "autoscale", True,
        tooltip="Otherwise, not autoscale.",
        widget="QPW_checkbox",
        )

``PARM_TYPE_CHOICE``
------------------------------------

.. code-block:: python

    ParameterItem(
        "color", "",
        choices=["", "red", "green", "blue"],
        tooltip="Pick a color.",
        widget="QPW_choice",
        )

``PARM_TYPE_INDEX``
------------------------------------

.. code-block:: python

    ParameterItem(
        "x", 50,
        hi=100,
        lo=0,
        tooltip="Choose a value from the range.",
        widget="QPW_index",
        )

``PARM_TYPE_DEFAULT``
------------------------------------

.. code-block:: python

    ParameterItem("title", "Suggested title")

.. _guide.ParameterEditorWidget:

``ParameterEditorWidget``
==================================

For the source code documentation, see 
:class:`~pyqparamwidget.param_editor.ParameterEditorWidget`.

.. rubric:: EXAMPLE

First make a dictionary of 
:class:`~pyqparamwidget.param_item.ParameterItem` objects.
The keys of the dictionary can be strings or Python objects or 
any other structure allowed by Python as dictionary keys.  The
keys, themselves, are not used by ``ParameterEditorWidget``.  They
are only used to identify each of the ``ParameterItem`` objects.

This example defines three ``ParameterItem`` objects:

.. code-block:: python
    :linenos:

    parameters = {
        "title": ParameterItem("title", "Suggested title"),
        "color": ParameterItem(
                "color", "",
                choices=["", "red", "green", "blue"],
                tooltip="Pick a color.",
                widget="QPW_choice",
                ),
        "autoscale": ParameterItem(
                "autoscale", True,
                tooltip="Otherwise, not autoscale.",
                widget="QPW_checkbox",
                ),

    }

Next, create the ``ParameterEditorWidget`` object, passing in the ``parent``
object (usually the ``QWidget`` object that will contain this new widget) and
the ``parameters`` dictionary.

.. code-block:: python

    panel = ParameterEditorWidget(parent, parameters)

Finally, add ``panel`` into parent's layout.

.. _guide.ParameterEditorTree:

``ParameterEditorTree``
==================================

TODO
