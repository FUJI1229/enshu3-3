import parser
import obfuscator 
import encrypt
import util

def main():
    args = parser.parse_arguments()
    filename = args.input
    code = util.read_code(filename)
    if args.xor_pairs:
        # XOR暗号化の適用と復号関数の挿入
        code = encrypt.apply_xor_encryption(code, args.xor_pairs)
    # 変数・関数・マクロの抽出
    replace_map = util.extract_replacements(code)
    #　ランダム置換
    obfuscated_code = obfuscator.obfuscate_code(code, replace_map)
    util.write_output(obfuscated_code, args.output)
    
if __name__ == '__main__':
    main()
