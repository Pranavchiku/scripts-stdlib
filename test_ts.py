num_to_english_mapping = {
    1: "a first",
    2: "a second",
    3: "a third",
    4: "a fourth",
    5: "a fifth",
    6: "a sixth",
    7: "a seventh",
    8: "an eighth",
    9: "a ninth",
    10: "a tenth",
    11: "an eleventh",
    12: "a twelfth",
    13: "a thirteenth",
    14: "a fourteenth",
    15: "a fifteenth",
    16: "a sixteenth",
    17: "a seventeenth",
    18: "an eighteenth"
}

map_arg_type_to_incorrect_str = {
    "number": [ "'5'", "true", "false", "null", "void 0", "[]", "{}", "( x: number ): number => x" ],
    "string": [ 5, "true", "false", "null", "void 0", "[]", "{}", "( x: number ): number => x" ],
    "Float64Array": [ "'5'", 5, "true", "false", "null", "void 0", "[]", "{}", "( x: number ): number => x" ],
    "Int32Array": [ "'5'", 5, "true", "false", "null", "void 0", "[]", "{}", "( x: number ): number => x" ]
}

routine_name = "dpttrf"

def get_variable_declaration( working_example, curr_var ):
    # return all except last line
    lst_declarations = working_example.split("\n")[:-2]
    # find place of '='
    lst = []
    for i in range( len( lst_declarations ) ):
        start = lst_declarations[i].find("const")
        end = lst_declarations[i].find("=")
        new_string = lst_declarations[i][start+1:end]
        if curr_var not in new_string:
            lst.append( lst_declarations[ i ] )
    return [ l for l in lst if l != "" ]


def get_working_routine_call( working_example ):
    # return last line
    string = working_example.split("\n")[-2]
    return string[:string.find(";")+1]

def get_working_routine_arguments( working_routine_call ):
    # find '(' and ')' and extract the arguments
    # remove all whitespace first
    working_routine_call = working_routine_call.replace(" ", "")
    start = working_routine_call.find("(")
    end = working_routine_call.find(")")
    arguments = working_routine_call[start+1:end]
    return arguments.split(",")


def generate_test_for_routine( routine_name, working_example, routine_arg_types, is_ndarray=False ):
    test = ""
    working_routine_call = get_working_routine_call( working_example )
    working_routine_arguments = get_working_routine_arguments( working_routine_call )
    for i in range( len( routine_arg_types ) ):
        variable_declaration = get_variable_declaration( working_example, working_routine_arguments[ i ] )
        test += "// The compiler throws an error if the function is provided " + num_to_english_mapping[i+1] + " argument which is not a " + routine_arg_types[i] + "...\n"
        test += "{\n"
        for j in range( len( variable_declaration ) ):
            test += "\t" + variable_declaration[j] + "\n"
        test += "\n"
        lst_vals = map_arg_type_to_incorrect_str[ routine_arg_types[i] ]
        for val in lst_vals:
            test += "\t" + routine_name + "( "
            for j in range( len( working_routine_arguments ) ):
                if j == i:
                    test += str(val) + ", "
                else:
                    test += working_routine_arguments[j] + ", "
            test = test[:-2] + " ); // $ExpectError\n"
        test += "}\n\n"
    if is_ndarray:
        test += "// The compiler throws an error if the `ndarray` method is provided an unsupported number of arguments...\n"
    else:
        test += "// The compiler throws an error if the function is provided an unsupported number of arguments...\n"
    test += "{\n"
    variable_declaration = get_variable_declaration( working_example, "working_routine_arguments[ i ]" )
    for i in range( len( variable_declaration ) ):
        test += "\t" + variable_declaration[i] + "\n"
    test += "\n"
    for i in range( len( routine_arg_types ) + 1 ):
        test += "\t" + routine_name + "( "
        for j in range( i ):
            if j != len( working_routine_arguments ) - 1:
                test += working_routine_arguments[j] + ", "
            else:
                test += working_routine_arguments[j] + ", " + "10" + ", "
        if ( i != 0 ):
            test = test[:-2] + " ); // $ExpectError\n"
        else:
            test = test[:-1]
            test += "); // $ExpectError\n"
    test += "}\n"
    return test

def generate_ts_tests(routine_name, working_example, routine_arg_types, working_ndarray_example, ndarray_routine_arg_types):
    test = """
/*
* @license Apache-2.0
*
* Copyright (c) 2024 The Stdlib Authors.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
"""
    test += "\n"
    test += "import " + routine_name + " = require( './index' );\n\n\n"
    test += "// TESTS //\n\n"
    test += "// The function returns a Float64Array...\n"
    test += "{\n"
    lst_working_example = working_example.split("\n")
    for i in range( 1, len( lst_working_example ) ):
        if ( lst_working_example[ i ] == ""):
            test += "\n"
            continue
        test += "\t" + lst_working_example[i] + "\n"
    test = test[:-2]
    test += "\n}\n\n"
    test += generate_test_for_routine( routine_name, working_example, routine_arg_types )
    lst_working_example_ndarray = working_ndarray_example.split("\n")
    test += "\n// Attached to main export is an `ndarray` method which returns a Float64Array...\n"
    test += "{\n"
    for i in range( 1, len( lst_working_example_ndarray ) ):
        if ( lst_working_example_ndarray[ i ] == ""):
            test += "\n"
            continue
        test += "\t" + lst_working_example_ndarray[i] + "\n"
    test = test[:-2]
    test += "\n}\n\n"
    test += generate_test_for_routine( routine_name + ".ndarray", working_ndarray_example, ndarray_routine_arg_types, True )
    return test

