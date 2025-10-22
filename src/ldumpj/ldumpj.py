from typing import *
import json
import re 
import argparse
from lark import Lark
from lark import Transformer_NonRecursive
import sys
from .core import parse_launchctl_output,fixup

def main():
    parser = argparse.ArgumentParser(
        prog='ldumpj',
        description='Parses the output of `launchctl dumpstate` and `launchctl print` into json',
        epilog='Text at the bottom of help'
    )

    parser.add_argument('-i','--input',type=argparse.FileType('r'),help="Input file, defaults to stdin",default=sys.stdin)
    parser.add_argument('-o','--output',type=argparse.FileType('w'),help="Output file, defaults to stdout",default=sys.stdout)
    parser.add_argument('-p','--pretty',action="store_true",help="JSON intendation")
    parser.add_argument('-m','--model',action="store_true",help="Validate JSON with model")
    parser.add_argument('-fix','--fix',action="store_true",help="Only output the fixup")
    
    
    args = parser.parse_args()
    raw_data = args.input.read()
    if args.fix:
        print(fixup(raw_data),file=args.output)
        exit(0)
    
    parsed = parse_launchctl_output(raw_data, validate_model=args.model)
    if args.model:
        for key in parsed:
            parsed[key] = parsed[key].model_dump()
    json.dump(parsed, args.output, indent=2 if args.pretty else None)
        
        
