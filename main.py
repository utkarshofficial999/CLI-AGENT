"""
Main Entry Point & REPL Engine for AI CLI Assistant.
Handles user input loop, slash commands, conversation state, streaming responses, and graceful exit.
"""

import sys
import config
from history_manager import HistoryManager
from llm_client import create_llm_client, BaseLLMClient
import ui


def get_active_model_name(provider: str) -> str:
    """Returns the model name string for the active provider."""
    if provider == "groq":
        return config.GROQ_MODEL
    elif provider == "gemini":
        return config.GEMINI_MODEL
    return config.OPENAI_MODEL


def handle_slash_command(
    command: str,
    history: HistoryManager,
    client: BaseLLMClient
) -> bool:
    """
    Handles slash commands. Returns True if command was handled, False if regular query.
    If command is /exit or /quit, terminates the application loop.
    """
    cmd_lower = command.lower().strip()

    if cmd_lower in ("/exit", "/quit"):
        history.save()
        ui.print_success("Conversation history saved. Goodbye! 👋")
        sys.exit(0)

    elif cmd_lower == "/help":
        ui.print_help_menu()
        return True

    elif cmd_lower == "/clear":
        history.clear()
        ui.print_success("Active conversation history cleared.")
        return True

    elif cmd_lower == "/history":
        ui.print_history_summary(history.get_messages(), history.system_prompt)
        return True

    elif cmd_lower.startswith("/system"):
        parts = command.split(maxsplit=1)
        if len(parts) > 1:
            new_prompt = parts[1].strip()
            history.set_system_prompt(new_prompt)
            history.save()
            ui.print_success(f"System prompt updated: '{new_prompt}'")
        else:
            current_prompt = history.system_prompt or "(None set)"
            ui.print_info(f"Current System Prompt: {current_prompt}")
            ui.print_info("To update, use: /system <your new system prompt>")
        return True

    elif cmd_lower == "/model":
        provider = config.get_active_provider()
        model_name = get_active_model_name(provider)
        ui.print_info(f"Active Provider: {provider.upper()} | Model: {model_name}")
        return True

    elif command.startswith("/"):
        ui.print_warning(f"Unknown command '{command}'. Type /help for available commands.")
        return True

    return False


def main():
    """Main application loop."""
    # 1. Initialize History Manager
    history = HistoryManager(
        storage_path=config.HISTORY_FILE,
        system_prompt=config.DEFAULT_SYSTEM_PROMPT
    )
    history_loaded = history.load()

    # 2. Initialize LLM Client
    try:
        client = create_llm_client()
        active_provider = config.get_active_provider()
        active_model = get_active_model_name(active_provider)
    except ValueError as err:
        ui.print_error(str(err))
        ui.print_info(
            "Quick Setup:\n"
            "1. Copy '.env.example' to '.env'\n"
            "2. Open '.env' and set your GROQ_API_KEY (or GEMINI_API_KEY / OPENAI_API_KEY)\n"
            "3. Run 'python main.py' again!"
        )
        sys.exit(1)
    except Exception as err:
        ui.print_error(f"Unexpected error initializing LLM client: {err}")
        sys.exit(1)

    # 3. Print Welcome Banner
    ui.print_welcome_banner(provider_name=active_provider, model_name=active_model)
    if history_loaded and history.get_messages():
        ui.print_info(f"Restored previous session ({len(history.get_messages())} messages loaded).")

    # 4. Interactive REPL Loop
    while True:
        try:
            user_input = ui.get_user_input()

            if not user_input:
                continue

            # Check if input is a slash command
            if handle_slash_command(user_input, history, client):
                continue

            # Add User input to conversation history
            history.add_user_message(user_input)

            # Get Streaming generator response from LLM provider
            stream_gen = client.stream_response(history)

            # Render live response stream in terminal
            assistant_response = ui.render_streaming_response(stream_gen)

            # Save assistant response to history if non-empty
            if assistant_response:
                history.add_assistant_message(assistant_response)
                history.save()

        except KeyboardInterrupt:
            ui.print_warning("\nSession interrupted. Saving history and exiting...")
            history.save()
            sys.exit(0)
        except Exception as e:
            ui.print_error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
