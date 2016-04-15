# Python Spoj
<!-- [![Build Status](https://travis-ci.org/DheerendraRathor/Python-Spoj.svg?branch=master)](https://travis-ci.org/DheerendraRathor/Python-Spoj) -->
<!-- [![Downloads](https://pypip.in/download/python_spoj/badge.svg)](https://pypi.python.org/pypi/python_spoj/) -->
<!-- [![Latest Version](https://pypip.in/version/python_spoj/badge.svg)](https://pypi.python.org/pypi/python_spoj/) -->
<!-- [![Documentation Status](https://readthedocs.org/projects/python-spoj/badge/?version=latest)](https://readthedocs.org/projects/python-spoj/?badge=latest)   -->
A platform for writing code for spoj

Built on top of [Python-Spoj repo(DheerendraRathor)](https://github.com/DheerendraRathor/Python-Spoj)

## Installation
You need to use python2 and sudo(Linux)

    $ sudo pip2 install -r requirements.txt
    $ sudo python2 setup.py install

<!-- ## Documentation -->

<!-- Documentation is present at [Read the Docs](http://python-spoj.rtfd.org) and also at the [PythonHosted](https://pythonhosted.org/python_spoj/) -->

## Usage
* Checkout [Code Platform web interface](https://github.com/shubhamshuklaer/code_platform_web), a web based
interface to spoj.
* Help
    * `spoj --help`
    * for help regarding a specific option like "config" use `spoj config --help`
* For autocompletion of arguments do `source /path/to/spoj_autocomplete.sh`.
Present inside the `spoj` dir.
* You can follow points given below to seperately configure it, or you can run
`spoj config --config_all` to configure everything at once.
* Create root for storing code
    * `spoj config -r`
    * You will be asked to put `path_to_chosen_root`
* Setup credentials for spoj `spoj config -c`
* Setup extensions for languages for eg. "cpp" for c++
    * `spoj config -e`
* Setup the editor to use. `spoj config --editor`. You will be asked to enter editor
* Setup compile command for a particular language
    * `spoj config --cmp_cmd`
    * for eg `g++ inp_file -o out_file`
    * inp_file and out_file are placeholders, while compiling they will be
    replaced in compile_command with actual filenames
* Setup run command for a particular language
    * `spoj config --run_cmd`
    * for eg `./out_file`
* Setup default language(optional) `spoj config -l`. You will be asked to enter the language code.
* Start a project. Eg `spoj start GSS1`. GSS1 is a problem code on spoj. The editor will open up.
* Compiling/testing/submitting - Commands must be executed from inside the
project folder eg `path_to_chosen_root/spoj/GSS1`
    * `spoj cmpile`
    * Giving test case manually: `spoj run`
    * Giving test case from a file:
        * `spoj add_input`. 2 files of form `i_<test_case_num>.txt` and `eo_<test_case_num>.txt` will be opened, fill the input and expected output respectively. Here <test_case_num> is just a number identifying the test.
        * if we pass a `-c` option with `spoj run` it will compile and then run.
        * `spoj run <test_case_num>`
        * if we give `<test_case_num>` as 0 then all test cases will be executed
* Submiting `spoj submit`
