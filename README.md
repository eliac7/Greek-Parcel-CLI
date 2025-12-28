# Greek Parcel CLI

A command-line interface (CLI) tool for tracking parcels from various Greek courier services. Built with Python, Typer, and Rich.

## Features

- **Multi-Courier Support**: Track packages from major Greek courier companies.
- **Rich Output**: Beautiful terminal output with tables and status indicators.
- **Easy to Use**: Simple CLI commands for quick tracking.

## Supported Couriers

The following courier services are currently supported:

- ACS (`acs`)
- Courier Center (`couriercenter`)
- EasyMail (`easymail`)
- ELTA (`elta`)
- Geniki Taxydromiki (`geniki`)
- Skroutz Last Mile (`skroutz`)
- Speedex (`speedex`)
- BoxNow (`boxnow`)

## Installation

### Prerequisites

- Python 3.9 or higher

### Install from PyPI (Recommended)

The easiest way to install Greek Parcel CLI is using pip:

```bash
pip install greek-parcel-cli
```

After installation, the `greek-parcel` command will be available globally:

```bash
greek-parcel list
greek-parcel track <number> -c <courier>
```

### Install from Source

#### Using uv (Recommended)

1.  Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Greek-Parcel-CLI.git
    cd Greek-Parcel-CLI
    ```

2.  Sync dependencies and create environment:
    ```bash
    uv sync
    ```

#### Using pip

1.  Clone the repository and enter the directory.
2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/macOS
    source .venv/bin/activate
    ```
3.  Install the package:
    ```bash
    pip install -e .
    ```

## Usage

### Using uv (No installation required)

You can run the tool directly without manual installation:

```bash
uv run greek-parcel list
uv run greek-parcel track <number> -c <courier>
```

### After Installation

If you installed via `pip` or `uv sync`, the `greek-parcel` command will be available:

```bash
greek-parcel list
greek-parcel track <number> -c <courier>
```

## Development

This project uses modern Python tooling.

1.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2.  Run the CLI directly during development:
    ```bash
    python -m src list
    python -m src track <number> -c <courier>
    ```

## Acknowledgements

Special thanks to [Daniel Pikilidis](https://github.com/DanielPikilidis) and his project [Greek-Courier-API](https://github.com/DanielPikilidis/Greek-Courier-API) for providing the endpoints and selectors used in this project.

## License

[MIT License](LICENSE)
