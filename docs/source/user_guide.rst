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

Parameter Item
==========================

A *parameter* has several pieces of information, as described in the source code
documentation, see :class:`~pyqparamwidget.param_item.ParameterItemBase`. There
are different types, depending on the type of parameter to be edited.  These are
the types available:

``ParameterItemCheckbox``
------------------------------------

.. code-block:: python

    ParameterItemCheckbox(
        "autoscale", True, tooltip="Otherwise, not autoscale."
        )

``ParameterItemChoice``
------------------------------------

.. code-block:: python

    ParameterItemChoice(
        "color", "",
        choices=["", "red", "green", "blue"],
        tooltip="Pick a color.",
        )

``ParameterItemIndex``
------------------------------------

.. code-block:: python

    ParameterItemIndex(
        "x", 50,
        hi=100,
        lo=0,
        tooltip="Choose a value from the range.",
        )

``ParameterItemText``
------------------------------------

.. code-block:: python

    ParameterItemText("title", "Suggested title", tooltip="Set the title. Be brief.")

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

This example defines three objects:

.. code-block:: python
    :linenos:

    parameters = {
        "title": qpw.param_item.ParameterItemText(
            "title",
            "Suggested title",
            tooltip="Set the title. Be brief."
            ),
        "color": qpw.param_item.ParameterItemChoice(
            "color",
            "",
            choices=["", "red", "green", "blue"],
            tooltip="Pick a color.",
        ),
        "autoscale": qpw.param_item.ParameterItemCheckbox(
            "autoscale",
            True,
            tooltip="Otherwise, not autoscale.",
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
