from typing import *
import json
import re 
import argparse
from lark import Lark
from lark import Transformer_NonRecursive
import sys

def fixup(malformed : str) -> str:
    """ 
        This fixes 1) malformed entries and add qoutes to ease parsing
        
        1)
            "graphData" => 				"client" => "com.apple.modelcatalogd"
            
        or

            PRODUCT_INFO_FILTER_DISABLE => 
		    XPC_SERVICE_NAME => com.apple.remoted
        2)
            creator = talagentd[69851]
                'creator = talagentd[69851]'
                
            but 
            
            creator = {
            }
            
            will not be enclosed with quotes

    """
    def _inner(malformed_input : List[str]):
        if malformed_input[0].strip() == "":
            malformed_input = malformed_input[1:]
        
        for line in malformed_input:
            
            """
                remove empty lines
                remove BSServiceDomains as it maps to a JSON which is hard to parse
            """
            line = line.strip()
            if line == "" or "BSServiceDomains" in line:
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
    
    # array = list 
    # collection = list
    
    NUM_HEX_PATTERN = re.compile("[A-Fa-f0-9]+")
    
    def resolve_type(self,value : str):
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
        return value.replace("'","").replace("\"","")
    
    def key(self, val : List[str]):
        (string,) = val
        return self.unqoute(string).strip()
    
    def header(self,value):
        (name,child) = value
        return self.unqoute(name),child
    
    def value(self, val : List[str]):
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
        if all(type(v) == tuple for v in values):
            return dict(values)
        else:
            return list(values)
            
    def array(self,values):
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
        prog='dumpstate2json',
        description='Parses the output of `launchctl dumpstate` and `launchctl print` into json',
        epilog='Text at the bottom of help'
    )

    parser.add_argument('-i','--input',type=argparse.FileType('r'),help="Input file, defaults to stdin",default=sys.stdin)
    parser.add_argument('-o','--output',type=argparse.FileType('w'),help="Output file, defaults to stdout",default=sys.stdout)
    parser.add_argument('-p','--pretty',action="store_true",help="JSON intendation")
    
    args = parser.parse_args()
    data = args.input.read()
    data = fixup(data)
    data = grammar.parse("{" + data + "}")
    
    json.dump(data,args.output,indent=args.pretty or None)