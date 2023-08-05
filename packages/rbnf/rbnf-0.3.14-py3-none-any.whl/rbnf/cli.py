from rbnf.bootstrap.rbnf import build_language, Language
from rbnf.color import Blue, LightBlue, Purple, Yellow
import rbnf.zero as ze
from wisepy.talking import Talking
from Redy.Tools.PathLib import Path
import os.path
talking = Talking()


@talking
def cc(filename: 'input source file',
       output:
       'output file name. default to be replacing input file\'s suffix with ".py"' = None,
       name: 'name of language' = 'unname'):
    """
    rbnf source code compiler.
    """

    lang = Language(name)

    with Path(filename).open('r') as fr:
        build_language(fr.read(), lang, filename)

    if not output:
        base, _ = os.path.splitext(filename)

        output = base + '.py'
    lang.dump(output)


@talking
def run(filename: 'python file generated by `rbnf` command, or rbnf sour file',
        opt: 'optimize switch' = False):
    """
    You can apply immediate tests on your parser.
    P.S: use `--opt` option takes longer starting time.
    """
    from rbnf.easy import build_parser
    import importlib.util
    import traceback
    full_path = Path(filename)
    base, ext = os.path.splitext(str(full_path))
    full_path_str = str(full_path)

    if not ext:
        if full_path.into('.py').exists():
            full_path_str = base + '.py'
        elif Path(base).into('.rbnf'):
            full_path_str = base + '.rbnf'

    if full_path_str[-3:].lower() != '.py':
        with Path(full_path_str).open('r') as fr:
            ze_exp = ze.compile(fr.read(), filename=full_path_str)
            lang = ze_exp.lang

    else:
        spec = importlib.util.spec_from_file_location("runbnf", full_path_str)

        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            lang = next(each for each in mod.__dict__.values()
                        if isinstance(each, Language))
        except StopIteration:
            raise NameError("Found no language in {}".format(full_path_str))

    parse = build_parser(lang, opt=bool(opt))
    namespace = {}

    print(Purple('type `:i` to switch between python mode and parsing mode.'))
    print(Purple('The last result of parsing is stored as symbol `res`.'))
    while True:

        inp = input('runbnf> ')
        if not inp.strip():
            continue
        elif inp.strip() == 'exit':
            break

        if inp.strip() == ':i':
            while True:
                inp = input('python> ')

                if inp.strip() == ':i':
                    break
                try:
                    try:
                        res = eval(inp, namespace)
                        if res is not None:
                            print(res)

                        namespace['_'] = res
                    except SyntaxError:
                        exec(inp, namespace)
                except Exception:
                    traceback.print_exc()
        else:
            res = namespace['res'] = parse(inp)
            print(
                LightBlue(
                    'parsed result = res: ResultDescription{result, tokens, state}'
                ))
            print(res.result)


def main():
    talking.on()
