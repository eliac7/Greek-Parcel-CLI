import typer
from rich.console import Console
from rich.table import Table

from greek_parcel.core.constants import ERROR_TRACKING_PACKAGE, STATUS_TRACKING
from greek_parcel.core.exceptions import CourierNotFoundError
from greek_parcel.trackers import get_tracker, list_couriers
from greek_parcel.utils.display import display_package, display_package_json

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
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output results as JSON instead of a formatted table.",
    ),
):
    """
    Track a parcel. If courier is not specified, attempts to find it in all supported couriers.

    Args:
        tracking_number: The tracking number to look up
        courier: The courier name (optional)
    """
    found = False

    def check_courier(name: str):
        """Helper to track with a specific courier safely."""
        try:
            tracker = get_tracker(name)
            if not tracker:
                return None
            return tracker.track(tracking_number)
        except Exception as e:
            return None

    if courier:
        # Single courier mode
        with console.status(f"Tracking with {courier}...", spinner="dots"):
            tracker = get_tracker(courier)
            if not tracker:
                console.print(f"[bold red]Unknown courier: {courier}[/bold red]")
                raise typer.Exit(code=1)
            
            try:
                package = tracker.track(tracking_number)
                if package.found:
                    if json_output:
                        display_package_json(package)
                    else:
                        display_package(package)
                    found = True
                else:
                    if json_output:
                        display_package_json(package)
                    else:
                        display_package(package)
            except Exception as e:
                error_msg = ERROR_TRACKING_PACKAGE.format(error=str(e))
                console.print(error_msg, style="bold red")
                raise typer.Exit(code=1) from e

    else:
        # Multithreaded search
        import concurrent.futures

        couriers = list_couriers()
        with console.status("Searching for package in all couriers...", spinner="dots") as status:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(couriers)) as executor:
                future_to_courier = {
                    executor.submit(check_courier, name): name for name in couriers
                }
                
                for future in concurrent.futures.as_completed(future_to_courier):
                    name = future_to_courier[future]
                    status.update(f"Checked {name}...")
                    try:
                        package = future.result()
                        if package and package.found:
                            if json_output:
                                display_package_json(package)
                            else:
                                display_package(package)
                            found = True
                            break
                    except Exception:
                        continue

    if not found and not courier:
        console.print(f"[bold red]Could not find tracking number {tracking_number} in any supported courier.[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

