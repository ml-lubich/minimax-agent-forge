from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .researcher import ResearcherAgent
from .analyst import AnalystAgent
from .writer import WriterAgent
from .base import AgentResponse

console = Console()


class Orchestrator:
    """Coordinates the multi-agent research pipeline."""

    def __init__(self, client: OpenAI, model: str = "MiniMax-Text-01"):
        self.researcher = ResearcherAgent(client, model)
        self.analyst = AnalystAgent(client, model)
        self.writer = WriterAgent(client, model)

    def run(self, query: str) -> str:
        console.print(Panel(f"[bold cyan]Query:[/] {query}", title="Agent Forge Pipeline"))

        # Stage 1: Research
        console.print("\n[bold yellow]Stage 1/3:[/] Researcher Agent gathering findings...")
        research = self.researcher.run(query)
        self._display_agent_output(research)

        # Stage 2: Analysis
        console.print("\n[bold yellow]Stage 2/3:[/] Analyst Agent evaluating findings...")
        analysis = self.analyst.run(query, context=research.content)
        self._display_agent_output(analysis)

        # Stage 3: Writing
        console.print("\n[bold yellow]Stage 3/3:[/] Writer Agent composing report...")
        combined_context = f"RESEARCH:\n{research.content}\n\nANALYSIS:\n{analysis.content}"
        report = self.writer.run(query, context=combined_context)
        self._display_agent_output(report)

        console.print("\n[bold green]Pipeline complete.[/]\n")
        return report.content

    def _display_agent_output(self, response: AgentResponse):
        md = Markdown(response.content)
        console.print(Panel(md, title=f"[bold]{response.agent_name} Agent[/]", border_style="blue"))
