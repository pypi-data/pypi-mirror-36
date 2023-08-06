import os
import unittest
from kelpie.vasp_run_manager import VaspSingleRunManager, VaspRunManagerError


sample_vasp_input_dir = os.path.join(os.path.dirname(__file__), 'sample_vasp_input')


class TestVaspSingleRunManager(unittest.TestCase):
    """Base class to test `vasp_run_manager.VaspSingleRunManager`"""

    vrm = VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'))

    def test_structure_file_not_specified(self):
        with self.assertRaises(VaspRunManagerError):
            VaspSingleRunManager()
        with self.assertRaises(FileNotFoundError):
            VaspSingleRunManager(input_structure_file='non_existent_POSCAR')

    def test_structure(self):
        from kelpie import io
        s = io.read_poscar(poscar_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'))
        self.assertEqual(self.vrm.input_structure.POSCAR, s.POSCAR)

    def test_calculation_workflow_not_specified(self):
        self.assertEqual(self.vrm.calculation_workflow, 'relaxation')

    def test_calculation_workflow_not_recognized(self):
        with self.assertRaises(NotImplementedError):
            VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                 calculation_workflow='hse')

    def test_run_location_not_specified(self):
        self.assertEqual(self.vrm.run_location, sample_vasp_input_dir)

    def test_host_scheduler_settings_not_specified(self):
        from kelpie.scheduler_settings import DEFAULT_SCHEDULER_SETTINGS
        self.assertEqual(self.vrm.host_scheduler_settings, DEFAULT_SCHEDULER_SETTINGS['cori_knl'])

    def test_host_scheduler_settings_path_to_file(self):
        custom_file = os.path.join(os.path.dirname(__file__), 'custom_scheduler.json')
        vrm = VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                   host_scheduler_settings=custom_file)
        self.assertEqual(vrm.host_scheduler_settings['exe'], 'vasp_ncl')

    def test_host_scheduler_settings_nondefault_tag(self):
        vrm = VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                   host_scheduler_settings='cori_haswell')
        self.assertEqual(vrm.host_scheduler_settings['n_mpi_per_node'], 32)

    def test_host_scheduler_settings_tag_not_recognized(self):
        with self.assertRaises(VaspRunManagerError):
            VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                 host_scheduler_settings='quest')

    def test_batch_script_template_not_specified(self):
        from kelpie.scheduler_templates import SCHEDULER_TEMPLATES
        self.assertEqual(self.vrm.batch_script_template, SCHEDULER_TEMPLATES['cori'])

    def test_batch_script_template_path_to_file(self):
        custom_file = os.path.join(os.path.dirname(__file__), 'custom_scheduler.json')
        vrm = VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                   batch_script_template=custom_file)
        self.assertEqual(vrm.batch_script_template, custom_file)

    def test_batch_script_template_nondefault_tag(self):
        from kelpie.scheduler_templates import SCHEDULER_TEMPLATES
        vrm = VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                   batch_script_template='quest')
        self.assertEqual(vrm.batch_script_template, SCHEDULER_TEMPLATES['quest'])

    def test_batch_script_template_tag_not_recognized(self):
        with self.assertRaises(VaspRunManagerError):
            VaspSingleRunManager(input_structure_file=os.path.join(sample_vasp_input_dir, 'POSCAR.all_OK'),
                                 batch_script_template='bridges')

    def test_batch_script(self):
        cori_test_script = os.path.join(os.path.dirname(__file__), 'cori_test_batch_script.q')
        with open(cori_test_script, 'r') as fr:
            self.assertEqual(self.vrm.batch_script.strip().split()[-1], fr.read().strip().split()[-1])

    @unittest.skip('Call to "srun" fails, obviously')
    def test_vasp_static_workflow(self):
        vrm = VaspSingleRunManager(input_structure_file='sample_vasp_input/POSCAR.all_OK',
                                   run_location='test_static_workflow')
        vrm.vasp_static_workflow()


if __name__ == '__main__':
    unittest.main()


