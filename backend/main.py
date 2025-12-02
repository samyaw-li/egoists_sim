from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from simulation import run_simulation_round

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    num_players: int
    altruist_ratio: float
    game_type: str
    custom_payoff: dict | None = None

simulation_history = []

@app.post("/simulate_round")
def simulate_round(request: SimulationRequest):
    try:
        result, updated_history = run_simulation_round(
            request.num_players,
            request.altruist_ratio,
            request.game_type,
            request.custom_payoff,
            simulation_history
        )
        simulation_history[:] = updated_history  # update in-place
        return {"round_result": result, "history": simulation_history}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset")
def reset_simulation():
    simulation_history.clear()
    return {"message": "Simulation history reset successfully."}
