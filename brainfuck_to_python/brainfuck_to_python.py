def is_balanced(raw_bf_code):
    balance = 0

    for char in raw_bf_code:
        if char == ']':
            if balance == 0:
                return False

            balance -= 1
        elif char == '[':
            balance += 1

    return balance == 0

def build_ast(raw_bf_code):
    tokens = [{'tag': ''}]

    for lexeme in raw_bf_code:
        if lexeme == '>':
            if tokens[-1]['tag'] == 'address':
                if tokens[-1]['value'] == -1:
                    del tokens[-1]
                else:
                    tokens[-1]['value'] += 1
            else:
                tokens.append({'tag': 'address', 'value': 1})

        elif lexeme == '<':
            if tokens[-1]['tag'] == 'address':
                if tokens[-1]['value'] == 1:
                    del tokens[-1]
                else:
                    tokens[-1]['value'] -= 1
            else:
                tokens.append({'tag': 'address', 'value': -1})

        elif lexeme == '+':
            if tokens[-1]['tag'] == 'cell value':
                if tokens[-1]['value'] == -1:
                    del tokens[-1]
                else:
                    tokens[-1]['value'] += 1
            else:
                tokens.append({'tag': 'cell value', 'value': 1})

        elif lexeme == '-':
            if tokens[-1]['tag'] == 'cell value':
                if tokens[-1]['value'] == 1:
                    del tokens[-1]
                else:
                    tokens[-1]['value'] -= 1
            else:
                tokens.append({'tag': 'cell value', 'value': -1})

        elif lexeme == '.':
            tokens.append({'tag': 'output'})

        elif lexeme == ',':
            tokens.append({'tag': 'input'})

        elif lexeme == '[':
            tokens.append({'tag': 'start loop'})

        elif lexeme == ']':
            if tokens[-1]['tag'] == 'start loop':
                del tokens[-1]
            else:
                tokens.append({'tag': 'end loop'})

    return tokens[1:]

def clear_cell(ast):
    new_ast = []
    i = 0

    while i < len(ast):
        if ast[i]['tag'] == 'start loop' and ast[i + 1]['tag'] == 'cell value' and ast[i + 1]['value'] == -1 and ast[i + 2]['tag'] == 'end loop':
            new_ast.append({'tag': 'clear'})
            i += 3
        else:
            new_ast.append(ast[i])
            i += 1

    return new_ast

def emit_py_code(ast, indentation='    '):
    def incrementer(n):
        sign = '+' if n > 0 else '-'
        return sign + '= ' + str(abs(n))

    level = 0
    statements = [
        'from collections import defaultdict',
        'cells = defaultdict(int)',
        'cell_addr = 0'
    ]

    for node in ast:
        if node['tag'] == 'address':
            n = node['value']
            statements.append(indentation * level + 'cell_addr ' + incrementer(n))
        elif node['tag'] == 'cell value':
            n = node['value']
            statements.append(indentation * level + 'cells[cell_addr] ' + incrementer(n))
        elif node['tag'] == 'output':
            statements.append(indentation * level + 'print(chr(cells[cell_addr]), end="")')
        elif node['tag'] == 'input':
            statements.append(indentation * level + 'cells[cell_addr] = ord(input())')
        elif node['tag'] == 'start loop':
            statements.append(indentation * level + 'while cells[cell_addr]:')
            level += 1
        elif node['tag'] == 'end loop':
            level -= 1
        elif node['tag'] == 'clear':
            statements.append(indentation * level + 'cells[cell_addr] = 0')

    return '\n'.join(statements)

def brainfuck_to_python(raw_bf_code):
    if not is_balanced(raw_bf_code):
        raise Exception('Unbalanced loop')

    return emit_py_code(build_ast(raw_bf_code))

def main():
    with open('test1.bf') as bf_file:
        bf_code = bf_file.read()

    py_code = brainfuck_to_python(bf_code)

    print(py_code)

if __name__ == '__main__':
    main()
