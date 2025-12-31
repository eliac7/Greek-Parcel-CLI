import typer
from rich.console import Console
from rich.table import Table

from greek_parcel.core.constants import ERROR_TRACKING_PACKAGE
from greek_parcel.core.identification import identify_courier
from greek_parcel.core.storage import load_history, remove_from_history, update_alias
from greek_parcel.cli.interactions import handle_history_save
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
        help="Courier name. If omitted, searches all.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output results as JSON instead of a formatted table.",
    ),
    save: bool = typer.Option(
        False,
        "--save",
        "-s",
        help="Automatically save to history without prompting.",
    ),
    no_save: bool = typer.Option(
        False,
        "--no-save",
        help="Do not save to history and do not prompt.",
    ),
):
    """
    Track a parcel.

    If found, you will be asked to save it to your history (unless --save or --no-save is used).
    """
    found = False
    found_courier_name = ""

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
                    found_courier_name = courier
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

        # Detect potential couriers
        candidates = identify_courier(tracking_number)

        if candidates:
            couriers_to_check = candidates
            if not json_output:
                console.print(
                    f"[dim]Detected potential couriers: {', '.join(candidates)}[/dim]"
                )
        else:
            # Fallback to all couriers if no pattern matches
            couriers_to_check = list_couriers()
            if not json_output:
                console.print(
                    "[dim]Could not identify courier format. Checking all...[/dim]"
                )

        with console.status("Searching for package...", spinner="dots") as status:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(couriers_to_check)
            ) as executor:
                future_to_courier = {
                    executor.submit(check_courier, name): name
                    for name in couriers_to_check
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
                            found_courier_name = name
                            break
                    except Exception:
                        continue

    if found:
        handle_history_save(tracking_number, found_courier_name, save, no_save, json_output)

    if not found and not courier:
        console.print(
            f"[bold red]Could not find tracking number {tracking_number} in any supported courier.[/bold red]"
        )
        raise typer.Exit(code=1)


@app.command()
def history():
    """Show tracking history."""
    history_data = load_history()
    if not history_data:
        console.print("[yellow]No tracking history found.[/yellow]")
        return

    table = Table(title="Tracking History")
    table.add_column("Alias", style="magenta")
    table.add_column("Courier", style="cyan")
    table.add_column("Tracking Number", style="green")

    for item in history_data:
        table.add_row(
            item.get("alias", ""),
            item.get("courier", ""),
            item.get("tracking_number", ""),
        )
    console.print(table)


@app.command()
def forget(tracking_number: str):
    """Remove a tracking number from history."""
    remove_from_history(tracking_number)
    console.print(f"[green]Removed {tracking_number} from history.[/green]")


@app.command()
def rename(tracking_number: str, alias: str):
    """Assign an alias to a tracking number."""
    if update_alias(tracking_number, alias):
        console.print(f"[green]Assigned alias '{alias}' to {tracking_number}.[/green]")
    else:
        console.print(
            f"[red]Tracking number {tracking_number} not found in history.[/red]"
        )


@app.command()
def refresh():
    """Track all items in history and show their current status."""
    history_data = load_history()
    if not history_data:
        console.print("[yellow]No tracking history found.[/yellow]")
        return

    for item in history_data:
        number = item["tracking_number"]
        courier_name = item["courier"]
        alias = item.get("alias", "")

        display_name = f"{alias} ({number})" if alias else number
        console.print(f"\n[bold blue]Checking {display_name}...[/bold blue]")

        # We reuse the track logic but simplified (no history saving)
        tracker = get_tracker(courier_name)
        if tracker:
            try:
                package = tracker.track(number)
                display_package(package)
            except Exception as e:
                console.print(f"[red]Error tracking {number}: {e}[/red]")
        else:
            console.print(f"[red]Courier {courier_name} not found.[/red]")


if __name__ == "__main__":
    app()