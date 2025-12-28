from importlib.metadata import version, PackageNotFoundError

from src.core.logging_config import setup_logging

try:
    __version__ = version("greek-parcel-cli")
except PackageNotFoundError:
    # Fallback for development/editable installs
    __version__ = "0.0.0-dev"

setup_logging()
