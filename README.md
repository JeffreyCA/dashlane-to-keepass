# dashlane-to-keepass
Python 2/3 script to convert Dashlane-exported CSV to KeePass 1.x XML

## Installation
1. Install dependencies
```
pip install validators
```
2. Download `script.py`

## Usage
`python script.py [-h] [-g GROUP] [-v] input_csv output_xml`

```
usage: script.py [-h] [-g GROUP] [-v] input_csv output_xml

Converts Dashlane-exported CSV files to KeePass 1.x XML format. Supports
password entries with both username and email fields.

positional arguments:
  input_csv             Dashlane-exported CSV input file
  output_xml            KeePass 1.x XML output file

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP, --group GROUP
                        name of group the passwords are stored under (by
                        default the group is 'General')
  -v, --verbose         enable verbose logging
```

### Example

`python script.py -g "Custom Group" dashlane_export.csv keepass.xml`
