import json
from typing import Dict, Any, List, Optional, Tuple, Union
from pydantic import BaseModel, Field

from tasks.email_task import get_email_tasks
from tasks.code_task import get_code_tasks
from tasks.data_task import get_data_tasks

from grader.email_grader import grade_email
from grader.code_grader import grade_code
from grader.data_grader import grade_data

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
        self.tasks.extend(get_email_tasks())
        self.tasks.extend(get_code_tasks())
        self.tasks.extend(get_data_tasks())
        # Force IDs for validator compliance
        ids = ["task_1", "task_2", "task_3"]
        for i, task in enumerate(self.tasks):
            if i < len(ids):
                task.id = ids[i]

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
        
        # Check for repeated actions (simulated by checking if prediction is same as last step)
        reward_value = 0.01 # Default baseline for incorrect action
        reason = "Incorrect action"
        
        # Grader logic
        score = 0.01 # Baseline failure score
        
        if self.history and action.prediction == self.history[-1]['prediction']:
            reward_value = 0.01
            reason = "Repeated action detected"
        else:
            if task.id == "task_1":
                score = grade_email(str(action.prediction), task.expected_category)
            elif task.id == "task_2":
                score = grade_code(str(action.prediction), task.bug_type)
            elif task.id == "task_3":
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
