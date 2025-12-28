from rich.console import Console
from rich.table import Table

from src.core.constants import (
    STATUS_DELIVERED,
    STATUS_IN_TRANSIT,
    STATUS_PACKAGE_NOT_FOUND,
)
from src.core.models import Package

console = Console()


def display_package(package: Package) -> None:
    """
    Display package tracking information in a formatted table.

    Args:
        package: The Package object to display
    """
    if not package.found:
        console.print(
            STATUS_PACKAGE_NOT_FOUND.format(courier_name=package.courier_name),
            style="bold red",
        )
        return

    table = Table(title=f"Tracking Info - {package.courier_name}")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Location", style="magenta")
    table.add_column("Description", style="green")

    for loc in package.locations:
        table.add_row(
            loc.datetime.strftime("%Y-%m-%d %H:%M"),
            loc.location,
            loc.description,
        )

    console.print(table)
    if package.delivered:
        console.print(STATUS_DELIVERED, style="bold green")
    else:
        console.print(STATUS_IN_TRANSIT, style="bold yellow")
