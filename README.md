# Download and parse files from the CDS download service

## Implementation steps

- Create and activate a virtual environment, e.g.

  `python3 -m venv venv/`
  `source venv/bin/activate`

- Environment variable settings

  - domain=root domain from which to download GZIP files
  - client_secret
  - client_id
  - DATABASE_UK=postgres connection string
  - IMPORT_FOLDER=folder to which to copy files, for import
  - OVERWRITE_XLSX=0|1 - 0 will run parser on all files; 1 will only parse files that are missing

- Install necessary Python modules 

  - appdirs==1.4.4
  - autopep8==1.5.4
  - certifi==2020.12.5
  - chardet==4.0.0
  - distlib==0.3.1
  - elementpath==2.0.4
  - et-xmlfile==1.0.1
  - filelock==3.0.12
  - idna==2.10
  - jdcal==1.4.1
  - lxml==4.6.2
  - Markdown==3.3.3
  - mdutils==1.3.0
  - numpy==1.19.4
  - openpyxl==3.0.5
  - pandas==1.1.4
  - pipenv==2020.11.15
  - psycopg2==2.8.6
  - pycodestyle==2.6.0
  - python-dateutil==2.8.1
  - python-docx==0.8.10
  - python-dotenv==0.15.0
  - pytz==2020.4
  - requests==2.25.1
  - sh==1.14.1
  - simplified-scrapy==1.5.159
  - six==1.15.0
  - toml==0.10.2
  - urllib3==1.26.2
  - virtualenv==20.2.2
  - virtualenv-clone==0.5.4
  - wget==3.2
  - xlrd==1.2.0
  - XlsxWriter==1.3.7
  - xmlschema==1.3.1


  via `pip3 install -r requirements.txt`

## Usage

### To download CDS extract files:
`python3 download.py`

### To parse CDS extract files into Excel:
`python3 parse.py`
