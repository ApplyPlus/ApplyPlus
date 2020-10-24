![logo](assets/logo.png)


## Running ApplyPlus from source

1. Install dependencies as described below
2. From the root of this directory, run-

`applyplus.py [-h] [--reverse] pathToPatch`

`patch_file_name` is required and is the patch you are applying

`--help` will list available subcommands and some
concept guides

`--reverse` will run `git apply --reverse`


## Installing required packages
Requirments: 

1. Python3.6 (or above)
1. SrcML
1. SrcSlice
1. Python Libraries from PyPI-

`pip3 install -r src/requirements.txt` 

### Installing SrcML
https://www.srcml.org/#download

After the installation completes, ensure that `srcml` can be run from the terminal. If 
the `Command Not Found` error arrises, follow the instructions highlighted in this document
https://osxdaily.com/2018/05/24/command-not-found-mac-terminal-error-fix/.

### SrcSclice
A binary for MacOS/Ubuntu devices is provided in this project under the `patch_context/srcSliceBuilds` folder. 


## Running Tests
`python3 ../vulnerableforks/tests/<test_file_name>`