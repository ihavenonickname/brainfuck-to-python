def optimize(ast, merge_equivalent_instructions=True, remove_empty_loops=True, clear_cells=True):
    new_ast = [{'tag': ''}]

    def can_merge(ast_index):
        return merge_equivalent_instructions and (
            'value' in ast[ast_index] and
            'value' in new_ast[-1] and
            ast[ast_index]['tag'] == new_ast[-1]['tag']
        )

    def can_remove_loop(ast_index):
        return remove_empty_loops and (
            ast[ast_index]['tag'] == 'end loop' and
            new_ast[-1]['tag'] == 'start loop'
        )

    def is_clean_pattern(ast_index):
        return clear_cells and (
            ast[ast_index    ]['tag'  ] == 'start loop' and
            ast[ast_index + 1]['tag'  ] == 'cell value' and
            ast[ast_index + 1]['value'] == -1           and
            ast[ast_index + 2]['tag'  ] == 'end loop'
        )

    i = 0

    while i < len(ast):
        if can_merge(i):
            if new_ast[-1]['value'] + ast[i]['value'] == 0:
                del new_ast[-1]
            else:
                new_ast[-1]['value'] += ast[i]['value']
            i += 1
        elif can_remove_loop(i):
            del new_ast[-1]
            i += 1
        elif is_clean_pattern(i):
            new_ast.append({'tag': 'clear'})
            i += 3
        else:
            new_ast.append(ast[i])
            i += 1

    return new_ast[1:]
