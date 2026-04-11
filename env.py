import json
from typing import Dict, Any, List, Optional, Tuple, Union
from pydantic import BaseModel

from tasks.email_task import get_email_tasks
from tasks.code_task import get_code_tasks
from tasks.data_task import get_data_tasks

from graders import grade_email, grade_code, grade_data

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
        e_tasks = get_email_tasks()
        c_tasks = get_code_tasks()
        d_tasks = get_data_tasks()
        
        task_list = [
            ("task_1", e_tasks[0], "graders:grade_email"),
            ("task_2", c_tasks[0], "graders:grade_code"),
            ("task_3", d_tasks[0], "graders:grade_data"),
        ]
        
        for tid, obj, gr in task_list:
            import copy
            task_obj = copy.deepcopy(obj)
            task_obj.id = tid
            task_obj.grader = gr
            self.tasks.append(task_obj)

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

    def step(self, action: Action) -> Tuple[Optional[Observation], Reward, bool, Dict[str, Any]]:
        if self.done:
             return None, Reward(value=0.0, reason="env done"), True, {}

        self.step_count += 1
        task = self.tasks[self.current_task_idx]
        
        score = 0.01 
        reason = "Incorrect action"
        
        if self.history and action.prediction == self.history[-1]['prediction']:
            reward_value = 0.01
            reason = "Repeated action detected"
        else:
            if "task_1" in task.id:
                score = grade_email(str(action.prediction), "work")
            elif "task_2" in task.id:
                score = grade_code(str(action.prediction), ["return", "result"])
            elif "task_3" in task.id:
                score = grade_data(action.prediction, [{"id": 1, "name": "Alice", "age": 25}, {"id": 3, "name": "Charlie", "age": 30}])
            
            reward_value = max(min(score, 0.99), 0.01)

            if score > 0.9:
                reason = "Task completed successfully"
                self.current_task_idx += 1
                self.step_count = 0
            elif score > 0.1:
                reason = "Correct intermediate step"
            else:
                reason = "Incorrect prediction"

        self.total_reward += reward_value
        self.history.append({"thought": action.thought, "prediction": action.prediction})
        
        if self.current_task_idx >= len(self.tasks):
            self.done = True
            
        if self.step_count >= self.max_steps_per_task:
            self.current_task_idx += 1
            self.step_count = 0
            if self.current_task_idx >= len(self.tasks):
                self.done = True

        obs = self._get_observation()
        reward = Reward(value=reward_value, reason=reason)
        info = {"total_reward": self.total_reward, "task_completed": score > 0.9}
        
        return obs, reward, self.done, info
