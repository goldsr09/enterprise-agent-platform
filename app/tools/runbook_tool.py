from pathlib import Path
from langchain_core.tools import tool

RUNBOOKS_DIRECTORY = Path(__file__).resolve().parents[2]/ "runbooks"

@tool
def search_runbook(query: str) -> str:
    """Search operational runbooks for guidance related to an issue."""
    matches = []

    for path in RUNBOOKS_DIRECTORY.glob("*.md"):
        content = path.read_text()

        if query.lower() in content.lower():
            matches.append(content)

    if not matches:
        return "No matching runbook guidance was found."

    return "\n\n".join(matches)