import sys
import os
from python_micrologic import RS3_Parser as rs3parser
from python_micrologic import SLSeg_Parser as slsegparser
from preprocess_fis.block_text_tilling import *
from xml.etree.ElementTree import ParseError
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
args = sys.argv
print (args)

functions = ['slseg', 'rs3parse', 'rs3trainingdata']
function_called = args[1]
location = args[2]
variables = args[3:5]
number_of_docs_to_parse_index = 0
error = ''
try:
    list_path = os.listdir(location)
    if function_called not in functions:
        print (f'{bcolors.WARNING}Incorrect function.')
        raise
    elif function_called == functions[0]: # slseg
        print(f'{bcolors.OKGREEN}Begin parsing SLSeg...')
        # print (list_path)
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            if os.path.isdir(abs_location):
                continue
            print (bcolors.OKBLUE+abs_location)
            slsegparser.parse_slseg(abs_location, *variables)
    elif function_called == functions[1]: # rs3parse
        print(f'{bcolors.OKGREEN}Begin parsing RS3 Parsing...')
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            if os.path.isdir(abs_location):
                continue
            print('begin rs3 parsing')
            rs3parser.parse_rs3(abs_location, *variables)
    elif function_called == functions[2]: # rs3parse to dat file for training
        print(f'{bcolors.OKCYAN}Begin generating RS3 training data...')
        number_of_docs_to_parse = args[4]
        for segfile in list_path:
            if number_of_docs_to_parse_index < int(number_of_docs_to_parse):
                abs_location = os.path.join(location, segfile)
                
                print(f'{bcolors.OKCYAN}begin rs3 parsing... {abs_location}')
                try:
                    rs3parser.RS3_generate_fis_training_data(tile, split, abs_location, variables[0], number_of_docs_to_parse_index)
                    print (f'{bcolors.WARNING}FINISHED PARSING... {variables}')

                except Exception as e:
                    print (f'{bcolors.FAIL}Failed to parse {variables}, {e}')
                    continue
                
                number_of_docs_to_parse_index += 1
            else:
                break
    
except OSError as error:
    print(f"{bcolors.FAIL}Error parsing: {error}")
    sys.exit(error)
except ParseError as error:
    print (f"{bcolors.FAIL}Error parsing: {error}")
    pass
