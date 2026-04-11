import json
from typing import Dict, Any, List, Optional, Tuple, Union
from pydantic import BaseModel, Field

from email_task import get_email_tasks
from code_task import get_code_tasks
from data_task import get_data_tasks

from email_grader import grade_email
from code_grader import grade_code
from data_grader import grade_data

class Observation(BaseModel):
    task_id: str
    description: str
    input_data: Any
    step_count: int

class Action(BaseModel):
    thought: str
    prediction: Any

class Reward(BaseModel):
    value: float
    reason: str

class WorkEnv:
    def __init__(self):
        self.tasks = []
        self._load_tasks()
        self.current_task_idx = 0
        self.step_count = 0
        self.max_steps_per_task = 3
        self.done = False
        self.history = []
        self.total_reward = 0.0

    def _load_tasks(self):
        # Cleanly load exactly one task for each type defined in openenv.yaml
        e_tasks = get_email_tasks()
        c_tasks = get_code_tasks()
        d_tasks = get_data_tasks()
        
        # Explicit mapping to match openenv.yaml order and IDs
        if e_tasks:
            e_tasks[0].id = "1"
            e_tasks[0].grader = "email_grader:grade_email"
            self.tasks.append(e_tasks[0])
            
        if c_tasks:
            c_tasks[0].id = "2"
            c_tasks[0].grader = "code_grader:grade_code"
            self.tasks.append(c_tasks[0])
            
        if d_tasks:
            d_tasks[0].id = "3"
            d_tasks[0].grader = "data_grader:grade_data"
            self.tasks.append(d_tasks[0])

    def reset(self) -> Optional[Observation]:
        self.current_task_idx = 0
        self.step_count = 0
        self.done = False
        self.history = []
        self.total_reward = 0.0
        return self._get_observation()

    def _get_observation(self) -> Optional[Observation]:
        if self.current_task_idx >= len(self.tasks):
            return None
            
        task = self.tasks[self.current_task_idx]
        input_data = None
        if hasattr(task, 'email_text'):
            input_data = task.email_text
        elif hasattr(task, 'code_snippet'):
            input_data = task.code_snippet
        elif hasattr(task, 'messy_data'):
            input_data = task.messy_data
            
        return Observation(
            task_id=task.id,
            description=task.description,
            input_data=input_data,
            step_count=self.step_count
        )

    def state(self) -> Dict[str, Any]:
        return {
            "current_task_idx": self.current_task_idx,
            "step_count": self.step_count,
            "done": self.done,
            "total_reward": self.total_reward
        }

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        self.step_count += 1
        task = self.tasks[self.current_task_idx]
        
        # Phase 2: Start with baseline positive contribution
        score = 0.01 
        reason = "Incorrect action"
        
        if self.history and action.prediction == self.history[-1]['prediction']:
            reward_value = 0.01
            reason = "Repeated action detected"
        else:
            if task.id == "1":
                score = grade_email(str(action.prediction), task.expected_category)
            elif task.id == "2":
                # Ensure we pass the list of keywords
                score = grade_code(str(action.prediction), task.expected_keywords)
            elif task.id == "3":
                score = grade_data(action.prediction, task.cleaned_data)
            
            # Phase 2 Compliance: Strictly between 0 and 1
            reward_value = max(min(score, 0.99), 0.01)

            if score > 0.9:
                reason = "Task completed successfully"
                self.current_task_idx += 1
                self.step_count = 0
            elif score > 0.1:
                reason = "Correct intermediate step / Partial success"
            else:
                reason = "Incorrect prediction"

        self.total_reward += reward_value
        self.history.append({"thought": action.thought, "prediction": action.prediction})
        
        if self.current_task_idx >= len(self.tasks):
            self.done = True
            
        if self.step_count >= self.max_steps_per_task:
            # Task failed after max steps, move to next
            self.current_task_idx += 1
            self.step_count = 0
            if self.current_task_idx >= len(self.tasks):
                self.done = True

        obs = self._get_observation() if not self.done else None
        reward = Reward(value=reward_value, reason=reason)
        info = {"total_reward": self.total_reward, "task_completed": score > 0.9}
        
        return obs, reward, self.done, info

if __name__ == "__main__":
    # Internal validation of the OpenEnv interface
    env = WorkEnv()
    obs = env.reset()
    print(f"Initial Observation: {obs}")
    print(f"Initial State: {env.state()}")
