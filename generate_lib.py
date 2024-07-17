from lib_index_js import generate_lib_index_js

def generate_lib(routine_name, jsdoc, jsdoc_ndarray):
    # check if `output` directory exists, if not create it
    import os

    if not os.path.exists("output"):
        os.mkdir("output")
    
    # check if `output/lib` directory exists, if not create it

    if not os.path.exists("output/lib"):
        os.mkdir("output/lib")
    
    with open("output/lib/index.js", "w") as f:
        f.write(generate_lib_index_js(routine_name, jsdoc, jsdoc_ndarray))

