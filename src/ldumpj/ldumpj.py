from typing import *
import json
import re 
import argparse
from lark import Lark
from lark import Transformer_NonRecursive
import sys
from .model import LauchctlService

FORBIDDEN = [
    # keys
    "BSServiceDomains",
    "VSCODE_NLS_CONFIG",
    # key value without structure (e.g. missing =)
    "submitted job. ignore execute allowed",
    "panic on consecutive crashes (0)",
]

def fixup(malformed : str) -> str:
    """
    Pre-processes the raw launchctl output to correct common formatting issues
    and inconsistencies, making it parsable by the LALR grammar.

    This function performs several key transformations:
    1.  Corrects malformed "=>" expressions where a value is missing,
        assigning "none" as a default value.
    2.  Handles lines that end with an "=" but have no value, assigning "none".
    3.  Wraps string literals and key-value pairs in single quotes to ensure
        they are correctly identified as tokens by the grammar.
    4.  Filters out empty lines and lines containing forbidden keywords that
        are known to cause parsing issues.
    """
    def _inner(malformed_input : List[str]):
        if malformed_input[0].strip() == "":
            malformed_input = malformed_input[1:]
        
        for line in malformed_input:
            
            """
                remove empty lines
                remove BSServiceDomains as it maps to a JSON which is hard to parse
                remove VSCODE_NLS_CONFIG as         '''     ''' 
                remove malformed key=value relations with do not have a key= part
            """
            line = line.strip()
            if not line or any((line.startswith(keyword)) for keyword in FORBIDDEN):
                continue
            
            """
                only fix "=>" is it is malformed:
                    a => 
                        a => none                    

                    a => .... => c => value
                        a => none 
                        .... => none
                        c => value
            """
            
            count = line.count("=>")
            match count:
                case 1: 
                    a,b = line.split("=>",maxsplit=2)
                    b = b.strip()
                    if b == "":
                        yield "'" + a.lstrip() + " => none'"
                        continue
                    elif b == "}":
                        yield "'" + a.lstrip() + " => none'\n}"
                        continue
                case _ if count >= 2:
                    splits = line.split("=>")
                    for split in splits[:-2]:
                        yield "'" + split.lstrip() + " => none'" 
                    yield "'" + splits[-2].lstrip() + " =>" + splits[-1] + "'"
                    continue
            
            """
                fix case: properties = 
            """
            
            if line.endswith(" ="):
                idx = line.index("=")
                yield "'" + line[:idx] + "= none'"
                continue
            
            """
                add quotes to indicate values
            """
            if any(
                [
                    line.endswith("{") or line.endswith("}"),
                    line.endswith("["),
                    line.endswith("]") and not "[" in line, # case: creator = talagentd[69851]
                ]
            ):
                yield line   
            else:       
                # this also includes case: properties = 
                yield "'" + line + "'"
    return "\n".join(_inner(malformed.splitlines()))

class CustomTransformer(Transformer_NonRecursive):
    
    NUM_HEX_PATTERN = re.compile("[A-Fa-f0-9]+")
    
    def resolve_type(self,value : str):
        """
        Converts a string value to its most appropriate type (bool, None, int, or str).
        """
        match value:
            case "true": return True
            case "false": return False
            case "none": return None

        if self.NUM_HEX_PATTERN.match(value):
            try:
                if value.startswith("0x"):
                    return int(value[2:],16)
                else:
                    return int(value)
            except ValueError:
                pass
            
        return value
    
    def unqoute(self,value):
        """
        Removes single or double quotes from the start and end of a string.
        """
        return value.replace("'","" ).replace("\"","")
    
    def key(self, val : List[str]):
        """
        Processes a key token from the grammar, unquoting and stripping it.
        """
        (string,) = val
        return self.unqoute(string).strip()
    
    def header(self,value):
        """
        Processes a header token (a key-value pair that starts a new section).
        """
        (name,child) = value
        return self.unqoute(name),child
    
    def value(self, val : List[str]):
        """
        Processes a value token, parsing it into a key-value tuple if it contains
        an assignment operator ("=" or "=>"), or returning it as a simple string.
        """
        (string,) = val
        string = self.unqoute(string)
        
        if " = " in string:
            a,b = string.split(" = ")
            return (self.unqoute(a),self.resolve_type(b))
            
        if " => " in string:
            a,b = string.split(" => ")
            return (self.unqoute(a),self.resolve_type(b))
        
        return string.strip()
    
    
    def collection(self,values):
        """
        Transforms a collection of parsed values into a dictionary if all items are
        key-value pairs, otherwise returns a list.
        """
        if all(type(v) == tuple for v in values):
            return dict(values)
        else:
            return list(values)
            
    def array(self,values):
        """
        Transforms a parsed array into a dictionary, using the index as the key.
        """
        return dict((int(k),v) for k,v in values)

    
grammar = Lark(
r""" 
start: header
header: key ("="  | "=>") (container | value)

// "}"? is a hack malformed output to get to a parsing end
?container: ("{" collection "}"?) | ("[" array "]")

array: (header | value)*
collection: (header | value)*

value: ESCAPED_SINGLE_QUOTE | ESCAPED_STRING
key:   UNESCAPED_KEY | ESCAPED_STRING | SIGNED_NUMBER

UNESCAPED_KEY: /[^\'\"\{\}=]+?(?=\s(=>|=))/ 
ESCAPED_SINGLE_QUOTE: /\'[^\']+\'/ 

%import common.SIGNED_NUMBER
%import common.WS
%import common.ESCAPED_STRING
%ignore WS
"""  
,parser="lalr",start="container",transformer=CustomTransformer())

def main():
    # https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser(
        prog='ldumpj',
        description='Parses the output of `launchctl dumpstate` and `launchctl print` into json',
        epilog='Text at the bottom of help'
    )

    parser.add_argument('-i','--input',type=argparse.FileType('r'),help="Input file, defaults to stdin",default=sys.stdin)
    parser.add_argument('-o','--output',type=argparse.FileType('w'),help="Output file, defaults to stdout",default=sys.stdout)
    parser.add_argument('-p','--pretty',action="store_true",help="JSON intendation")
    parser.add_argument('-m','--model',action="store_true",help="Validate JSON with model")
    
    args = parser.parse_args()
    data = args.input.read()
    data = fixup(data)
    data = grammar.parse("{" + data + "}")
    
    if args.model:
        models = dict()
        for service_name,service_json in data.items():
            models[service_name] = LauchctlService(**service_json).model_dump()
        json.dump(models,args.output,indent=args.pretty or None)
    else:
        json.dump(data,args.output,indent=args.pretty or None)
        
        
