# -*- coding: utf-8 -*-
"""The graphical part of a Quantum ESPRESSO step"""

import molssi_workflow
import molssi_util.molssi_widgets as mw
import quantum_espresso_step
import Pmw
import pprint  # nopep8
import tkinter as tk
import tkinter.ttk as ttk


class TkQuantumESPRESSO(molssi_workflow.TkNode):
    """The node_class is the class of the 'real' node that this
    class is the Tk graphics partner for
    """

    node_class = quantum_espresso_step.QuantumESPRESSO

    def __init__(self, tk_workflow=None, node=None, canvas=None,
                 namespace='org.molssi.workflow.quantum_espresso_step.tk',
                 x=None, y=None, w=None, h=None):
        '''Initialize a node

        Keyword arguments:
        '''
        self.namespace = namespace
        self.dialog = None

        super().__init__(tk_workflow=tk_workflow, node=node,
                         canvas=canvas, x=x, y=y, w=w, h=h)
        self.create_dialog()

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit Quantum ESPRESSO step',
            command=self.handle_dialog)
        self.dialog.withdraw()

        # self._widget, which is inherited from the base class, is
        # a place to store the pointers to the widgets so that we can access
        # them later. We'll set up a short hand 'w' just to keep lines short
        w = self._widget
        frame = ttk.Frame(self.dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)
        w['frame'] = frame
        # make it large!
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        w = int(0.9 * sw)
        h = int(0.8 * sh)
        x = int(0.05 * sw / 2)
        y = int(0.1 * sh / 2)

        self.dialog.geometry('{}x{}+{}+{}'.format(w, h, x, y))

        self.quantum_espresso_tk_workflow = molssi_workflow.TkWorkflow(
            master=frame,
            workflow=self.node.quantum_espresso_workflow,
            namespace=self.namespace
        )
        self.quantum_espresso_tk_workflow.draw()

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Quantum ESPRESSO input
        """
        if self.dialog is None:
            self.create_dialog()

        self.dialog.activate(geometry='centerscreenfirst')

    def handle_dialog(self, result):
        if result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result))

        self.dialog.deactivate(result)

        # set up our shorthand for the widgets
        w = self._widget
    def update_workflow(self, tk_workflow=None, workflow=None):
        """Update the nongraphical workflow. Only used in nodes that contain
        workflows"""

        super().update_workflow(
            workflow=self.node.quantum_espresso_workflow,
            tk_workflow=self.quantum_espresso_tk_workflow
        )

    def from_workflow(self, tk_workflow=None, workflow=None):
        """Recreate the graphics from the non-graphical workflow.
        Only used in nodes that contain workflow"""

        super().from_workflow(
            workflow=self.node.quantum_espresso_workflow,
            tk_workflow=self.quantum_espresso_tk_workflow
        )

    def handle_help(self):
        """Not implemented yet ... you'll need to fill this out!"""
        print('Help!')
