import "../styles/TrendChart.css";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function TrendChart({ results, showHalfway }) {
  if (!results.length) return null;

  return (
    <div className="trend-chart">
      <h2>Trend Over Rounds</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={results}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="round" label={{ value: "Round", position: "insideBottom" }} />
          <YAxis
            label={{
              value: "Fraction",
              angle: -90,
              position: "insideLeft",
            }}
            domain={[0, 1]}
            tickFormatter={(tick) => `${(tick * 100).toFixed(0)}%`}
          />
          <Tooltip formatter={(value) => `${(value * 100).toFixed(1)}%`} />
          <Legend />
          <Line
            type="monotone"
            dataKey="propC"
            stroke="#007bff"
            name="% Altruists"
          />
          <Line
            type="monotone"
            dataKey="propD"
            stroke="#ff0000"
            name="% Egoists"
          />
          {showHalfway && (
            <Line
              type="monotone"
              dataKey="propH"
              stroke="#00cc00"
              name="% Halfway"
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TrendChart;
