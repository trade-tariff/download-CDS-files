# Download and parse files from the CDS download service

## Implementation

### Create and activate a virtual environment, e.g.

- `python3 -m venv venv/`
- `source venv/bin/activate`

### Environment variable settings

#### Connectivity to CDS download server

- DOMAIN=root domain from which to download GZIP files
- CLIENT_SECRET=STRING
- CLIENT_ID=STRING

#### Data

- IMPORT_FOLDER=STRING
- COPY_TO_IMPORT_FOLDER=1 | 0
- OVERWRITE_XLSX=1 | 0

#### Send grid mail API

- SENDGRID_API_KEY=STRING
- FROM_EMAIL=in the form EMAIL ADDRESS | NAME

  e.g. test@test.com|Geoff Test

- TO_EMAILS=List of email addresses: comma-separated in the form EMAIL ADDRESS | FIRST_NAME | LAST_NAME

  e.g. test@test.com|Geoff|Test,test2@test.com|Mary|Test

- SEND_MAIL=1 | 0

### Install packages

- Install necessary Python modules via `pip3 install -r requirements.txt`

## Usage

### To download CDS extract files:

- `python3 download.py`
- `python3 download_monthly.py`
- `python3 download_annual.py`

### To parse CDS extract files into Excel:

`python3 parse.py`

### To run all three of the steps above:

`python3 run.py`
