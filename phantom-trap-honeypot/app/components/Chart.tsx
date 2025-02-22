import { Line } from "react-chartjs-2";

interface ChartProps {
  logs: { timestamp: string }[];
}

export default function Chart({ logs }: ChartProps) {
  const timestamps = logs.map((log) => new Date(log.timestamp).toLocaleTimeString());

  const data = {
    labels: timestamps,
    datasets: [{
      label: "SSH Attacks",
      data: logs.map((_, index) => index + 1),
      borderColor: "rgb(255, 99, 132)",
      borderWidth: 2,
    }],
  };

  return <Line data={data} />;
}
