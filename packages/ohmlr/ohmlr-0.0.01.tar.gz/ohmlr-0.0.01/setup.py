# from numpy.distutils.core import Extension
# from setuptools import find_packages

# libraries = ['gomp', 'lapack']  # + lapack_opt_info['libraries']
# library_dirs = ['/usr/lib', '/usr/local/lib']  # lapack_opt_info['library_dirs']

# fortran_module = Extension(
#     name='fortran_module',
#     sources=['./fem/fortran_module.f90', './fem/fortran_module.pyf'],
#     libraries=libraries,
#     # library_dirs=library_dirs,
#     extra_f90_compile_args=['-fopenmp', '-lgomp'])

# gnu (gcc, g++, g77, gfortran): -fopenmp
# intel (icc, icpc, ifort): -qopenmp
# PGI (pgcc, pgCC, pgf77, pgf90): -mp
# Clang (clang, clang++): -fopenmp
# etc... https://computing.llnl.gov/tutorials/openMP/

with open('README.rst', 'r') as f:
    readme = f.read()

with open('version', 'r') as f:
    version = f.read()

if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(
        name='ohmlr',
        version=version,
        description='One-hot multinomial logisitc regression',
        long_description=readme,
        author='Joseph P. McKenna',
        author_email='joepatmckenna@gmail.com',
        url='http://joepatmckenna.github.io/ohmlr',
        download_url='https://pypi.org/project/ohmlr',
        packages=['ohmlr'],
        # packages=find_packages(),
        # ext_modules=[fortran_module],
        classifiers=("Programming Language :: Python :: 3",
                     "Operating System :: OS Independent"),
        license='MIT',
        keywords=['inference', 'statistics', 'machine learning'])
    # data_files=[])
