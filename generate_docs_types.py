# routine_name = "dlaset"

# jsdoc = """
# /**
# * Initializes an `M` by `N` matrix `A` to `beta` on the diagonal and `alpha` on the off-diagonals.
# *
# * @param {string} order - storage layout
# * @param {string} uplo - specifies whether the upper or lower triangular part of matrix `A` is supplied
# * @param {NonNegativeInteger} M - number of rows in matrix `A`
# * @param {NonNegativeInteger} N - number of columns in matrix `A`
# * @param {number} alpha - scalar constant to which off-diagonal elements are set
# * @param {number} beta - scalar constant to which diagonal elements are set
# * @param {Float64Array} A - input matrix
# * @param {PositiveInteger} LDA - stride of the first dimension of `A` (a.k.a., leading dimension of the matrix `A`)
# * @throws {TypeError} first argument must be a valid order
# * @returns {Float64Array} `A`
# *
# * @example
# * var Float64Array = require( '@stdlib/array/float64' );
# *
# * var A = new Float64Array( [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] );
# *
# * dlaset( 'row-major', 'lower', 3, 3, 3.1, 3.7, A, 3 );
# * // A => <Float64Array>[ 3.7, 0.0, 0.0, 3.1, 3.7, 0.0, 3.1, 3.1, 3.7 ]
# */
# """

# jsdoc_ndarray = """
# /**
# * Initializes an `M` by `N` matrix `A` to `beta` on the diagonal and `alpha` on the off-diagonals using alternative indexing semantics.
# *
# * @param {string} order - storage layout
# * @param {string} uplo - specifies whether the upper or lower triangular part of matrix `A` is supplied
# * @param {NonNegativeInteger} M - number of rows in matrix `A`
# * @param {NonNegativeInteger} N - number of columns in matrix `A`
# * @param {number} alpha - scalar constant to which off-diagonal elements are set
# * @param {number} beta - scalar constant to which diagonal elements are set
# * @param {Float64Array} A - input matrix
# * @param {integer} strideA1 - stride of the first dimension of `A`
# * @param {integer} strideA2 - stride of the second dimension of `A`
# * @param {NonNegativeInteger} offsetA - starting index for `A`
# * @throws {TypeError} first argument must be a valid order
# * @returns {Float64Array} `A`
# *
# * @example
# * var Float64Array = require( '@stdlib/array/float64' );
# *
# * var A = new Float64Array( [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] );
# *
# * dlaset( 'row-major', 'lower', 3, 3, 3.1, 3.7, A, 3, 1, 1 );
# * // A => <Float64Array>[ 0.0, 3.7, 0.0, 0.0, 3.1, 3.7, 0.0, 3.1, 3.1, 3.7 ]
# */
# """

# working_example = """
# const A = new Float64Array( [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] );

# dlaset( 'row-major', 'lower', 3, 3, 3.1, 3.7, A, 3 ); // $ExpectType Float64Array
# """

# working_ndarray_example = """
# const A = new Float64Array( [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] );

# dlaset.ndarray( 'row-major', 'lower', 3, 3, 3.1, 3.7, A, 3, 1, 0 ); // $ExpectType Float64Array
# """

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


def generate_docs_types(routine_name, jsdoc, jsdoc_ndarray, working_example, working_ndarray_example):
    routine_arg_types = get_routine_arg_types(jsdoc.split('\n'))
    ndarray_routine_arg_types = get_routine_arg_types(jsdoc_ndarray.split('\n'))

    import os
    if not os.path.exists("output"):
        os.mkdir("output")

    if not os.path.exists("output/docs"):
        os.mkdir("output/docs")

    if not os.path.exists("output/docs/types"):
        os.mkdir("output/docs/types")

    with open("output/docs/types/index.d.ts", "w") as f:
        f.write(generate_ts_doc_for_interface_routine(routine_name, jsdoc, jsdoc_ndarray))
    
    with open("output/docs/types/test.ts", "w") as f:
        f.write(generate_ts_tests(routine_name, working_example, routine_arg_types, working_ndarray_example, ndarray_routine_arg_types))


# if __name__ == "__main__":
#     generate_index_d_ts(routine_name, jsdoc, jsdoc_ndarray, working_example, working_ndarray_example)
