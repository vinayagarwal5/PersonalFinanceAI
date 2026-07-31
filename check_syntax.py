#!/usr/bin/env python3
import py_compile,sys,pathlib
ok=True
for f in pathlib.Path('python').rglob('*.py'):
    try:
        py_compile.compile(str(f), doraise=True)
    except Exception as e:
        print('ERROR', f, repr(e))
        ok=False
if not ok:
    sys.exit(1)
print('All Python files compiled successfully.')
sys.exit(0)
