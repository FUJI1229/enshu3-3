import argparse
from clang import cindex
from obfuscator import generate_unique_random_name

# 例外を除外（これもう少しマシになりそうだけどあって困らないか）
exclude_names = {
    'int', 'char', 'float', 'double', 'void', 'return',
    'if', 'else', 'while', 'for', 'break', 'continue',
    'switch', 'case', 'default', 'struct', 'typedef',
    'sizeof', 'main', 'printf', 'fprintf', 'scanf',
    'stdin', 'stdout', 'stderr', 'malloc', 'free', 'exit',
    'fopen', 'fclose', 'fwrite', 'fread', 'snprintf',
    'perror', 'strcmp', 'strcpy','strlen', 'strtol',
    'GetFileAttributes', 'FindFirstFile', 'FindNextFile', 'FindClose',
    'RegOpenKeyEx', 'RegSetValueEx','RegCloseKey'
}

def extract_identifiers(filename=None, code=None, clang_lib_path='/usr/lib/llvm-14/lib/libclang.so'):
    if not filename and not code:
        raise ValueError('pls type filename or code explicitly')

    cindex.Config.set_library_file(clang_lib_path)
    index = cindex.Index.create()

    if filename and code is None:
        # ファイル解析
        tu = index.parse(filename)
    else:
        # 文字列解析(一回ファイルに書き出してから解析することになる)
        fake_filename = filename if filename else 'tmp.c'
        tu = index.parse(fake_filename, args=['-std=c11'], unsaved_files=[(fake_filename, code)], options=0)

    var_map = {}
    func_map = {}
    param_map = {}

    def obfuscate_name(cursor):
        if cursor.spelling in exclude_names or not cursor.spelling:
            return

        if cursor.kind == cindex.CursorKind.VAR_DECL:
            if cursor.spelling not in var_map:
                var_map[cursor.spelling] = generate_unique_random_name()
        elif cursor.kind == cindex.CursorKind.FUNCTION_DECL:
            if cursor.spelling not in func_map:
                func_map[cursor.spelling] = generate_unique_random_name()
        elif cursor.kind == cindex.CursorKind.PARM_DECL:
            if cursor.spelling not in param_map:
                param_map[cursor.spelling] = generate_unique_random_name()

    def walk_ast(cursor):
        obfuscate_name(cursor)
        for c in cursor.get_children():
            walk_ast(c)
    walk_ast(tu.cursor)
    return var_map, func_map, param_map

def parse_arguments():
    parser = argparse.ArgumentParser(description="An obfuscator for C programs")
    parser.add_argument('-i', '--input', required=True, help='Input C source file')
    parser.add_argument('-o', '--output', help='Output file for obfuscated code')
    parser.add_argument(
        '--xor-pairs',
        nargs='*',
        type=str,
        metavar=('STRING', 'KEY(STRING)'),
        help='Pairs of string and XOR key: str1 key1 str2 key2 ...'
    )
    return parser.parse_args()
