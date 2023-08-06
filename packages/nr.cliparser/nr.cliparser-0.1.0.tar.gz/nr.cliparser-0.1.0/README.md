# `nr.cliparser`

&ndash; Extensible CLI parser.

*Work in progress*

__Example__

```python
import nr.cliparser

parser = nr.cliparser.Parser()
parser.argument('-h', nargs=0, help='Show this help.')
parser.argument('script', nargs='?', help='A script to run.')
parser.argument('argv', nargs='...', help='Arguments for the script.')

install = parser.subparser('--install', help='Install a packge.')
install.argument('ref', nargs='?', multiple=True, help='A package reference.')
install.argument('-e', metavar='ref', help='A package reference to install editable.', multiple=True)
install.argument('-g', nargs=0, help='Install globally.')
install.argument('-r', nargs=0, help='Install into root.')

args = parser.parse()
if args['h']:
  parser.print_help()
  exit()

print(args)
```

```
$ python3 example.py -h
usage: example -h  [script] ... --install [ [ref] -e <ref> -g  -r ] 

-h                 Show this help.                                    
[script]           A script to run.                                   
...                Arguments for the script.                          
--install [ ... ]  Install a packge.                                  
  [ref]            A package reference.                               
  -e <ref>         A package reference to install editable.           
  -g               Install globally.                                  
  -r               Install into root.                                 

$ python3 example.py --install -e scope@package  
{'install': {'e': ['scope@package'], 'ref': [], 'g': False, 'r': False}, 'h': False, 'script': None, 'argv': []}
```

### Changes

#### v0.1.0

* Initial release
