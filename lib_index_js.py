routine_name = "dptts2"

jsdoc = """
/**
* Solves a tridiagonal system of the form `A * X = B` using `L * D * L ** T` factorization of `A`.
*
* @param {string} order - storage layout
* @param {NonNegativeInteger} N - order of tridiagonal matrix `A`
* @param {NonNegativeInteger} NRHS - number of right hand sides i.e. number of columns in matrix `B`
* @param {Float64Array} D - array containing the diagonal elements of `A`
* @param {Float64Array} E - array containing the off-diagonal elements of `A`
* @param {Float64Array} B - input matrix
* @param {PositiveInteger} LDB - stride of the first dimension of `B` (a.k.a., leading dimension of the matrix `B`)
* @throws {TypeError} first argument must be a valid order
* @returns {Float64Array} output matrix
*
* @example
* var Float64Array = require( '@stdlib/array/float64' );
*
* var D = new Float64Array( [ 1.0, 1.0, 1.0 ] );
* var E = new Float64Array( [ 2.0, 3.0 ] );
* var B = new Float64Array( [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ] );
*
* dptts2( 'row-major', 3, 2, D, E, B, 2 );
* // B => <Float64Array>[ 11.0, 38.0, -5.0, -18.0, 2.0, 6.0 ]
*/
"""

jsdoc_ndarray = """
/**
* Solves a tridiagonal system of the form `A * X = B` using `L * D * L ** T` factorization of `A`.
*
* @param {string} order - storage layout
* @param {NonNegativeInteger} N - order of tridiagonal matrix `A`
* @param {NonNegativeInteger} NRHS - number of right hand sides i.e. number of columns in matrix `B`
* @param {Float64Array} D - array containing the diagonal elements of `A`
* @param {integer} strideD - stride length for `D`
* @param {integer} offsetD - index offset for `D`
* @param {Float64Array} E - array containing the off-diagonal elements of `A`
* @param {integer} strideE - stride length for `E`
* @param {integer} offsetE - index offset for `E`
* @param {Float64Array} B - input matrix
* @param {integer} strideB1 - stride of the first dimension of `B`
* @param {integer} strideB2 - stride of the second dimension of `B`
* @param {integer} offsetB - index offset for `B`
* @throws {TypeError} first argument must be a valid order
* @returns {Float64Array} output matrix
*
* @example
* var Float64Array = require( '@stdlib/array/float64' );
*
* var D = new Float64Array( [ 1.0, 1.0, 1.0 ] );
* var E = new Float64Array( [ 2.0, 3.0 ] );
* var B = new Float64Array( [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ] );
*
* dptts2( 'row-major', 3, 2, D, 1, 0, E, 1, 0, B, 2, 1, 0 );
* // B => <Float64Array>[ 11.0, 38.0, -5.0, -18.0, 2.0, 6.0 ]
*/
"""

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
