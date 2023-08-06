import os
import numpy as np
import gzip
import datetime
from lxml import etree


class VasprunXMLParserError(Exception):
    """Base class to handle errors related to parsing the vasprun.xml file."""
    pass


class VasprunXMLParser(object):
    """Base class to parse relevant output from a vasprun.xml file."""

    def __init__(self, vasprun_xml_file='vasprun.xml'):
        """
        :param vasprun_xml_file: name of the vasprun.xml file (default='vasprun.xml')
        :type vasprun_xml_file: str
        """
        self.vasprun_xml_file = os.path.abspath(vasprun_xml_file)
        self.xmlroot = self._get_vasprun_xml_root()

    def _get_vasprun_xml_root(self):
        """Read contents from a vasprun.xml or vasprun.xml.gz file, convert it into
        etree.ElementTree and get the root element with tag 'modeling'

        :raises: VasprunXMLParserError if the root element is not 'modeling'
        :return: root element of vasprun.xml
        :rtype: etree._Element
        """
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(self.vasprun_xml_file)
        xmlroot = tree.getroot()
        if xmlroot.tag != 'modeling':
            error_message = 'Root element of vasprun.xml "modeling" not found'
            raise VasprunXMLParserError(error_message)
        return xmlroot

    def read_composition_information(self):
        """Read the list of elemental species in the unit cell, and number of atoms, atomic mass, number of valence
        electrons, VASP pseudopotential title tag for each species.

        :return: unit cell composition information.
                 - {element1: {'natoms': n1, 'atomic_mass': m1, 'valence': v1, 'pseudopotential': p1}, element2: ...}
        :rtype: dict(str, dict(str, int or float or str))
        """
        atomtypes_array = self.xmlroot.findall('./atominfo/array')
        composition_info = {}
        for array in atomtypes_array:
            if array.attrib['name'] != 'atomtypes':
                continue
            for species in array.findall('./set/rc'):
                natoms, elem, mass, valence, psp = [c.text.strip() for c in species.findall('c')]
                composition_info.update({elem: {'natoms': int(natoms),
                                                'atomic_mass': float(mass),
                                                'valence': float(valence),
                                                'pseudopotential': psp
                                                }
                                         })
        return composition_info

    def read_list_of_atoms(self):
        """Read the list of atoms in the unit cell.

        :return: list of atoms ['atom1', 'atom1', 'atom2', 'atom2', 'atom2', ...]
        :rtype: list
        """
        atoms_array = self.xmlroot.findall('./atominfo/array')
        atomslist = []
        for array in atoms_array:
            if array.attrib['name'] != 'atoms':
                continue
            for species in array.findall('./set/rc'):
                atom_symbol, atomtype = [c.text.strip() for c in species.findall('c')]
                atomslist.append(atom_symbol)
        return atomslist

    def read_number_of_ionic_steps(self):
        """Read number of ionic steps in the VASP run.

        :return: number of ionic steps
        :rtype: int
        """
        return len(self.xmlroot.findall('./calculation'))

    def read_scf_energies(self):
        """Read all the the energies in every ionic step.

        :return: {ionic_step_1: [e1, e2, e3, ...], ionic_step_2: [e1, e2, ...], ionic_step_3: ...}
        :rtype: dict(int, list(float))
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        scf_energies = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            scsteps = ionic_step.findall('scstep')
            scstep_energies = []
            for scstep in scsteps:
                for energy in scstep.findall('./energy/i'):
                    if energy.attrib['name'] == 'e_fr_energy':
                        scstep_energies.append(float(energy.text.strip()))
            scf_energies[n_ionic_step] = scstep_energies
        return scf_energies

    def read_entropies(self):
        """Read entropy at the end of each ionic step.

        :return: {ionic_step_1: entropy_1, ionic_step_2: entropy_2, ionic_step_3: ...}
        :rtype: dict(int, float)
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        entropy_dict = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            entropy = None
            final_scstep = ionic_step.findall('scstep')[-1]
            for final_energy_block in final_scstep.findall('energy'):
                for energy in final_energy_block.findall('i'):
                    if energy.attrib['name'] == 'eentropy':
                        entropy = float(energy.text.strip())
            entropy_dict[n_ionic_step] = entropy
        return entropy_dict

    def read_free_energies(self):
        """Read free energy at the end of each ionic step.

        :return: {ionic_step_1: free_energy_1, ionic_step_2: free_energy_2, ionic_step_3: ...}
        :rtype: dict(int, float)
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        free_energy_dict = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            free_energy = None
            final_scstep = ionic_step.findall('scstep')[-1]
            for final_energy_block in final_scstep.findall('energy'):
                for energy in final_energy_block.findall('i'):
                    if energy.attrib['name'] == 'e_fr_energy':
                        free_energy = float(energy.text.strip())
            free_energy_dict[n_ionic_step] = free_energy
        return free_energy_dict

    def read_forces(self):
        """Read forces on all atoms in the unit cell at the end of each ionic step.

        :return: {ionic_step_1: [[fx_1, fy_1, fz_1], [fx_2, fy_2, fz_2], ...], ionic_step_2: ...}
        :rtype: dict(int, numpy.array)
                - numpy.array of shape (N_atoms, 3)
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        forces_dict = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            varrays = ionic_step.findall('varray')
            forces = []
            for varray in varrays:
                if varray.attrib['name'] != 'forces':
                    continue
                for force_on_atom in varray.findall('v'):
                    forces.append([float(e) for e in force_on_atom.text.split()])
            forces_dict[n_ionic_step] = np.array(forces)
        return forces_dict

    def read_stress_tensors(self):
        """Read stress (in kbar) on the unit cell at the end of each ionic step.

        :return: {ionic_step_1: [[Sxx, Sxy, Sxz], [Syx, Syy, Syz], [Szx, Szy, Szz]], ionic_step_2: ...}
        :rtype: dict(int, numpy.array)
                - numpy.array of shape (3, 3)
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        stress_tensor_dict = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            varrays = ionic_step.findall('varray')
            stress_tensor = []
            for varray in varrays:
                if varray.attrib['name'] != 'stress':
                    continue
                for stress_component in varray.findall('v'):
                    stress_tensor.append([float(e) for e in stress_component.text.split()])
            stress_tensor_dict[n_ionic_step] = np.array(stress_tensor)
        return stress_tensor_dict

    def read_lattice_vectors(self):
        """Read lattice vectors (in Angstrom) of the unit cell at the end of each ionic step.

        :return: {ionic_step_1: [[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]], ionic_step_2: ...}
        :rtype: dict(key, numpy.array)
                - numpy.array of shape (3, 3)
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        lattice_vectors_dict = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            varrays = ionic_step.findall('./structure/crystal/varray')
            lattice_vectors = []
            for varray in varrays:
                if varray.attrib['name'] != 'basis':
                    continue
                for lattice_vector in varray.findall('v'):
                    lattice_vectors.append([float(e) for e in lattice_vector.text.split()])
            lattice_vectors_dict[n_ionic_step] = np.array(lattice_vectors)
        return lattice_vectors_dict

    def read_cell_volumes(self):
        """Read the volume (in cubic Angstrom) of the unit cell at the end of each ionic step.

        :return: {ionic_step_1: float, ionic_step_2: float}
        :rtype: dict(int, float)
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        volume_dict = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            volume = float(ionic_step.find('./structure/crystal/i').text.strip())
            volume_dict[n_ionic_step] = volume
        return volume_dict

    def read_fermi_energy(self):
        """
        :return: Fermi energy
        :rtype: float
        """
        try:
            fermi_energy = float(self.xmlroot.find('./calculation/dos/i').text.strip())
        except (AttributeError, TypeError):
            fermi_energy = None
        return fermi_energy

    def read_band_occupations(self):
        """Read occupation of every band at every k-point for each spin channel.

        :return: {'spin_1': {kpoint_1: {'band_energy': [band1, ...], 'occupation': [occ1, ...]}, 'kpoint_2': ...}}
        :rtype: dict(str, dict(int, dict(str, list(float))))
        """
        final_ionic_step = self.xmlroot.findall('./calculation')[-1]
        eigenvalues = final_ionic_step.find('eigenvalues')
        if eigenvalues is None:
            return
        occupations_dict = {}
        for spin_set in eigenvalues.findall('./array/set/set'):
            spin = spin_set.attrib['comment'].replace(' ', '_')
            occupations_dict[spin] = {}
            for kpoint_set in spin_set.findall('./set'):
                kpoint = int(kpoint_set.attrib['comment'].split()[-1])
                occupations_dict[spin][kpoint] = {'band_energy': [], 'occupation': []}
                for band in kpoint_set.findall('./r'):
                    be, occ = [float(b) for b in band.text.strip().split()]
                    occupations_dict[spin][kpoint]['band_energy'].append(be)
                    occupations_dict[spin][kpoint]['occupation'].append(occ)
        return occupations_dict

    def read_run_timestamp(self):
        """Read the time and date when the calulation was run.

        :return: year, month, day, hour, minute, second when the calculation was run.
        :rtype: `datetime.datetime` object
        """
        date_and_time = self.xmlroot.findall('./generator/i')
        year = month = day = hour = minute = second = 0
        for field in date_and_time:
            if field.attrib['name'] == 'date':
                year, month, day = [int(f) for f in field.text.strip().split()]
            if field.attrib['name'] == 'time':
                hour, minute, second = [int(f) for f in field.text.strip().split(':')]
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def read_scf_looptimes(self):
        """Read total time taken for each SCF loop during the run.

        :return: {ionic_step_1: [t1, t2, t3, ...], ionic_step_2: [t1, t2, ...], ...}
        :rtype: dict(int, list(float))
        """
        ionic_steps = self.xmlroot.findall('./calculation')
        scf_looptimes = {}
        for n_ionic_step, ionic_step in enumerate(ionic_steps):
            scsteps = ionic_step.findall('scstep')
            scstep_times = []
            for scstep in scsteps:
                for time in scstep.findall('time'):
                    if time.attrib['name'] == 'total':
                        scstep_times.append(float(time.text.strip().split()[-1]))
            scf_looptimes[n_ionic_step] = scstep_times
        return scf_looptimes

