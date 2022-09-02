# Download and parse files from the CDS download service

## Implementation steps

### Create and activate a virtual environment, e.g.

  - `python3 -m venv venv/`
  - `source venv/bin/activate`

### Environment variable settings

#### Connectivity to download server

- domain=STRING
- client_secret=STRING
- client_id=STRING

#### Data

- DATABASE_UK=DATABASE CONNECTION STRING
- IMPORT_FOLDER=STRING
- OVERWRITE_XLSX=1 | 0

#### Data queries

- DIT_DATA_FOLDER=STRING
- TGB_DATA_FOLDER=STRING

### Environment variable settings

- Install necessary Python modules via `pip3 install -r requirements.txt`

---

## Usage

### To download CDS extract files:
- `python3 download.py`
- `python3 download_monthly.py`
- `python3 download_annual.py`

### To parse CDS extract files into Excel:
`python3 parse.py`

### To go to the Excel folder:
`python3 dest.py`

### To run all three of the steps above:
`python3 parse.py`

### Grepping
`python3 grep.py 058032`

---

## Searching for content using XPath

### Searching in EU-provided Taric files

- `python3 xpath.py m 3643189 tgb` (searches for measure with SID 3643189 in EU files)
- `python3 xpath.py c 2933199070 tgb` (searches for commodity with code 2933199070 in EU files)
- `python3 xpath.py mt 750 tgb` (searches for measures of type 750 in EU files)

### Searching in DIT-provided Taric files (UK tariff)

- `python3 xpath.py m 20138293 dit` (searches for measure with SID 20138293 in UK files)
- `python3 xpath.py c 2933199070 dit` (searches for commodity with code 2933199070 in UK files)
- `python3 xpath.py mt 750 dit` (searches for measures of type 750 in UK files)