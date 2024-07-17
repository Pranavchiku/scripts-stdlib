def fetch_example(jsdoc):
    example = ""
    start = False
    for line in jsdoc:
        if "@example" in line:
            start = True
        if "*/" in line:
            start = False
        if start:
            example += line + "\n"
    return example


def generate_lib_index_js(routine_name, jsdoc, jsdoc_ndarray=""):
    out = """
/**
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

'use strict';
"""
    out += "\n"
    out += "/**\n"
    # take second line of jsdoc and add it to out
    jsdoc_lines = jsdoc.split("\n")
    tmp = jsdoc_lines[2][2:]
    first_word = tmp.split(" ")[0]
    # make first word singular
    # if last two letter is 'es', remove 'es'
    if first_word[-2:] == "es" and first_word != "Solves" and first_word != "Computes" and first_word != "Determines":
        new_first_word = first_word[:-2]
    elif first_word[-3] == "ies":
        new_first_word = first_word[:-3] + "y"
    else:
        new_first_word = first_word[:-1]
    # lower case the first letter
    new_first_word = new_first_word[0].lower() + new_first_word[1:]
    tmp = tmp.replace(first_word, new_first_word)
    out += "* " + "LAPACK routine to " + tmp + "\n"
    out += "*\n"
    out += "* @module @stdlib/lapack/base/" + routine_name + "\n"
    out += "*\n"
    # fetch content after `@example` from jsdoc
    out += fetch_example(jsdoc.split("\n"))
    out += "* \n"
    # fetch content after `@example` from jsdoc_ndarray
    example = fetch_example(jsdoc_ndarray.split("\n"))
    # replace routine name with routine name.ndarray
    example = example.replace(routine_name, routine_name + ".ndarray")
    out += example
    out += "*/\n"

    out += """
// MODULES //

var join = require( 'path' ).join;
var tryRequire = require( '@stdlib/utils/try-require' );
var isError = require( '@stdlib/assert/is-error' );
var main = require( './main.js' );


// MAIN //
"""
    out += "\n"
    out += "var " + routine_name + ";\n"
    out += "var tmp = tryRequire( join( __dirname, './native.js' ) );\n"
    out += "if ( isError( tmp ) ) {\n"
    out += "\t" + routine_name + " = main;\n"
    out += "} else {\n"
    out += "\t" + routine_name + " = tmp;\n"
    out += "}\n"
    out += "\n"

    out += "// EXPORTS //\n"
    out += "\n"
    out += "module.exports = " + routine_name + ";\n"
    return out
