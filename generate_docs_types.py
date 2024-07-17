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
