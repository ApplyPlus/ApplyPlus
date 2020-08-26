# vulnerableforks

Link to Patch Classification Spreadsheet: https://docs.google.com/spreadsheets/d/1hCqyOZA-nplliI-bdGzt6IMTdFmO5hQp88RwCge0wcw/edit?usp=sharing

Link to Patch Classification Write Up (Description and examples) - https://docs.google.com/document/d/134bmSlemKDy2chgjqK3wxQGC0PsluSVZDMMZgkTlp_Y/edit?usp=sharing

## Expected directory structure:

|- msm-3.10 (run scripts from within this directory)
|- vulnerableforks

## Running Apply Patch Script
`python3 apply.py [--reverse] [--help] ../vulnerableforks/patches/<patch_file_name>`

`patch_file_name` is required and is the patch you are applying

`--help` will list available subcommands and some
concept guides

`--reverse` will run `git apply --reverse`

## Running Tests
`python3 ../vulnerableforks/tests/<test_file_name>`
