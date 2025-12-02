from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simulation_ps115d import create_population, simulate_round_ps115d

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

population_ps = None
history_ps = []


@app.post("/ps115d/reset")
def reset_ps115d():
    global population_ps, history_ps
    population_ps = create_population(120)
    history_ps = []
    return {"status": "reset"}


@app.post("/ps115d/simulate")
def simulate_ps115d(mode: str = "BASIC"):
    global population_ps, history_ps
    if population_ps is None:
        population_ps = create_population(120)

    population_ps, summary = simulate_round_ps115d(population_ps, mode)

    # Add round number
    round_number = len(history_ps) + 1
    summary["round"] = round_number
    summary["game"] = mode
    history_ps.append(summary)

    return {"round_result": summary, "history": history_ps}
