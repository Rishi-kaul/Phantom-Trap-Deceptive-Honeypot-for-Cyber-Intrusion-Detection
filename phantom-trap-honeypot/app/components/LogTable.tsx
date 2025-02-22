interface LogProps {
    logs: { timestamp: string; ip: string; username: string; password: string }[];
  }
  
  export default function LogTable({ logs }: LogProps) {
    return (
      <div className="bg-gray-800 p-4 rounded-lg mt-6">
        <h2 className="text-xl font-semibold mb-2">Attack Logs</h2>
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="p-2">Timestamp</th>
              <th className="p-2">IP</th>
              <th className="p-2">Username</th>
              <th className="p-2">Password</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index} className="border-b border-gray-700">
                <td className="p-2">{new Date(log.timestamp).toLocaleString()}</td>
                <td className="p-2">{log.ip}</td>
                <td className="p-2">{log.username}</td>
                <td className="p-2">{log.password}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  