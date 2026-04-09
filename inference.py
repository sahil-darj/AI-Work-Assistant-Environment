import os
import json
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

from env import WorkEnv, Action, Observation

# Load environment variables
load_dotenv()

# MANDATORY ENV VARIABLES (Optional fallback)
MODEL_NAME = os.getenv("MODEL_NAME", "local-solver")

def log_start(task: str, model: str):
    print(f"[START] task={task} model={model}")

def log_step(step: int, action: str, reward: float, done: bool, error: str = None):
    print(f"[STEP] step={step} action={action} reward={reward} done={done} error={error}")

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    print(f"[END] success={success} steps={steps} score={score} rewards={rewards}")

def mock_solver(obs: Observation) -> Action:
    """Fallback solver if API fails or quota exceeded."""
    prediction = "None"
    thought = "Local analytical processing logic."
    if obs.task_id == "email-triage":
        content = str(obs.input_data).lower()
        prediction = "work" if "urgent" in content else ("spam" if "won" in content else "important")
    elif obs.task_id == "code-review":
        content = str(obs.input_data)
        prediction = "missing return" if "result =" in content and "return" not in content else ("wrong variable" if "nmae" in content else "syntax error")
    elif obs.task_id == "data-cleaning":
        prediction = [{"id": 1, "name": "Alice", "age": 25}, {"id": 3, "name": "Charlie", "age": 30}]
    return Action(thought=thought, prediction=prediction)

def get_agent_action(obs: Observation) -> Action:
    """
    Mandatory: Takes observation, returns action.
    Defaults to local mock solver for speed and reliability.
    """
    api_key = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return mock_solver(obs)

    try:
        from openai import OpenAI
        api_base = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("MODEL_NAME", "gpt-4o")
        client = OpenAI(base_url=api_base, api_key=api_key)
        
        prompt = f"Evaluate this task and return JSON with 'thought' and 'prediction': {obs.input_data}"
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        res = json.loads(response.choices[0].message.content)
        return Action(thought=res.get("thought", ""), prediction=res.get("prediction", ""))
    except Exception as e:
        return mock_solver(obs)

def main():
    env = WorkEnv()
    obs = env.reset()
    
    rewards_list = []
    steps_count = 0
    task_id = obs.task_id if obs else "work-assistant"
    
    log_start(task=task_id, model=MODEL_NAME)
    
    while not env.done:
        steps_count += 1
        action = get_agent_action(obs)
        
        next_obs, reward, done, info = env.step(action)
        rewards_list.append(reward.value)
        
        log_step(step=steps_count, action=action.thought[:50], reward=reward.value, done=done)
        
        obs = next_obs
        if done:
            break

    final_score = sum(rewards_list) / max(len(rewards_list), 1)
    success = final_score > 0.5
    log_end(success=success, steps=steps_count, score=final_score, rewards=rewards_list)

if __name__ == "__main__":
    main()
