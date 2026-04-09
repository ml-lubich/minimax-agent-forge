#!/usr/bin/env python3
"""MiniMax Agent Forge — Multi-agent research pipeline powered by MiniMax API."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

from agents import Orchestrator

load_dotenv()
console = Console()


def get_client() -> OpenAI:
    import os

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] MINIMAX_API_KEY not found in .env")
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url="https://api.minimaxi.chat/v1")


def interactive_mode(orchestrator: Orchestrator):
    console.print("[bold cyan]MiniMax Agent Forge[/] — Interactive Mode")
    console.print("Type your research query (or 'quit' to exit)\n")
    while True:
        try:
            query = console.input("[bold green]>>> [/]").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not query or query.lower() in ("quit", "exit", "q"):
            break
        orchestrator.run(query)


def main():
    parser = argparse.ArgumentParser(description="MiniMax Agent Forge — Multi-agent research pipeline")
    parser.add_argument("query", nargs="?", help="Research topic or question")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--output", "-o", type=str, help="Save report to file")
    parser.add_argument("--model", "-m", type=str, default="MiniMax-Text-01", help="MiniMax model to use")
    args = parser.parse_args()

    client = get_client()
    orchestrator = Orchestrator(client, model=args.model)

    if args.interactive:
        interactive_mode(orchestrator)
        return

    if not args.query:
        console.print("[bold red]Error:[/] Provide a query or use --interactive mode")
        parser.print_help()
        sys.exit(1)

    report = orchestrator.run(args.query)

    if args.output:
        Path(args.output).write_text(report)
        console.print(f"\n[bold green]Report saved to:[/] {args.output}")


if __name__ == "__main__":
    main()
