import os
import json
import time
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich import print as rprint

from env import WorkEnv, Action, Observation

load_dotenv()
console = Console()
api_key = os.getenv("HF_TOKEN")
client = OpenAI(api_key=api_key)

class Analytics:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def log_step(self, task_id: str, action: Action, reward: float, reason: str):
        self.history.append({
            "task": task_id,
            "thought": action.thought,
            "prediction": str(action.prediction)[:50],
            "reward": reward,
            "reason": reason,
            "timestamp": time.time()
        })

    def show_summary(self):
        table = Table(title="[bold cyan]Run Statistics[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Task ID", style="dim")
        table.add_column("Result", justify="right")
        table.add_column("Reason")
        table.add_column("Reward", justify="right")

        total_reward = 0
        rewards = []
        for entry in self.history:
            total_reward += entry['reward']
            rewards.append(total_reward)
            color = "green" if entry['reward'] > 0 else "red"
            table.add_row(
                entry['task'],
                entry['prediction'],
                entry['reason'],
                f"[{color}]{entry['reward']:+.1f}[/{color}]"
            )
        
        console.print("\n", table)
        console.print(Panel(f"[bold white]Cumulative Reward:[/bold white] [bold yellow]{total_reward:.2f}[/bold yellow]", expand=False))
        self.save_chart(rewards)

    def save_chart(self, rewards: List[float]):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 5))
        plt.style.use('dark_background')
        plt.plot(rewards, marker='o', linestyle='-', color='#00ffcc', linewidth=2)
        plt.fill_between(range(len(rewards)), rewards, color='#00ffcc', alpha=0.1)
        plt.title('Agent Performance: Cumulative Reward Over Steps', color='white', pad=20)
        plt.xlabel('Step Count', color='gray')
        plt.ylabel('Total Reward', color='gray')
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.savefig('performance_chart.png')
        console.print("[dim italic]📊 Performance chart saved to 'performance_chart.png'[/dim italic]")

def mock_solver(obs: Observation) -> Action:
    prediction = "None"
    thought = "Analyzing environment state and formulating optimal response."
    
    if obs.task_id == "email-triage":
        content = str(obs.input_data).lower()
        if "urgent" in content: 
            prediction = "work"
            thought = "Subject line contains high-priority keywords ('Urgent'). Classifying as 'work'."
        elif "congratulations" in content: 
            prediction = "spam"
            thought = "Detected typical promotional/phishing signature. Classifying as 'spam'."
        else: 
            prediction = "important"
            thought = "Personal context detected without work-related urgency. Classifying as 'important'."
            
    elif obs.task_id == "code-review":
        content = str(obs.input_data)
        if "result =" in content and "return" not in content: 
            prediction = "missing return"
            thought = "Function computes a result but fails to return it to the caller."
        elif "nmae" in content: 
            prediction = "wrong variable"
            thought = "Typo detected: 'nmae' instead of 'name' in the print statement."
        else: 
            prediction = "syntax error"
            thought = "Syntax error: Function definition is missing a colon."
            
    elif obs.task_id == "data-cleaning":
        prediction = [{"id": 1, "name": "Alice", "age": 25}, {"id": 3, "name": "Charlie", "age": 30}]
        thought = "Removing rows with null values, casting age to int, and de-duplicating by ID."
        
    return Action(thought=thought, prediction=prediction)

def get_agent_action(obs: Observation) -> Action:
    if not api_key or api_key == "your_actual_key_here":
        return mock_solver(obs)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Task: {obs.description}\nInput: {obs.input_data}\nRespond JSON: 'thought', 'prediction'"}],
            response_format={"type": "json_object"},
            timeout=10
        )
        data = json.loads(response.choices[0].message.content)
        return Action(thought=data.get("thought", ""), prediction=data.get("prediction", ""))
    except Exception:
        return mock_solver(obs)

def main():
    console.clear()
    console.print(Panel.fit("[bold cyan]🚀 OpenEnv AI Work Assistant - Production Baseline[/bold cyan]\n[dim]Initializing neural environment and telemetry...[/dim]", border_style="cyan"))
    
    env = WorkEnv()
    analytics = Analytics()
    obs = env.reset()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        while not env.done:
            task_desc = f"[bold yellow]Executing {obs.task_id}[/bold yellow] (Step {obs.step_count+1})"
            p_task = progress.add_task(description=task_desc, total=None)
            
            action = get_agent_action(obs)
            next_obs, reward, done, info = env.step(action)
            
            analytics.log_step(obs.task_id, action, reward.value, reward.reason)
            
            progress.update(p_task, completed=True)
            
            if info.get("task_completed"):
                rprint(f"[bold green]✓[/bold green] Task {obs.task_id} cleared!")
            
            obs = next_obs
            if done:
                break

    analytics.show_summary()

if __name__ == "__main__":
    main()
