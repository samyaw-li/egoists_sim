import "../styles/CustomPayoffForm.css";

function CustomPayoffForm({ settings, setSettings }) {
  const { customPayoff } = settings;

  const handleChange = (field, value) => {
    setSettings((prev) => ({
      ...prev,
      customPayoff: { ...prev.customPayoff, [field]: value },
    }));
  };

  return (
    <fieldset className="custom-payoff-form">
      <legend>Custom Payoff Matrix</legend>

      <div className="payoff-grid">
        <div></div>
        <strong>Altruist (C)</strong>
        <strong>Egoist (D)</strong>

        <div>Altruist (C) vs Altruist (C)</div>
        <input
          type="number"
          value={customPayoff.CC_self || ""}
          onChange={(e) => handleChange("CC_self", e.target.value)}
        />
        <input
          type="number"
          value={customPayoff.CC_other || ""}
          onChange={(e) => handleChange("CC_other", e.target.value)}
        />

        <div>Altruist (C) vs Egoist (D)</div>
        <input
          type="number"
          value={customPayoff.CD_self || ""}
          onChange={(e) => handleChange("CD_self", e.target.value)}
        />
        <input
          type="number"
          value={customPayoff.CD_other || ""}
          onChange={(e) => handleChange("CD_other", e.target.value)}
        />

        <div>Egoist (D) vs Egoist (D)</div>
        <input
          type="number"
          value={customPayoff.DD_self || ""}
          onChange={(e) => handleChange("DD_self", e.target.value)}
        />
        <input
          type="number"
          value={customPayoff.DD_other || ""}
          onChange={(e) => handleChange("DD_other", e.target.value)}
        />
      </div>
    </fieldset>
  );
}

export default CustomPayoffForm;
