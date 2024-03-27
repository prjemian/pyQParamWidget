"""
Constants

.. autosummary::

   ~PARM_TYPE_CHECKBOX 
   ~PARM_TYPE_CHOICE 
   ~PARM_TYPE_DEFAULT 
   ~PARM_TYPE_INDEX
   ~UNDEFINED_VALUE
   ~QPW_CheckBox
   ~QPW_Choice
   ~QPW_Index
   ~QPW_Text

The Python symbols define a text name (used in situation when the Python symbol
might not be available) and are used to create a specific kind of Qt Widget.
The next table shows the definitions:

======================  ==================  =========
Python symbol           Text name           Qt Widget
======================  ==================  =========
``PARM_TYPE_CHECKBOX``  ``"QPW_checkbox"``  QCheckBox
``PARM_TYPE_CHOICE``    ``"QPW_choice"``    QComboBox
``PARM_TYPE_INDEX``     ``"QPW_index"``     QSpinBox
``PARM_TYPE_DEFAULT``   ``"QPW_default"``   QLineEdit
======================  ==================  =========

.. note:: The ``QPW_`` prefix: pyQParamWidget

:see: https://www.pythonguis.com/tutorials/pyqt-dialogs/
"""

from PyQt5 import QtWidgets

# TODO: refactor into subclasses here


class QPW_CheckBox(QtWidgets.QCheckBox):
    """
    Widget type for checkbox or boolean parameter.

    .. autosummary::

       ~qpw_get
       ~qpw_set
    """

    original_type = type(True)

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.checkState())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setCheckState(2 if value else 0)


class QPW_Choice(QtWidgets.QComboBox):
    """
    Widget type for picking from a list.

    .. autosummary::

       ~qpw_get
       ~qpw_set
    """

    original_type = None

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.currentText())

    def qpw_set(self, value):
        """Set the widget's value."""
        if self.original_type is None:
            self.original_type = type(value)
        self.setCurrentText(str(value))


class QPW_Index(QtWidgets.QSpinBox):
    """
    Widget type for adjusting a number between limits.

    .. autosummary::

       ~qpw_get
       ~qpw_set
    """

    original_type = None

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.value())

    def qpw_set(self, value):
        """Set the widget's value."""
        if self.original_type is None:
            self.original_type = type(value)
        self.setValue(value)


class QPW_Text(QtWidgets.QLineEdit):
    """
    Widget type for editing as text.

    .. autosummary::

       ~qpw_get
       ~qpw_set
    """

    original_type = None

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.text())

    def qpw_set(self, value):
        """Set the widget's value."""
        if self.original_type is None:
            self.original_type = type(value)
        self.setText(str(value))


PARM_TYPE_CHECKBOX = "QPW_checkbox"
"""
Widget type for toggling a checkbox or boolean Parameter. (checked: True)

This will produce a ``QCheckBox`` widget in the editor.
"""

PARM_TYPE_CHOICE = "QPW_choice"
"""
Widget type for choosing a Parameter from a list.

This will produce a ``QComboBox`` widget in the editor.

PARAMETERS

- choices ([str]): List of possible string values.
"""

PARM_TYPE_INDEX = "QPW_index"
"""
Widget type for editing an integer Parameter within a range.

This will produce a ``QSpinBox`` widget in the editor.

PARAMETERS

- hi (int): Maximum value.
- lo (int): Minimum value.
"""

PARM_TYPE_DEFAULT = "QPW_default"
"""
Widget type for editing a Parameter as text.

This will produce a ``QLineEdit`` widget in the editor.
"""

UNDEFINED_VALUE = object
"""For comparison with user input, avoids comparison with an explicit value."""


_PARM_WIDGETS = {
    PARM_TYPE_CHECKBOX: QPW_CheckBox,
    PARM_TYPE_CHOICE: QPW_Choice,
    PARM_TYPE_DEFAULT: QPW_Text,
    PARM_TYPE_INDEX: QPW_Index,
}
_PARM_WIDGET_KEYS = list(_PARM_WIDGETS.keys())


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
