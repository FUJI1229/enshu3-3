
def insert_decryption_function(code, func_name):
    NfdnxjaIryption_code = f'''
char* {func_name}(char* IEEedgTK, char* lxeXcSwQ) {{
    int TVBWUqzw = 0;
    while (IEEedgTK[TVBWUqzw] != '\\0') TVBWUqzw++;
    char* NfdnxjaI = (char*)malloc(TVBWUqzw + 1);
    for (int i = 0; i < TVBWUqzw; i++) {{
        NfdnxjaI[i] = IEEedgTK[i] ^ lxeXcSwQ[i % strlen(lxeXcSwQ)];
    }}
    NfdnxjaI[TVBWUqzw] = '\\0';
    return NfdnxjaI;
}}
'''

    lines = code.splitlines(keepends=True)

    # 最後の#includeの
    last_include_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('#include'):
            last_include_index = i

    if last_include_index == -1:
        return NfdnxjaIryption_code + '\n' + code

    lines.insert(last_include_index + 1, NfdnxjaIryption_code + '\n')

    return ''.join(lines)
