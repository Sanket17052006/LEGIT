import { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/scans/stats/dashboard');
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p className="text-center text-gray-500 py-8">Loading dashboard...</p>;
  }

  if (!stats) {
    return <p className="text-center text-gray-500 py-8">Error loading dashboard</p>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-sm font-medium text-gray-500">Total Scans</h3>
          <p className="text-3xl font-bold text-gray-800">{stats.total_scans}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <h3 className="text-sm font-medium text-gray-500">Compliant</h3>
          <p className="text-3xl font-bold text-green-600">{stats.compliant_count}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
          <h3 className="text-sm font-medium text-gray-500">Non-Compliant</h3>
          <p className="text-3xl font-bold text-red-600">{stats.non_compliant_count}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
          <h3 className="text-sm font-medium text-gray-500">Pending</h3>
          <p className="text-3xl font-bold text-yellow-600">{stats.pending_count}</p>
        </div>
      </div>

      {/* Recent Scans */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Scans</h2>
        {stats.recent_scans.length === 0 ? (
          <p className="text-gray-500 text-center py-4">No scans yet</p>
        ) : (
          <div className="space-y-3">
            {stats.recent_scans.map((scan) => (
              <div key={scan.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div>
                  <span className="font-medium">#{scan.id}</span>
                  <span className="ml-3 text-gray-600">{scan.product_name || 'Unnamed'}</span>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  scan.compliance_status === 'compliant'
                    ? 'bg-green-100 text-green-800'
                    : scan.compliance_status === 'non_compliant'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {scan.compliance_status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
