# download-CDS-files

This project downloads files containing tariff information and extracts them
into a human-readable XLSX format.

These files are subsequently emailed to various stakeholders as part of a service run
by the Online Trade Tariff team.

The following is a flowchart of the process

```mermaid
graph TD
    A[Circle CI Workflow at 7 am UTC] --> B[Sync files from trade-tariff-reporting S3 bucket]
    B --> C[Download new files from Secure Data Exchange Service - SDES]
    C --> D{Check if XLSX files already exist?}
    D -- Yes --> E[Assume files sent to third parties]
    D -- No --> F[Parse XML files into XLSX format]
    F --> G[Email via SES to relevant parties]
```

## Dependency Management

We use `pip-tools` for dependency management to declare flexible dependencies in `.in` files and generate fully pinned `.txt` lock files. Our automated workflows regularly update these lock files to ensure the latest compatible versions of dependencies are installed, even if the `.in` files do not specify exact versions.

The process is as follows:

1. Declare flexible dependencies in `requirements.in` and `requirements_dev.in` (e.g., `requests` or `requests>=2.25.0`), without strict pins.
2. Use `pip-compile --upgrade` to generate pinned `requirements.txt` and `requirements_dev.txt` files with exact versions.
3. Use `pip-sync` to install dependencies exactly as pinned, ensuring reproducible environments.
4. Our CI/CD workflows run `pip-compile --upgrade` on a schedule to bump dependency versions regularly, keeping the project secure and up-to-date.

To update dependencies:

```bash
pip-compile --upgrade --output-file=requirements.txt requirements.in  # Generates requirements.txt
pip-compile --upgrade --output-file=requirements_dev.txt requirements_dev.in  # Generates requirements_dev.txt
pip-sync requirements.txt requirements_dev.txt  # Syncs your environment
```

## Getting started for local development

```bash
python -m venv venv  # Create isolated Python environment
source venv/bin/activate  # Activate environment

# First time setup
pip install pip-tools  # Install dependency management tools
pip-compile requirements.in  # Generate requirements.txt
pip-compile requirements_dev.in  # Generate requirements_dev.txt
pip-sync requirements.txt requirements_dev.txt  # Install all dependencies
cp .env.example .env # Copy the example .env file to configure the project
```

Once you've copied the example configuration file, you'll want help from the team to populate the secrets
in your local copy of the .env file.

Please make sure you **never upload secrets to github**.

You should then be able to download the CDS files and email parsed changes like so:

```bash
python download.py
python parse.py
```

## Prerequisites

- python (specific version is defined in .tool-versions)
- aws access (speak to a team member)
- secrets for interfacing with the cds api (speak to a team member)
