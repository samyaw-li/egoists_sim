import "../styles/SimulationControls.css";

function SimulationControls({ settings, setSettings }) {
  const handleChange = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="simulation-controls">
      <div className="control">
        <label>Game Type:</label>
        <select
          value={settings.gameType}
          onChange={(e) => handleChange("gameType", e.target.value)}
        >
          <option value="BASIC">Basic Game</option>
          <option value="COMPETITIVE">Competitive Game</option>
        </select>
      </div>
    </div>
  );
}

export default SimulationControls;
