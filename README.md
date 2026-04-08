# AI Work Assistant OpenEnv

## Project Overview
The **AI Work Assistant OpenEnv** is a production-ready simulation environment designed for the Meta OpenEnv Hackathon. It evaluates an AI agent's ability to perform common productivity tasks: categorizing communications, debugging code, and processing structured data.

## Motivation
As AI agents move from chat interfaces to autonomous "employees," they must master real-world workflows. This environment provides a standardized benchmark for testing agents on multi-step tasks with incremental rewards and deterministic grading.

## Task Descriptions

### 1. Email Triage (Easy)
- **Input**: Raw email text snippet.
- **Action**: Classify into one of three categories: `important`, `spam`, or `work`.
- **Grading**: Binary (1.0 for correct, 0.0 for incorrect).

### 2. Code Review (Medium)
- **Input**: A buggy Python function.
- **Action**: Identify the specific type of bug: `missing return`, `wrong variable`, or `syntax error`.
- **Grading**: Exact match (1.0), partial match if keywords are present (0.5), else 0.0.

### 3. Data Cleaning (Hard)
- **Input**: A JSON dataset with null values, duplicates, and incorrect types.
- **Action**: Return a cleaned JSON list following these rules:
  - Remove rows with `None` values.
  - Cast `age` to `int`.
  - Remove duplicate entries (by `id`).
- **Grading**: Fully correct list (1.0), valid but partially correct list (0.5), else 0.0.

## Interface Specifications

### Observation Space
The observation is a Pydantic model:
- `task_id`: String identifier.
- `description`: Instructions for the task.
- `input_data`: Task-specific content (text, code, or JSON).
- `step_count`: Current step in the sequence.

### Action Space
The agent must provide:
- `thought`: A string explaining its reasoning.
- `prediction`: The task output (string for Easy/Medium, List[Dict] for Hard).

### Reward System
- `+1.0`: Final task completion.
- `+0.2`: Correct intermediate/partial steps.
- `-0.1`: Incorrect action.
- `-0.5`: Repeated/looping action (identical prediction as previous step).

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Validation**:
   Check if the environment loads correctly:
   ```bash
   python env.py
   ```

3. **Run Baseline Inference**:
   Set your API key (ensure you use `HF_TOKEN` as the variable name):
   ```bash
   export HF_TOKEN="your_openai_key"
   python run_baseline.py
   ```

## Docker Support

Build the environment:
```bash
docker build -t openenv-work-assistant .
```

Run in container:
```bash
docker run -e HF_TOKEN="your_token" openenv-work-assistant python run_baseline.py
```

## Hugging Face Spaces
This project is fully compatible with containerized Hugging Face Spaces. 
- **Tags**: `openenv`
- **Instructions**: Connect your repository to a new HF Space and ensure the `Dockerfile` is at the root.

## Baseline Results (GPT-4o)
- **Email Triage**: 1.0 (Passed)
- **Code Review**: 1.0 (Passed)
- **Data Cleaning**: 1.0 (Passed)
- **Average Score**: 1.0
