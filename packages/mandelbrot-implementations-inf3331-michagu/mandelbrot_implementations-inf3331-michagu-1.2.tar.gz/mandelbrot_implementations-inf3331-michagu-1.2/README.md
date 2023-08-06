# INF3331-michagu - Assignment 4

As we where to create a user interface, I've made the decision that this is the execution point for
every implementation. 
-----------------------------------------------------------------------------------------------------------
### Execution of mandelbrot.py
As you would see if you run the script with the -h flag, the scripts is ran like the following:

usage: mandelbrot.py [-h] [-m MANDELBROT_IMPLEMENTATION] [-c COLOR_SCALE] [-t MAX_ESCAPE_TIME]
                     minX maxX minY maxY nX nY filename

positional arguments:
  minX                  Min value for x-axes
  maxX                  Max value for x-axes
  minY                  Min value for y-axes
  maxY                  Max value for y-axes
  nX                    Resolution for the x-axes
  nY                    Resolution for the y-axes
  filename              Filename for the Mandelbrot set

optional arguments:
  -h, --help            show this help message and exit
  -m MANDELBROT_IMPLEMENTATION, --mandelbrot_implementation MANDELBROT_IMPLEMENTATION
                        1.Pure Python | 2.Numpy | 3.Numba | 4.Cython -
                        defaults to Cython
  -c COLOR_SCALE, --color_scale COLOR_SCALE
                        1.jet_r | 2.magma | 3.gnuplot2 - defaults to jet_r
  -t MAX_ESCAPE_TIME, --max_escape_time MAX_ESCAPE_TIME
                        Max escape time, defaults to 1000
-----------------------------------------------------------------------------------------------------------
### Test execution
The test framework used is unittest.
- To run the test: python test_complex.py -v
- The -v flag is just to get a verbose output.
-----------------------------------------------------------------------------------------------------------
### Package
I've chosen not to include the artifacts you get when generating a package, but with the 
included setup.py script you can generate the package with `python setup.py sdist bdist_wheel`

I've also distributed my package on Pypi so you could find it with `pip search michagu` and install it
with `pip install mandelbrot-inf3331-michagu` 
-----------------------------------------------------------------------------------------------------------