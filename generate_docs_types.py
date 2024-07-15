routine_name = "dlacpy"

jsdoc = """
/**
* Copies all or part of a two-dimensional matrix `A` to another matrix `B`.
*
* @param {string} order - storage layout of `A` and `B`
* @param {string} uplo - specifies whether the upper or lower triangular part of matrix `A` is supplied
* @param {NonNegativeInteger} M - number of rows in matrix `A`
* @param {NonNegativeInteger} N - number of columns in matrix `A`
* @param {Float64Array} A - input matrix
* @param {PositiveInteger} LDA - stride of the first dimension of `A` (a.k.a., leading dimension of the matrix `A`)
* @param {Float64Array} B - destination matrix
* @param {PositiveInteger} LDB - stride of the first dimension of `B` (a.k.a., leading dimension of the matrix `B`)
* @throws {TypeError} first argument must be a valid order
* @returns {Float64Array} `B`
*
* @example
* var Float64Array = require( '@stdlib/array/float64' );
*
* var A = new Float64Array( [ 1.0, 2.0, 3.0, 4.0 ] );
* var B = new Float64Array( 4 );
*
* dlacpy( 'row-major', 'all', 2, 2, A, 2, B, 2 );
* // B => <Float64Array>[ 1.0, 2.0, 3.0, 4.0 ]
*/
"""

jsdoc_ndarray = """
/**
* Copies all or part of a two-dimensional matrix `A` to another matrix `B` using alternative indexing semantics.
*
* @param {string} order - storage layout of `A` and `B`
* @param {string} uplo - specifies whether the upper or lower triangular part of matrix `A` is supplied
* @param {NonNegativeInteger} M - number of rows in matrix `A`
* @param {NonNegativeInteger} N - number of columns in matrix `A`
* @param {Float64Array} A - input matrix
* @param {integer} strideA1 - stride of the first dimension of `A`
* @param {integer} strideA2 - stride of the second dimension of `A`
* @param {PositiveInteger} offsetA - starting index for `A`
* @param {Float64Array} B - destination matrix
* @param {integer} strideB1 - stride of the first dimension of `B`
* @param {integer} strideB2 - stride of the second dimension of `B`
* @param {PositiveInteger} offsetB - starting index for `B`
* @throws {TypeError} first argument must be a valid order
* @returns {Float64Array} `B`
*
* @example
* var Float64Array = require( '@stdlib/array/float64' );
*
* var A = new Float64Array( [ 0.0, 1.0, 2.0, 3.0, 4.0 ] );
* var B = new Float64Array( [ 0.0, 0.0, 11.0, 312.0, 53.0, 412.0 ] );
*
* dlacpy( 'row-major', 'all', 2, 2, A, 2, 1, 1, B, 2, 1, 2 );
* // B => <Float64Array>[ 0.0, 0.0, 1.0, 2.0, 3.0, 4.0 ]
*/
"""

working_example = """
const A = new Float64Array( [ 1.0, 2.0, 3.0, 4.0 ] );
const B = new Float64Array( 4 );

dlacpy( 'row-major', 'all', 2, 2, A, 2, B, 2 ); // $ExpectType Float64Array
"""

working_ndarray_example = """
const A = new Float64Array( [ 1.0, 2.0, 3.0, 4.0 ] );
const B = new Float64Array( 4 );

dlacpy.ndarray( 'row-major', 'all', 2, 2, A, 2, 1, 0, B, 2, 1,0 ); // $ExpectType Float64Array
"""

from index_d_ts import generate_ts_doc_for_interface_routine
from test_ts import generate_ts_tests

mapping_type_to_ts_type = {
    'string': 'string',
    'NonNegativeInteger': 'number',
    'Float64Array': 'Float64Array',
    'PositiveInteger': 'number',
    'number': 'number',
    'Int32Array': 'Int32Array',
    'integer': 'number'
}

def get_routine_arg_types(jsdoc):
    routine_arg_types = []
    for line in jsdoc:
        if "@param" in line:
            start = line.find('{')
            end = line.find('}')
            routine_arg_types.append(mapping_type_to_ts_type[line[start+1:end]])
    return routine_arg_types


def generate_index_d_ts(routine_name, jsdoc, jsdoc_ndarray, working_example, working_ndarray_example):
    routine_arg_types = get_routine_arg_types(jsdoc.split('\n'))
    ndarray_routine_arg_types = get_routine_arg_types(jsdoc_ndarray.split('\n'))

    import os
    os.mkdir("output")

    with open("output/index.d.ts", "w") as f:
        f.write(generate_ts_doc_for_interface_routine(routine_name, jsdoc, jsdoc_ndarray))
    
    with open("output/test.ts", "w") as f:
        f.write(generate_ts_tests(routine_name, working_example, routine_arg_types, working_ndarray_example, ndarray_routine_arg_types))


if __name__ == "__main__":
    generate_index_d_ts(routine_name, jsdoc, jsdoc_ndarray, working_example, working_ndarray_example)
