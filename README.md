# ApplyPlus



## Running Apply Patch Script
`python3 apply.py [--reverse] [--help] ../vulnerableforks/patches/<patch_file_name>`

`patch_file_name` is required and is the patch you are applying

`--help` will list available subcommands and some
concept guides

`--reverse` will run `git apply --reverse`

## Running Tests
`python3 ../vulnerableforks/tests/<test_file_name>`
