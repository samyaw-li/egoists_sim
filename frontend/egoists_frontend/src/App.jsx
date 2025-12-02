import { useState } from "react";
import SimulationControls from "./components/SimulationControls";
import CustomPayoffForm from "./components/CustomPayoffForm";
import ResultsTable from "./components/ResultsTable";
import TrendChart from "./components/TrendChart";
import "./App.css";
import "./styles/components.css";

function App() {
  const [settings, setSettings] = useState({
    numPlayers: 16,
    altruistRatio: 50,
    gameType: "BASIC",
    customPayoff: {},
  });

  const [results, setResults] = useState([]);

    const handleSimulate = async () => {
    const res = await fetch("http://127.0.0.1:8000/simulate_round", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        num_players: settings.numPlayers,
        altruist_ratio: settings.altruistRatio / 100,
        game_type: settings.gameType,
        custom_payoff:
          settings.gameType === "CUSTOM"
            ? {
                CC: [
                  Number(settings.customPayoff.CC_self || 0),
                  Number(settings.customPayoff.CC_other || 0),
                ],
                CD: [
                  Number(settings.customPayoff.CD_self || 0),
                  Number(settings.customPayoff.CD_other || 0),
                ],
                DD: [
                  Number(settings.customPayoff.DD_self || 0),
                  Number(settings.customPayoff.DD_other || 0),
                ],
              }
            : null,
      }),
    });

    const data = await res.json();
    setResults(data.history || []);
  };

  const handleReset = async () => {
    await fetch("http://127.0.0.1:8000/reset", { method: "POST" });
    setResults([]);
  };

  return (
    <div className="app-container">
      <h1>Egoists vs Altruists Simulation</h1>

      <SimulationControls settings={settings} setSettings={setSettings} />

      {settings.gameType === "CUSTOM" && (
        <CustomPayoffForm settings={settings} setSettings={setSettings} />
      )}

      <div className="button-row">
        <button onClick={handleSimulate}>Run Round</button>
        <button onClick={handleReset}>Reset</button>
      </div>

      <ResultsTable results={results} />
      <TrendChart results={results} />
    </div>
  );
}

export default App;
