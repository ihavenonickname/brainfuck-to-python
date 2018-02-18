import unittest
from brainfuck_to_python import brainfuck_to_python as bf_to_py

class TestBrainfuckToPython(unittest.TestCase):
    def _to_py_code(self, lines):
        boilerplate_lines = [
            'from collections import defaultdict',
            'cells = defaultdict(int)',
            'cell_addr = 0'
        ]

        return '\n'.join(boilerplate_lines + lines)

    def test_basic(self):
        bf = '''
        +>+>-<-<
        '''
        py = self._to_py_code([
            'cells[cell_addr] += 1',
            'cell_addr += 1',
            'cells[cell_addr] += 1',
            'cell_addr += 1',
            'cells[cell_addr] -= 1',
            'cell_addr -= 1',
            'cells[cell_addr] -= 1',
            'cell_addr -= 1'
        ])

        self.assertEqual(bf_to_py(bf), py)

    def test_indentation(self):
        bf = '''
        >[>[>]+]-
        '''
        py = self._to_py_code([
            'cell_addr += 1',
            'while cells[cell_addr]:',
            '    cell_addr += 1',
            '    while cells[cell_addr]:',
            '        cell_addr += 1',
            '    cells[cell_addr] += 1',
            'cells[cell_addr] -= 1',
        ])

        self.assertEqual(bf_to_py(bf), py)

    def test_reduction_instructions(self):
        bf = '''
        +++--->>>---<<<+++
        '''
        py = self._to_py_code([
            'cell_addr += 3',
            'cells[cell_addr] -= 3',
            'cell_addr -= 3',
            'cells[cell_addr] += 3'
        ])

        self.assertEqual(bf_to_py(bf), py)

    def test_remove_empty_loops(self):
        bf = '''
        +++[]--->>>---[]<<<+++[+-]
        '''
        py = self._to_py_code([
            'cell_addr += 3',
            'cells[cell_addr] -= 3',
            'cell_addr -= 3',
            'cells[cell_addr] += 3'
        ])

        self.assertEqual(bf_to_py(bf), py)

    def test_refuse_unbalanced_loops(self):
        bf_programs = [
            '+++]',
            '[+++',
            '[.[.].][',
            '[[.[.].]',
        ]

        for bf in bf_programs:
            with self.assertRaises(Exception) as ctx:
                bf_to_py(bf)

            self.assertEqual(str(ctx.exception), 'Unbalanced loop')


