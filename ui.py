import sys
from typing import Generator, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console()


def print_welcome_banner(provider_name: str, model_name: str) -> None:
    banner_text = Text()
    banner_text.append("🤖 JARVIS AI CLI Assistant", style="bold cyan")
    banner_text.append("\nYour Personal Terminal-based Generative AI Companion\n", style="dim white")
    banner_text.append(f"\nProvider: ", style="bold green")
    banner_text.append(f"{provider_name.upper()}", style="yellow")
    banner_text.append(f"  |  Model: ", style="bold green")
    banner_text.append(f"{model_name}", style="yellow")
    banner_text.append("\nType ", style="dim")
    banner_text.append("/help", style="bold magenta")
    banner_text.append(" for slash commands or ", style="dim")
    banner_text.append("/exit", style="bold magenta")
    banner_text.append(" to quit.", style="dim")

    console.print(Panel(banner_text, border_style="cyan", expand=False))


def print_help_menu() -> None:
    table = Table(title="Available Slash Commands", border_style="cyan", title_style="bold cyan")
    table.add_column("Command", style="bold magenta", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("/help", "Show this help menu")
    table.add_row("/clear", "Clear active conversation context history")
    table.add_row("/history", "Display current session conversation history")
    table.add_row("/system <prompt>", "View or update system instruction prompt")
    table.add_row("/model", "Display active LLM provider and model name")
    table.add_row("/exit or /quit", "Save session and exit CLI Assistant")

    console.print(table)


def get_user_input() -> str:
    try:
        console.print("\n[bold cyan]You >[/bold cyan] ", end="")
        user_input = input().strip()
        return user_input
    except (KeyboardInterrupt, EOFError):
        return "/exit"


def render_streaming_response(stream_generator: Generator[str, None, None]) -> str:
    console.print("\n[bold green]AI >[/bold green] ", end="")

    full_response = ""
    try:
        for chunk in stream_generator:
            console.print(chunk, end="", highlight=False)
            full_response += chunk
        console.print()
    except Exception as e:
        console.print(f"\n[bold red][Streaming Error]: {e}[/bold red]")

    return full_response


def print_history_summary(messages: List[Dict[str, Any]], system_prompt: str) -> None:
    console.print(Panel("[bold cyan]Conversation Session History[/bold cyan]", border_style="cyan"))

    if system_prompt:
        console.print(f"[bold yellow]System Prompt:[/bold yellow] {system_prompt}\n")

    if not messages:
        console.print("[dim]No messages in current session.[/dim]")
        return

    for idx, msg in enumerate(messages, 1):
        role = msg.get("role", "unknown").capitalize()
        content = msg.get("content", "")
        style = "bold cyan" if role == "User" else "bold green"
        console.print(f"[{style}][{idx}] {role}:[/{style}] {content}")


def print_info(message: str) -> None:
    console.print(f"[bold blue]ℹ {message}[/bold blue]")


def print_success(message: str) -> None:
    console.print(f"[bold green]✔ {message}[/bold green]")


def print_warning(message: str) -> None:
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")


def print_error(message: str) -> None:
    console.print(f"[bold red]✖ {message}[/bold red]")
