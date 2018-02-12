class Indentable():
    def __init__(self):
        self.level = 0

    def _indentation(self):
        return '    ' * self.level

class Output(Indentable):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self._indentation() + 'print(chr(cells[cell_addr]), end="")'

class Input(Indentable):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self._indentation() + 'cells[cell_addr] = ord(input())'

class AddressChanger(Indentable):
    def __init__(self, diff):
        super().__init__()
        self._diff = diff

    def __str__(self):
        s = f'+= {self._diff}' if self._diff > 0 else f'-= {abs(self._diff)}'

        return self._indentation() + f'cell_addr {s}'

class CellValueChanger(Indentable):
    def __init__(self, diff):
        super().__init__()
        self._diff = diff

    def __str__(self):
        s = f'+= {self._diff}' if self._diff > 0 else f'-= {abs(self._diff)}'

        return self._indentation() + f'cells[cell_addr] {s}'

class Loop(Indentable):
    def __init__(self):
        super().__init__()
        self._commands = []

    def add(self, command):
        self._commands.append(command)

    def __bool__(self):
        return bool(self._commands)

    def __str__(self):
        s = self._indentation() + 'while cells[cell_addr] != 0:'

        for command in self._commands:
            command.level = self.level + 1
            s += '\n' + str(command)

        return s

def parse_regular_command(token):
    if token == '>':
        return AddressChanger(1)

    if token == '<':
        return AddressChanger(-1)

    if token == '+':
        return CellValueChanger(1)

    if token == '-':
        return CellValueChanger(-1)

    if token == '.':
        return Output()

    if token == ',':
        return Input()

    return None

def parse_loop(tokens):
    loop = Loop()

    while True:
        token = tokens.pop(0)

        if token == ']':
            break

        if token == '[':
            loop.add(parse_loop(tokens))
        else:
            loop.add(parse_regular_command(token))

    return loop

def parse(tokens):
    semantic_stack = []

    while tokens:
        token = tokens.pop(0)

        if token == '[':
            loop = parse_loop(tokens)

            if loop:
                semantic_stack.append(tokens)
        else:
            command = parse_regular_command(token)

            if command:
                semantic_stack.append(command)

    return semantic_stack

def generate_code(ast):
    boilerplate = '''from collections import defaultdict
cells = defaultdict(int)
cell_addr = 0
'''

    return boilerplate + '\n'.join(str(node) for node in ast)

def tokenize(raw_code):
    return list(op for op in raw_code if op in '[]+-<>.,')

def brainfuck_to_python(bf_raw_code):
    tokens = tokenize(bf_raw_code)
    ast = parse(tokens)
    code = generate_code(ast)

    return code

def main():
    with open('test1.bf') as bf_file:
        bf_code = bf_file.read()

    py_code = brainfuck_to_python(bf_code)

    print(py_code)

if __name__ == '__main__':
    main()
