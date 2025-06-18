import json

def format_json_readable(data: dict, indent: int = 2) -> str:
    """Format a dictionary as a human-readable JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False)

def extract_key_points(text: str) -> list:
    """Very naive key-point extractor based on lines."""
    return [line.strip() for line in text.split('\n') if line.strip()]

def wrap_markdown_section(title: str, content: str) -> str:
    """Wrap content under a markdown title."""
    return f"### {title}\n\n{content.strip()}\n"

def clean_output(text) -> str:
    if isinstance(text, dict):
        text = text.get("output", "")
    return text.strip().replace("\n\n", "\n")
