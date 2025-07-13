import random
import string
import parser
import obfuscator

def generate_random_func_name(min_length=6, max_length=12):
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(string.ascii_letters, k=length))

def read_code(filename):
    with open(filename, 'r') as f:
        return f.read()

def extract_replacements(code):
    var_map, func_map, param_map = parser.extract_identifiers(filename=None,code=code)
    macro_map = obfuscator.extract_macros(code)
    return {**var_map, **func_map, **param_map, **macro_map}


def write_output(code, output_file):
    if output_file:
        with open(output_file, 'w') as f:
            f.write(code)
    else:
        print(code)