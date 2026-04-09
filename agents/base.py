from openai import OpenAI
from pydantic import BaseModel


class AgentResponse(BaseModel):
    agent_name: str
    content: str


class Agent:
    """Base agent powered by MiniMax API (OpenAI-compatible)."""

    def __init__(self, client: OpenAI, name: str, system_prompt: str, model: str = "MiniMax-Text-01"):
        self.client = client
        self.name = name
        self.system_prompt = system_prompt
        self.model = model

    def run(self, user_message: str, context: str = "") -> AgentResponse:
        messages = [{"role": "system", "content": self.system_prompt}]
        prompt = user_message
        if context:
            prompt = f"Context from previous agents:\n{context}\n\n---\n\nUser query: {user_message}"
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096,
            temperature=0.7,
        )
        content = response.choices[0].message.content or ""
        return AgentResponse(agent_name=self.name, content=content)
