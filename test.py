from rich.console import Console
from rich.text import Text

console = Console()
text = Text("Hello, World!")
text.stylize("bold magenta", 0, 6)
console.print(text)

from rich.prompt import Prompt
name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")

import time
from rich.progress import track

for i in track(range(20), description="Processing..."):
    time.sleep(1)  # Simulate work being done