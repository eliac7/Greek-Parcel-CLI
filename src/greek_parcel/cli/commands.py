import typer
from rich.console import Console
from rich.table import Table

from greek_parcel.core.constants import ERROR_TRACKING_PACKAGE, STATUS_TRACKING
from greek_parcel.core.exceptions import CourierNotFoundError
from greek_parcel.trackers import get_tracker, list_couriers
from greek_parcel.utils.display import display_package

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
        None,
        "--courier",
        "-c",
        help="Courier name (acs, boxnow, elta, geniki, skroutz, speedex, easymail, couriercenter). If omitted, searches all.",
    ),
):
    """
    Track a parcel. If courier is not specified, attempts to find it in all supported couriers.

    Args:
        tracking_number: The tracking number to look up
        courier: The courier name (optional)
    """
    if courier:
        trackers_to_try = [courier]
    else:
        trackers_to_try = list_couriers()

    found = False
    
    with console.status(
        "Searching for package..." if not courier else f"Tracking with {courier}...",
        spinner="dots",
    ) as status:
        for courier_name in trackers_to_try:
            tracker = get_tracker(courier_name)
            if not tracker:
                if courier:
                    console.print(f"[bold red]Unknown courier: {courier_name}[/bold red]")
                    raise typer.Exit(code=1)
                continue

            if not courier:
                status.update(f"Checking {courier_name}...")

            try:
                package = tracker.track(tracking_number)
                if package.found:
                    display_package(package)
                    found = True
                    break
                elif courier:
                     display_package(package)
            except Exception as e:
                if courier:
                    error_msg = ERROR_TRACKING_PACKAGE.format(error=str(e))
                    console.print(error_msg, style="bold red")
                    raise typer.Exit(code=1) from e
                continue
    
    if not found:
        if courier:
            pass
        else:
            console.print(f"[bold red]Could not find tracking number {tracking_number} in any supported courier.[/bold red]")
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
