"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Chart from "../components/Chart";
import LogTable from "../components/LogTable";

export default function Home() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    axios.get("http://localhost:3000/api/logs")
      .then(response => setLogs(response.data))
      .catch(() => {
        setError(true);
        console.warn("⚠️ Backend is unreachable. Using fallback data.");
        
        setLogs([
          { timestamp: new Date().toISOString(), ip: "192.168.1.1", username: "admin", password: "123456" },
          { timestamp: new Date().toISOString(), ip: "203.0.113.5", username: "root", password: "toor" }
        ]);
      });
  }, []);

  return (
    <div>
      {error && <p className="bg-red-500 p-2 text-white rounded">⚠️ Showing fallback data.</p>}
      <Chart logs={logs} />
      <LogTable logs={logs} />
    </div>
  );
}
