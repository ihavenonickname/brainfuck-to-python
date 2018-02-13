
def get_token(lexeme):
    if lexeme == '>':
        return {'tag': 'address', 'value': 1}

    if lexeme == '<':
        return {'tag': 'address', 'value': -1}

    if lexeme == '+':
        return {'tag': 'cell value', 'value': 1}

    if lexeme == '-':
        return {'tag': 'cell value', 'value': -1}

    if lexeme == '.':
        return {'tag': 'output'}

    if lexeme == ',':
        return {'tag': 'input'}

    if lexeme == '[':
        return {'tag': 'start loop'}

    if lexeme == ']':
        return {'tag': 'end loop'}

    return None

def build_ast(raw_bf_code):
    accumulator = []

    for token in filter(bool, map(get_token, raw_bf_code)):
        if not accumulator:
            accumulator.append(token)
        elif token['tag'] not in ['address', 'cell value']:
            accumulator.append(token)
        elif token['tag'] != accumulator[-1]['tag']:
            accumulator.append(token)
        else:
            value = token['value'] + accumulator[-1]['value']

            if value != 0:
                accumulator[-1] = {'tag': token['tag'], 'value': value}

    return accumulator

def build_py_code(ast, indentation='    '):
    level = 0
    statements = [
        'from collections import defaultdict',
        'cells = defaultdict(int)',
        'cell_addr = 0'
    ]

    for node in ast:
        if node['tag'] == 'address':
            start = indentation * level + 'cell_addr '
            middle = '+= ' if node['value'] > 0 else '-= '
            end = str(abs(node['value']))
            statements.append(start + middle + end)
        elif node['tag'] == 'cell value':
            start = indentation * level + 'cells[cell_addr] '
            middle = '+= ' if node['value'] > 0 else '-= '
            end = str(abs(node['value']))
            statements.append(start + middle + end)
        elif node['tag'] == 'output':
            statements.append(indentation * level + 'print(chr(cells[cell_addr]), end="")')
        elif node['tag'] == 'input':
            statements.append(indentation * level + 'cells[cell_addr] = ord(input())')
        elif node['tag'] == 'start loop':
            statements.append(indentation * level + 'while cells[cell_addr]:')
            level += 1
        elif node['tag'] == 'end loop':
            level -= 1

    return '\n'.join(statements)

def brainfuck_to_python(raw_bf_code):
    return build_py_code(build_ast(raw_bf_code))

def main():
    with open('test1.bf') as bf_file:
        bf_code = bf_file.read()

    py_code = brainfuck_to_python(bf_code)

    print(py_code)

if __name__ == '__main__':
    main()
