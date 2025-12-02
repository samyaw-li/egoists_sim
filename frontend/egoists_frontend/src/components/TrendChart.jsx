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

function TrendChart({ results }) {
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
              value: "Average Payoff",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="cumulative_altruist"
            stroke="#007bff"
            name="Altruists (Cumulative)"
          />
          <Line
            type="monotone"
            dataKey="cumulative_egoist"
            stroke="#ff0000"
            name="Egoists (Cumulative)"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TrendChart;
