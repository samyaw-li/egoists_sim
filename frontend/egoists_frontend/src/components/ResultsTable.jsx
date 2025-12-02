import "../styles/ResultsTable.css";

function ResultsTable({ results, showHalfway }) {
  if (!results.length) return <p>No results yet.</p>;

  return (
    <div className="results-table">
      <h2>Results</h2>
      <table>
        <thead>
          <tr>
            <th>Round</th>
            <th>% Altruists (Cooperators)</th>
            <th>% Egoists (Defectors)</th>
            {showHalfway && <th>% Halfway</th>}
          </tr>
        </thead>
        <tbody>
          {results.map((r, idx) => (
            <tr key={idx}>
              <td>{r.round}</td>
              <td>{(r.propC * 100).toFixed(1)}</td>
              <td>{(r.propD * 100).toFixed(1)}</td>
              {showHalfway && <td>{(r.propH * 100).toFixed(1)}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultsTable;
