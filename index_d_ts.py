mapping_type_to_ts_type = {
    'string': 'string',
    'NonNegativeInteger': 'number',
    'Float64Array': 'Float64Array',
    'PositiveInteger': 'number',
    'number': 'number',
    'Int32Array': 'Int32Array',
    'integer': 'number'
}

def get_ts_type(var_name, jsdoc_type):
    if ( var_name == 'order' ):
        return 'Layout'

    if ( var_name == 'uplo' ):
        return 'MatrixTriangle'

    if ( var_name == 'side' ):
        return 'OperationSide'

    if ( 'trans' in var_name ):
        return 'TransposeOperation'

    if ( 'diag' in var_name ):
        return 'DiagonalType'

    return mapping_type_to_ts_type[jsdoc_type]


def generate_tsdoc_for_index_d_ts(jsdoc, is_ndarray, routine_name):
    # iterate over each line in jsdoc
    # if it is @private, remove the line
    # if it contains @param, search for `{` and `}` and remove all inbetween them
    # including `{` and `}`
    # if it contains @returns, search for `{` and `}` and remove all inbetween them
    # including `{` and `}`

    # code begins
    new_jsdoc = ""
    for line in jsdoc:
        if ('@private' in line) or ('@throws' in line):
            continue
        if ('@param' in line) or ('@returns' in line):
            start = line.find(' {')
            end = line.find('}')
            line = line[:start] + line[end+1:]
        if (routine_name in line) and is_ndarray:
            # change routine name to `routine_name.ndarray`
            line = line.replace(routine_name, routine_name + '.ndarray')
        if '*/' in line:
            new_jsdoc += '\t' + line
        else:
            new_jsdoc += '\t' + line + '\n'
    
    if is_ndarray:
        new_jsdoc += '\t' + "ndarray( "
    else:
        new_jsdoc += '\t' + "( "
    
    for line in jsdoc:
        if ('@param' in line):
            start = line.find('{')
            end = line.find('}')
            hyphen_loc = line.find('-')
            var_name = line[end+1:hyphen_loc].strip()
            ts_type = get_ts_type(var_name, line[start+1:end].strip())
            new_jsdoc += var_name + ": " + ts_type + ", "
        if ('@returns' in line):
            start = line.find('{')
            end = line.find('}')
            hyphen_loc = line.find('-')
            var_name = line[end+1:hyphen_loc].strip()
            ts_type = get_ts_type(var_name, line[start+1:end].strip())
            new_jsdoc = new_jsdoc[:-2] + " "
            new_jsdoc += "): " + ts_type + ";"

    return new_jsdoc
# test the function

def generate_tsdoc_for_lower_part_of_index_d_ts(jsdoc, is_ndarray, routine_name):
    if not is_ndarray:
        # new jsdoc is same as jsdoc just strip '\t' from the beginning
        # and remove last line
        new_jsdoc = ""
        for line in jsdoc:
            if line == jsdoc[-1]:
                continue
            if line == jsdoc[-2]:
                new_jsdoc += '*\n'
                continue
            new_jsdoc += line.replace('\t','') + '\n'
        return new_jsdoc
    # ndarray
    # return jsdoc as is from `@example` to `*/`
    new_jsdoc = ""
    start = False
    for line in jsdoc:
        if ('@example' in line):
            start = True
        if routine_name in line:
            # change routine name to `routine_name.ndarray`
            line = line.replace(routine_name, routine_name + '.ndarray')
        if start:
            new_jsdoc += line.replace('\t','') + '\n'
    # remove last line
    new_jsdoc = new_jsdoc[:-1]
    new_jsdoc += "declare var " + routine_name + ": Routine;\n"
    new_jsdoc += "\n\n"
    new_jsdoc += "// EXPORTS //\n\n"
    new_jsdoc += "export = " + routine_name + ";"
    return new_jsdoc

def generate_ts_doc_for_interface_routine(routine_name, jsdoc, jsdoc_ndarray = ""):
    tsdoc = """
/**
* Interface describing `""" + routine_name + """`.
*/
interface Routine {"""
    tsdoc_normal = generate_tsdoc_for_index_d_ts(jsdoc.split('\n'), False, routine_name)
    tsdoc += tsdoc_normal
    tsdoc += '\n'
    if ( len(jsdoc_ndarray) != 0 ):
        tsdoc_ndarray = generate_tsdoc_for_index_d_ts(jsdoc_ndarray.split('\n'), True, routine_name)
        tsdoc += tsdoc_ndarray
        tsdoc += '\n'
    tsdoc += "}"

    tsdoc_normal = generate_tsdoc_for_lower_part_of_index_d_ts(tsdoc_normal.split('\n'), False, routine_name)
    if ( len(jsdoc_ndarray) != 0 ):
        tsdoc_ndarray = generate_tsdoc_for_lower_part_of_index_d_ts(jsdoc_ndarray.split('\n'), True, routine_name)
        tsdoc += '\n' + tsdoc_normal + tsdoc_ndarray
    else:
        tsdoc += '\n' + tsdoc_normal
    return tsdoc
