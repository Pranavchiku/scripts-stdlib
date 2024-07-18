from test_test_js import generate_test_js

def generate_test( routine_name ):
    import os
    if not os.path.exists( "output" ):
        os.mkdir( "output" )
    
    if not os.path.exists( "output/test" ):
        os.mkdir( "output/test" )

    with open( "output/test/test.js", "w" ) as f:
        f.write( generate_test_js( routine_name ) )
