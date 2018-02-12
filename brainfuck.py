def brainfuck_to_python(tokens, indentation='    '):
    level = 0
    statements = [
        'from collections import defaultdict',
        'cells = defaultdict(int)',
        'cell_addr = 0'
    ]

    for token in tokens:
        if token == '>':
            statements.append(indentation * level + 'cell_addr += 1')
        elif token == '<':
            statements.append(indentation * level + 'cell_addr -= 1')
        elif token == '+':
            statements.append(indentation * level + 'cells[cell_addr] += 1')
        elif token == '-':
            statements.append(indentation * level + 'cells[cell_addr] -= 1')
        elif token == '.':
            statements.append(indentation * level + 'print(chr(cells[cell_addr]), end="")')
        elif token == ',':
            statements.append(indentation * level + 'cells[cell_addr] = ord(input())')
        elif token == '[':
            statements.append(indentation * level + 'while cells[cell_addr]:')
            level += 1
        elif token == ']':
            level -= 1

    return '\n'.join(statements)

def main():
    with open('test1.bf') as bf_file:
        bf_code = bf_file.read()

    py_code = brainfuck_to_python(bf_code)

    print(py_code)

if __name__ == '__main__':
    main()
