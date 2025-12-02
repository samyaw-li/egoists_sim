import { useState } from "react";
import SimulationControls from "./components/SimulationControls";
import ResultsTable from "./components/ResultsTable";
import TrendChart from "./components/TrendChart";
import "./App.css";
import "./styles/components.css";

function App() {
  const [settings, setSettings] = useState({
    numPlayers: 120,   // default PS115D population
    gameType: "BASIC", // BASIC or COMPETITIVE
    showHalfway: false, // optional toggle to show halfway players
  });

  const [results, setResults] = useState([]);

  const handleSimulate = async () => {
    const res = await fetch("http://127.0.0.1:8000/ps115d/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: settings.gameType,
      }),
    });

    const data = await res.json();
    setResults(prev => [...prev, data.round_result]);
  };

  const handleReset = async () => {
    await fetch("http://127.0.0.1:8000/ps115d/reset", { method: "POST" });
    setResults([]);
  };

  return (
    <div className="app-container">
      <h1>Egoists vs Altruists Simulation (PS115D)</h1>

      <SimulationControls settings={settings} setSettings={setSettings} />

      <div className="control">
        <label>
          <input
            type="checkbox"
            checked={settings.showHalfway}
            onChange={(e) =>
              setSettings(prev => ({ ...prev, showHalfway: e.target.checked }))
            }
          />
          Show Halfway Players
        </label>
      </div>

      <div className="button-row">
        <button onClick={handleSimulate}>Run Round</button>
        <button onClick={handleReset}>Reset</button>
      </div>

      <ResultsTable results={results} showHalfway={settings.showHalfway} />
      <TrendChart results={results} showHalfway={settings.showHalfway} />
    </div>
  );
}

export default App;
