import asyncio
import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from env import WorkEnv, Action
from inference import get_agent_action

load_dotenv()
app = FastAPI(title="OpenEnv AI Work Assistant Dashboard")

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
templates = Jinja2Templates(directory="static")
global_env = WorkEnv()

@app.get("/")
async def get_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

# --- MANDATORY OPENENV API ---
@app.post("/reset")
async def reset_env():
    return global_env.reset().dict()

@app.post("/step")
async def step_env(action: Action):
    obs, reward, done, info = global_env.step(action)
    return {"observation": obs.dict(), "reward": reward.dict(), "done": done, "info": info}

@app.get("/state")
async def get_state():
    return global_env.state().dict()

@app.get("/stream")
async def stream_run():
    async def event_generator():
        env = WorkEnv()
        obs = env.reset()
        
        yield f"data: {json.dumps({'status': 'initializing', 'msg': 'Initializing Neural Environment...'})}\n\n"
        await asyncio.sleep(1)

        while not env.done:
            # Send current observation
            input_display = obs.input_data
            if isinstance(input_display, list):
                input_display = json.dumps(input_display[:2], indent=2) + "..."
            
            yield f"data: {json.dumps({'type': 'observation', 'task': obs.task_id, 'desc': obs.description, 'input': str(input_display)})}\n\n"
            await asyncio.sleep(0.5)

            # Get Action
            action = get_agent_action(obs)
            yield f"data: {json.dumps({'type': 'action', 'thought': action.thought, 'prediction': str(action.prediction)})}\n\n"
            await asyncio.sleep(0.8)

            # Step Environment
            next_obs, reward, done, info = env.step(action)
            yield f"data: {json.dumps({'type': 'reward', 'value': reward.value, 'reason': reward.reason, 'total': info['total_reward']})}\n\n"
            
            obs = next_obs
            if done:
                break
            await asyncio.sleep(0.5)

        yield f"data: {json.dumps({'status': 'finished', 'msg': 'Simulation Complete'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# --- MANDATORY RUNNER ---
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
