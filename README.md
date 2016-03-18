# Python Spoj
<!-- [![Build Status](https://travis-ci.org/DheerendraRathor/Python-Spoj.svg?branch=master)](https://travis-ci.org/DheerendraRathor/Python-Spoj) -->
<!-- [![Downloads](https://pypip.in/download/python_spoj/badge.svg)](https://pypi.python.org/pypi/python_spoj/) -->
<!-- [![Latest Version](https://pypip.in/version/python_spoj/badge.svg)](https://pypi.python.org/pypi/python_spoj/) -->
<!-- [![Documentation Status](https://readthedocs.org/projects/python-spoj/badge/?version=latest)](https://readthedocs.org/projects/python-spoj/?badge=latest)   -->
A command line tool for SPOJ in python


## Installation
You need to use python2 and sudo(Linux)

    $ sudo python2 setup.py install
    $ sudo pip2 install -r requirements.txt

<!-- ## Documentation -->

<!-- Documentation is present at [Read the Docs](http://python-spoj.rtfd.org) and also at the [PythonHosted](https://pythonhosted.org/python_spoj/) -->

## Usage
* Help
    * `spoj --help`
    * for help regarding a specific option like "config" use `spoj config --help`
* Create root for storing code
    * `mkdir path_to_chosen_root`
    * `spoj -r path_to_chosen_root`
* Setup credentials for spoj `spoj config -c`
* Setup extensions for languages for eg. "cpp" for c++
    * `spoj config -e`
    * You can get the language code from `spoj/lang.py`
    * Ignore the dot while giving extension
* Setup the editor to use. `spoj config --editor editor_name`
* Setup compile command for a particular language
    * `spoj config --cmp_cmd`
    * for eg `g++ inp_file -o out_file`
    * inp_file and out_file are placeholders, while compiling they will be
    replaced in compile_command with actual filenames
* Setup run command for a particular language
    * `spoj config --run_cmd`
    * for eg `./out_file`
* Setup default language(optional) `spoj config -l 1`. here 1 is language code for c++ 5.1
* Start a project. Eg `spoj start GSS1`. GSS1 is a problem code on spoj. The editor will open up.
* Compiling/testing/submitting - Commands must be executed from inside the
project folder eg `path_to_chosen_root/spoj/GSS1`
    * spoj cmpile
    * Giving test case manually: `spoj run`
    * Giving test case from a file:
        * Create file `i_<test_case_num>.txt` and `eo_<test_case_num>.txt` and fill the input and expected output respectively. Here <test_case_num> is just a number identifying the test.
        * `spoj run <test_case_num>`
* Submiting `spoj submit`
