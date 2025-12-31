import typer
from rich.console import Console

from greek_parcel.core.storage import add_to_history, is_in_history

console = Console()


def handle_history_save(
    tracking_number: str, courier: str, save: bool, no_save: bool, is_json: bool
):
    """
    Handle the interactive logic for saving a tracking number to history.

    Args:
        tracking_number: The tracking number found.
        courier: The courier name.
        save: Flag to force saving.
        no_save: Flag to force NOT saving.
        is_json: Flag indicating if output is JSON (suppress prompts).
    """
    if is_json:
        # Never ask in JSON mode, only save if explicitly requested
        if save:
            add_to_history(tracking_number, courier)
        return

    if is_in_history(tracking_number):
        # Update the courier name in case it was refined, but don't prompt
        add_to_history(tracking_number, courier)
        return

    if no_save:
        return

    should_save = save
    if not should_save:
        should_save = typer.confirm(
            "Save this tracking number to history?", default=False
        )

    if should_save:
        alias = typer.prompt(
            "Optional alias (press Enter to skip)", default="", show_default=False
        )
        add_to_history(tracking_number, courier, alias)
        console.print(f"[green]Saved {tracking_number} to history.[/green]")
