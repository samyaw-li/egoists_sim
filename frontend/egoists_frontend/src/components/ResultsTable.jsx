import "../styles/ResultsTable.css";

function ResultsTable({ results }) {
  if (!results.length) return <p>No results yet.</p>;

  return (
    <div className="results-table">
      <h2>Results</h2>
      <table>
        <thead>
          <tr>
            <th>Round</th>
            <th>Game</th>
            <th>Altruists</th>
            <th>Egoists</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r) => (
            <tr key={r.round}>
              <td>{r.round}</td>
              <td>{r.game}</td>
              <td>{r.altruist_mean.toFixed(2)}</td>
              <td>{r.egoist_mean.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultsTable;
