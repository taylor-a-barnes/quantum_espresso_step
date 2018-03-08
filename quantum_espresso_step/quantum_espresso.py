# -*- coding: utf-8 -*-
"""Non-graphical part of the Quantum ESPRESSO step in a MolSSI workflow"""

import molssi_workflow
from molssi_workflow import units, Q_, data  # nopep8
import logging

logger = logging.getLogger(__name__)


class QuantumESPRESSO(molssi_workflow.Node):
    def __init__(self,
                 workflow=None,
                 namespace='org.molssi.workflow.quantum_espresso',
                 extension=None):
        '''Setup the non-graphical part of the Quantum ESPRESSO step in a
        MolSSI workflow.

        Keyword arguments:
        '''
        logger.debug('Creating Quantum ESPRESSO {}'.format(self))
        self.quantum_espresso_workflow = molssi_workflow.Workflow(
            parent=self, name='Quantum ESPRESSO',
            namespace=namespace)

        super().__init__(
            workflow=workflow,
            title='Quantum ESPRESSO',
            extension=extension)

    def run(self):
        """Run a Quantum ESPRESSO step.
        """
        # Get the first real node
        node = self.quantum_espresso_workflow.get_node('1').next()

        input_data = []
        while node is not None:
            keywords = node.get_input()
            input_data.append(' '.join(keywords))
            node = node.next()

        files = {'molssi.dat': '\n'.join(input_data)}
        logger.info('molssi.dat:\n' + files['molssi.dat'])

        local = molssi_workflow.ExecLocal()
        result = local.run(
            cmd=['quantum_espresso', '-in', 'molssi.dat'],  # nopep8
            files=files,
            return_files=[])

        if result is None:
            logger.error('There was an error running Quantum ESPRESSO')
            return None

        logger.debug('\n' + pprint.pformat(result))

        logger.info('stdout:\n' + result['stdout'])
        if result['stderr'] != '':
            logger.warning('stderr:\n' + result['stderr'])

        return super().run()
