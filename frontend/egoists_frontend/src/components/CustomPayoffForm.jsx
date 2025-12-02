import "../styles/CustomPayoffForm.css";

function CustomPayoffForm({ settings, setSettings }) {
  const handlePayoffChange = (interaction, index, value) => {
    setSettings((prev) => ({
      ...prev,
      customPayoff: {
        ...prev.customPayoff,
        [interaction]: prev.customPayoff[interaction].map((v, i) =>
          i === index ? Number(value) : v
        ),
      },
    }));
  };

  return (
    <div className="custom-payoff-form">
      <h3>Custom Payoff Matrix</h3>

      <table className="payoff-table">
        <thead>
          <tr>
            <th>Interaction</th>
            <th>Self</th>
            <th>Other</th>
          </tr>
        </thead>

        <tbody>
          {["CC", "CD", "DD"].map((key) => (
            <tr key={key}>
              <td>{key}</td>
              <td>
                <input
                  type="number"
                  value={settings.customPayoff[key][0]}
                  onChange={(e) => handlePayoffChange(key, 0, e.target.value)}
                />
              </td>

              <td>
                <input
                  type="number"
                  value={settings.customPayoff[key][1]}
                  onChange={(e) => handlePayoffChange(key, 1, e.target.value)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CustomPayoffForm;
