import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function History() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchScans();
  }, [filter]);

  const fetchScans = async () => {
    try {
      const url = filter === 'all' ? '/api/scans/' : `/api/scans/?status=${filter}`;
      const response = await axios.get(url);
      setScans(response.data);
    } catch (err) {
      console.error('Error fetching scans:', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteScan = async (id) => {
    if (!window.confirm('Delete this scan?')) return;
    try {
      await axios.delete(`/api/scans/${id}`);
      setScans(scans.filter((s) => s.id !== id));
    } catch (err) {
      console.error('Error deleting scan:', err);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Scan History</h1>

      {/* Filters */}
      <div className="flex space-x-4 mb-6">
        {['all', 'compliant', 'non_compliant', 'partial', 'pending'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              filter === f
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1).replace('_', ' ')}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-gray-500 text-center py-8">Loading...</p>
      ) : scans.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">No scans found</p>
          <Link to="/scan" className="text-primary-600 hover:underline">
            Scan your first product
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {scans.map((scan) => (
                <tr key={scan.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-900">#{scan.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {scan.product_name || 'Unnamed Product'}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      scan.compliance_status === 'compliant'
                        ? 'bg-green-100 text-green-800'
                        : scan.compliance_status === 'non_compliant'
                        ? 'bg-red-100 text-red-800'
                        : scan.compliance_status === 'partial'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {scan.compliance_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {new Date(scan.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-sm space-x-2">
                    <Link
                      to={`/scan`}
                      className="text-primary-600 hover:underline"
                    >
                      View
                    </Link>
                    <button
                      onClick={() => deleteScan(scan.id)}
                      className="text-red-600 hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default History;
