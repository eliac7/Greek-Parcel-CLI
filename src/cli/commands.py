import typer
from rich.console import Console
from rich.table import Table

from src.core.constants import ERROR_TRACKING_PACKAGE, STATUS_TRACKING
from src.core.exceptions import CourierNotFoundError
from src.trackers import get_tracker, list_couriers
from src.utils.display import display_package

app = typer.Typer(help="Greek Parcel Tracking CLI")
console = Console()


@app.command()
def list():
    """List all supported couriers."""
    couriers = list_couriers()
    table = Table(title="Supported Couriers")
    table.add_column("Name", style="cyan")
    for courier in couriers:
        table.add_row(courier)
    console.print(table)


@app.command()
def track(
    tracking_number: str,
    courier: str = typer.Option(
        ...,
        "--courier",
        "-c",
        help="Courier name (acs, elta, geniki, skroutz, speedex, easymail, couriercenter)",
    ),
):
    """
    Track a parcel with a specific courier.

    Args:
        tracking_number: The tracking number to look up
        courier: The courier name
    """
    tracker = get_tracker(courier)
    if not tracker:
        console.print(f"[bold red]Unknown courier: {courier}[/bold red]")
        raise typer.Exit(code=1)

    with console.status(
        STATUS_TRACKING.format(tracking_number=tracking_number, courier=courier),
        spinner="dots",
    ):
        try:
            package = tracker.track(tracking_number)
            display_package(package)
        except Exception as e:
            error_msg = ERROR_TRACKING_PACKAGE.format(error=str(e))
            console.print(error_msg, style="bold red")
            raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
