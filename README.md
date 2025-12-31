# Greek Parcel CLI

A command-line interface (CLI) tool for tracking parcels from various Greek courier services. Built with Python, Typer, and Rich.

## Features

- **Multi-Courier Support**: Track packages from major Greek courier companies.
- **Smart Detection**: Automatically identifies the courier based on the tracking number format.
- **Rich Output**: Beautiful terminal output with tables and status indicators.
- **JSON Output**: Optional JSON output for programmatic integration (e.g., widgets, scripts).
- **Easy to Use**: Simple CLI commands for quick tracking.
- **Improved Reliability**: Uses random User-Agents to mimic real browser traffic and avoid blocking.

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
# List all supported couriers
greek-parcel list

# Track a parcel (auto-detects courier)
greek-parcel track <number>

# Track with a specific courier
greek-parcel track <number> -c <courier>

# Output as JSON (for integration with scripts/widgets)
greek-parcel track <number> --json
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
uv run greek-parcel track <number>
```

### After Installation

If you installed via `pip` or `uv sync`, the `greek-parcel` command will be available:

```bash
greek-parcel list
greek-parcel track <number>
```

## Development

This project uses modern Python tooling.

1.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2.  Run the CLI directly during development:
    ```bash
    python -m greek_parcel list
    python -m greek_parcel track <number>
    ```

## Contributing

Contributions are welcome! This project supports multiple courier services, but I cannot verify that all of them work correctly without real tracking numbers.

### How You Can Help

- **Share Tracking Numbers**: If you have a tracking number from any supported courier that you can share (anonymized if needed), please open an issue. This helps verify that the tracking functionality works correctly.

- **Report Issues**: Found a bug or a courier that's not working? Please open an issue with details about the problem.

- **Fork and Contribute**: Feel free to fork the repository, make improvements, and submit a pull request. Whether it's fixing bugs, adding new features, or improving documentation, all contributions are appreciated!

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Acknowledgements

Special thanks to [Daniel Pikilidis](https://github.com/DanielPikilidis) and his project [Greek-Courier-API](https://github.com/DanielPikilidis/Greek-Courier-API) for providing the endpoints and selectors used in this project.

## License

[MIT License](LICENSE)