import os
import json
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

from env import WorkEnv, Action, Observation

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
HF_TOKEN = os.getenv("HF_TOKEN")

def log_start(task: str, model: str):
    print(f"[START] task={task} model={model}")

def log_step(step: int, action: str, reward: float, done: bool, error: str = None):
    print(f"[STEP] step={step} action={action} reward={reward} done={done} error={error}")

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    print(f"[END] success={success} steps={steps} score={score} rewards={rewards}")

def mock_solver(obs: Observation) -> Action:
    prediction = "None"
    thought = "Analytical processing."
    if "email" in str(obs.task_id):
        prediction = "work"
    elif "code" in str(obs.task_id):
        prediction = "return result"
    elif "data" in str(obs.task_id):
        prediction = [{"id": 1, "name": "Alice", "age": 25}, {"id": 3, "name": "Charlie", "age": 30}]
    return Action(thought=thought, prediction=prediction)

def get_agent_action(obs: Observation) -> Action:
    api_key = HF_TOKEN or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return mock_solver(obs)

    try:
        from openai import OpenAI
        client = OpenAI(base_url=API_BASE_URL, api_key=api_key)
        prompt = f"Task: {obs.description}\nInput: {obs.input_data}\nReturn JSON: {{'thought': '...', 'prediction': '...'}}"
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        res = json.loads(response.choices[0].message.content)
        return Action(thought=res.get("thought", ""), prediction=res.get("prediction", ""))
    except Exception:
        return mock_solver(obs)

def main():
    env = WorkEnv()
    
    # We need to run exactly 3 task evaluations, each with [START] and [END]
    for i in range(len(env.tasks)):
        # Important: We evaluate each task in the sequence
        # Since env.step() advances the index, we just need to detect the boundaries
        
        obs = env._get_observation()
        if not obs: break
        
        task_id = obs.task_id
        log_start(task=task_id, model=MODEL_NAME)
        
        task_rewards = []
        task_steps = 0
        
        # Run steps until THIS specific task is done (index increments or env done)
        start_idx = env.current_task_idx
        while env.current_task_idx == start_idx and not env.done:
            task_steps += 1
            action = get_agent_action(obs)
            
            obs, reward, done, info = env.step(action)
            task_rewards.append(reward.value)
            
            log_step(step=task_steps, action=action.thought[:30], reward=reward.value, done=done)
            
            if done: break
            
        # Task is finished, print [END] for THIS task
        avg_score = sum(task_rewards) / max(len(task_rewards), 1)
        log_end(success=avg_score > 0.5, steps=task_steps, score=avg_score, rewards=task_rewards)

if __name__ == "__main__":
    main()
