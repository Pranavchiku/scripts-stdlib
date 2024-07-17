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


working_example = """
const D = new Float64Array( [ 1.0, 1.0, 1.0 ] );
const E = new Float64Array( [ 2.0, 3.0 ] );
const B = new Float64Array( [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ] );

dptts2( 'row-major', 3, 2, D, E, B, 2 ); // $ExpectType Float64Array
"""

working_ndarray_example = """
const D = new Float64Array( [ 1.0, 1.0, 1.0 ] );
const E = new Float64Array( [ 2.0, 3.0 ] );
const B = new Float64Array( [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ] );

dptts2.ndarray( 'row-major', 3, 2, D, 1, 0, E, 1, 0, B, 2, 1, 0 ); // $ExpectType Float64Array
"""

from generate_docs_types import generate_docs_types
from generate_lib import generate_lib

if __name__ == '__main__':
    generate_docs_types(routine_name, jsdoc, jsdoc_ndarray, working_example, working_ndarray_example)
    generate_lib(routine_name, jsdoc, jsdoc_ndarray)
