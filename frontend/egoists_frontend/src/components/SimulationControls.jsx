import "../styles/SimulationControls.css";

function SimulationControls({ settings, setSettings }) {
  const handleChange = (field, value) => {
    setSettings((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="simulation-controls">
      <div className="control">
        <label>Number of Players:</label>
        <input
          type="number"
          value={settings.numPlayers}
          onChange={(e) => handleChange("numPlayers", Number(e.target.value))}
        />
      </div>

      <div className="control">
        <label>% Altruists:</label>
        <input
          type="number"
          value={settings.altruistRatio}
          onChange={(e) => handleChange("altruistRatio", Number(e.target.value))}
        />
      </div>

      <div className="control">
        <label>Game Type:</label>
        <select
          value={settings.gameType}
          onChange={(e) => handleChange("gameType", e.target.value)}
        >
          <option value="BASIC">BASIC</option>
          <option value="EYES">EYES</option>
          <option value="PUNISH">PUNISH</option>
          <option value="CUSTOM">Custom</option>
        </select>
      </div>

      {/* 👇 CUSTOM PAYOFF MATRIX (only visible when CUSTOM is selected) */}
      {settings.gameType === "CUSTOM" && (
        <div className="custom-payoff-section">
          <h4>Custom Payoff Matrix</h4>

          <div className="control">
            <label>Reward (C vs C):</label>
            <input
              type="number"
              value={settings.customPayoffs.CC}
              onChange={(e) =>
                handleChange("customPayoffs", {
                  ...settings.customPayoffs,
                  CC: Number(e.target.value),
                })
              }
            />
          </div>

          <div className="control">
            <label>Sucker (C vs D):</label>
            <input
              type="number"
              value={settings.customPayoffs.CD}
              onChange={(e) =>
                handleChange("customPayoffs", {
                  ...settings.customPayoffs,
                  CD: Number(e.target.value),
                })
              }
            />
          </div>

          <div className="control">
            <label>Temptation (D vs C):</label>
            <input
              type="number"
              value={settings.customPayoffs.DC}
              onChange={(e) =>
                handleChange("customPayoffs", {
                  ...settings.customPayoffs,
                  DC: Number(e.target.value),
                })
              }
            />
          </div>

          <div className="control">
            <label>Punishment (D vs D):</label>
            <input
              type="number"
              value={settings.customPayoffs.DD}
              onChange={(e) =>
                handleChange("customPayoffs", {
                  ...settings.customPayoffs,
                  DD: Number(e.target.value),
                })
              }
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default SimulationControls;
