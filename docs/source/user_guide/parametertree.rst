.. _guide.ParameterTree:

Parameter Tree
==================================

A *hierarchy* of parameters can be edited using the
:class:`~pyQParamWidget.param_tree.ParameterTree()` dialog.

.. seealso:: :ref:`guide.ParameterEditor`

Here is one example.

.. rubric:: View of a hierarchical parameter dictionary using ParameterTree

.. figure:: ../_static/qpw.png
   :width: 60%

   View of ``ParameterTree`` dialog.

The *hierarchy* (a dictionary of dictionaries) is displayed as a tree on the
left side.  The keys are text strings, to be displayed in the tree.  The end of
each branch of the tree is a dictionary of Parameter Items.  See the next block
of Python code.  When the end of a branch is selected, a :ref:`guide.ParameterEditor`
is shown in the right side of the dialog.

.. rubric:: Python code to construct the example hierarchical parameter dictionary

.. code-block:: python
    :linenos:

    import pyQParamWidget as qpw

    hierarchy = {
        "applications": {
            "tiled": {
                "server": {
                    "settings_file": qpw.ParameterItemText(
                        label="settings file", value="~/.config/settings.ini"
                    ),
                    "catalog": qpw.ParameterItemText(label="catalog", value="bluesky_data"),
                    "url": qpw.ParameterItemText(label="url", value="http://localhost"),
                },
            },
            "other": {
                "demo": qpw.ParameterItemCheckbox("demo mode?", True),
            },
        },
        "UI": {
            "plotting": {
                "autoplot": qpw.ParameterItemCheckbox(
                    label="autoplot",
                    value=True,
                    tooltip="Plot when the run is selected.",
                ),
                "autoselect": qpw.ParameterItemCheckbox(
                    label="autoselect",
                    value=True,
                    tooltip="Automatically select the signals to plot.",
                ),
                "colors": qpw.ParameterItemChoice(
                    label="colors", value="", choices=["", "r", "b", "g", "k"]
                ),
            },
        },
    }

.. rubric::  Python code to display the hierarchy in a ParameterTree dialog

.. code-block:: python
    :linenos:

    dialog = qpw.ParameterTree(None, parameters=hierarchy)
    # dialog.show()  # modeless: does not block
    dialog.exec()  # modal: blocks
    # Show the final values of the parameters, once the dialog is closed.
    print(f"{dialog.values()=}")

.. _guide:get-tree-values:

Get the values from the tree dialog
-----------------------------------

The widget's :meth:`~pyQParamWidget.param_tree.ParameterTree.values`
method returns a hierarchical dictionary with the accepted parameter values.  The dictionary
keys are the same as the parameter dictionary (``hierarchy``) supplied.

.. code-block:: python

    dialog = qpw.ParameterTree(None, parameters=hierarchy)
    dialog.exec()
    # ...user interaction
    results = dialog.values()

.. rubric:: EXAMPLE

Using the ``hierarchy`` dictionary above, and making no changes in the tree dialog,
``print(results)`` would return:

.. code-block:: python

    {
        "applications": {
            "tiled": {
                "server": {
                    "settings_file": "~/.config/settings.ini",
                    "catalog": "bluesky_data",
                    "url": "http://localhost",
                },
            },
            "other": {
                "demo": True,
            },
        },
        "UI": {
            "plotting": {
                "autoplot": True,
                "autoselect": True,
                "colors": "",
            },
    }

Accept and Reset buttons
------------------------

An alert will be shown (see :ref:`guide:alert`) if the editor has changes. It will
not be possible to select another item from the tree until the changes are
resolved.

.. rubric:: Alert message when selecting another tree item while editor has changes.

.. figure:: ../_static/tree-with-changes.png
   :width: 60%

   Editor shown for ``other`` parameters.

After the checkbox was changed, the ``server`` was selected.  This brings up the
*Alert* message, stating that changes must first be resolved.  Once the dialog
is closed, the selected item will be changed back to ``other``.
