import re
import random
import string

used_names = set()

def generate_unique_random_name(length=8):
    while True:
        name = ''.join(random.choices(string.ascii_letters, k=length))
        if name not in used_names:
            used_names.add(name)
            return name

def extract_macros(code):
    macro_map = {}
    define_pattern = re.compile(r'^\s*#define\s+([a-zA-Z_][a-zA-Z0-9_]*)', re.MULTILINE)
    for match in define_pattern.finditer(code):
        macro_name = match.group(1)
        if macro_name not in macro_map:
            macro_map[macro_name] = generate_unique_random_name()
    return macro_map

def obfuscate_code(code, replace_map):
    for orig_name, obf_name in replace_map.items():
        code = re.sub(r'\b' + re.escape(orig_name) + r'\b', obf_name, code)
    return code

def xor_obfuscate_literals(code, xor_map, decrypt_func_name):
    def replacer(match):
        literal = match.group(1)
        if literal in xor_map:
            encrypted, key = xor_map[literal]
            return f'{decrypt_func_name}("{encrypted}", "{key}")'
        return f'"{literal}"'
    return re.sub(r'"([^"]+)"', replacer, code)