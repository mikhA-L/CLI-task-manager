import argparse
import json
import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

DATA_FILE = "tasks.json"
console = Console()


def load_tasks(filepath=DATA_FILE):
    """Load tasks from JSON file, returning an empty list if missing or corrupt."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        console.print("[bold red]Warning:[/bold red] Could not read data file. Starting fresh.")
        return []


def save_tasks(tasks, filepath=DATA_FILE):
    """Save tasks list to a JSON file."""
    try:
        with open(filepath, "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        console.print(f"[bold red]Error saving tasks:[/bold red] {e}")


def add_task(tasks, title=None, priority="Med", filepath=DATA_FILE):
    """Add a task. Asks for prompt if title is None, raises ValueError if title is empty."""
    if title is None:
        title = Prompt.ask("[bold cyan]Task Title:[/bold cyan]").strip()
        if not title:
            console.print("[red]The title cannot be blank.[/red]")
            return None

        priority = Prompt.ask(
            "[bold cyan]Priority[/bold cyan]",
            choices=["High", "Med", "Low"],
            default="Med",
        )

    title = title.strip()
    if not title:
        raise ValueError("The task title cannot be empty.")

    if priority not in ["High", "Med", "Low"]:
        priority = "Med"

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks, filepath=filepath)
    console.print(f"[green]Task '{title}' ({priority} priority) added successfully![/green]")
    return task


def list_tasks(tasks):
    """Display all tasks formatted in a Rich table."""
    if not tasks:
        console.print(Panel("\n[yellow]No tasks found! Add one to get started.[/yellow]", title="Info"))
        return

    table = Table(title="\n[blue]Your Tasks[/blue]", show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="center", style="dim", width=6)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Title", justify="left")
    table.add_column("Created at", justify="center", style="dim")

    for task in tasks:
        if task["completed"]:
            status = "[bold green]✔ Done[/bold green]"
            title_style = f"[strike dim]{task['title']}[/strike dim]"
        else:
            status = "[bold yellow]Pending[/bold yellow]"
            title_style = task["title"]

        p = task["priority"]
        if p == "High":
            priority_fmt = "[bold red]High[/bold red]"
        elif p == "Med":
            priority_fmt = "[bold yellow]Med[/bold yellow]"
        else:
            priority_fmt = "[bold blue]Low[/bold blue]"

        table.add_row(str(task["id"]), status, priority_fmt, title_style, task["created_at"])

    console.print(table)


def mark_complete(tasks, tasks_id=None, filepath=DATA_FILE):
    """Mark a task complete by ID. Returns True if found, False otherwise."""
    if tasks_id is None:
        list_tasks(tasks)
        if not tasks:
            return False

        try:
            tasks_id = int(Prompt.ask("[bold cyan]Enter Task ID to mark complete[/bold cyan]"))
        except ValueError:
            console.print("[yellow]Please enter a valid numeric ID.[/yellow]")
            return False

    for task in tasks:
        if task["id"] == tasks_id:
            task["completed"] = True
            save_tasks(tasks, filepath=filepath)
            console.print(f"\n[green]Task #{tasks_id} marked as Complete![/green]")
            return True

    console.print("[bold red]Task ID not found.[/bold red]")
    return False


def del_tasks(tasks, task_iD=None, filepath=DATA_FILE):
    """Delete a task by ID and re-index remaining task IDs."""
    if task_iD is None:
        list_tasks(tasks)
        if not tasks:
            return None

        try:
            task_iD = int(Prompt.ask("[bold cyan]Enter Task ID to delete[/bold cyan]"))
        except ValueError:
            console.print("[bold red]Please enter a valid numeric ID.[/bold red]")
            return None

    for i, task in enumerate(tasks):
        if task["id"] == task_iD:
            removed = tasks.pop(i)
            for idx, t in enumerate(tasks, start=1):
                t["id"] = idx
            save_tasks(tasks, filepath=filepath)
            console.print(f"[bold red]Deleted task: '{removed['title']}'[/bold red]")
            return removed

    console.print("[bold red]Task ID not found.[/bold red]")
    return None


def main(args):
    tasks = load_tasks()

    # CLI Flags execution
    if args.view:
        list_tasks(tasks)
        return
    elif args.add is not None:
        add_task(tasks, title=args.add, priority=args.priority or "Med")
        return
    elif args.mark is not None:
        mark_complete(tasks, tasks_id=args.mark)
        return
    elif args.dele is not None:
        del_tasks(tasks, task_iD=args.dele)
        return
    elif args.priority and args.add is None:
        console.print("[bold red]Error:[/bold red] Priority flag can only be used with --add.")
        console.print('Example: python taskmanager.py --add "Task Name" -p High')
        return

    # Menu Loop
    while True:
        console.print("\n[bold cyan]--- Task Manager ---[/bold cyan]")
        console.print("1. [green]View Tasks[/green]")
        console.print("2. [blue]Add Task[/blue]")
        console.print("3. [yellow]Complete Task[/yellow]")
        console.print("4. [red]Delete Task[/red]")
        console.print("5. Exit")

        choice = Prompt.ask("[bold]Select an option[/bold]", choices=["1", "2", "3", "4", "5"])

        match choice:
            case "1":
                list_tasks(tasks)
            case "2":
                add_task(tasks)
            case "3":
                mark_complete(tasks)
            case "4":
                del_tasks(tasks)
            case "5":
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    parser.add_argument("-v", "--view", action="store_true", help="Display all tasks")
    parser.add_argument("-a", "--add", type=str, help="Add a task title")
    parser.add_argument("-p", "--priority", choices=["High", "Med", "Low"], help="Set Priority")
    parser.add_argument("-m", "--mark", type=int, help="Mark task complete using ID")
    parser.add_argument("-d", "--dele", type=int, help="Delete task using ID")

    args = parser.parse_args()
    main(args)