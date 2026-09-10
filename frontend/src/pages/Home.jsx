import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Legal Metrology Compliance Checker
        </h1>
        <p className="text-lg text-gray-600">
          Automated compliance checking for Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-12">
        <Link
          to="/scan"
          className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border-l-4 border-primary-500"
        >
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Scan Product</h2>
          <p className="text-gray-600">
            Upload or capture a product image to check compliance with Legal Metrology rules.
          </p>
        </Link>

        <Link
          to="/dashboard"
          className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border-l-4 border-green-500"
        >
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Dashboard</h2>
          <p className="text-gray-600">
            View compliance statistics and monitor enforcement activities.
          </p>
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">About</h2>
        <p className="text-gray-600 mb-4">
          This system helps enforcement agencies check compliance of packaged commodities
          under the Legal Metrology Act, 2009 and Legal Metrology (Packaged Commodities) Rules, 2011.
        </p>
        <h3 className="font-semibold text-gray-700 mb-2">Checks Performed:</h3>
        <ul className="list-disc list-inside text-gray-600 space-y-1">
          <li>Manufacturer/Packer/Importer name and address</li>
          <li>Net quantity declaration</li>
          <li>Maximum Retail Price (MRP)</li>
          <li>Manufacture/Packing date</li>
          <li>Consumer care details</li>
          <li>Country of origin</li>
          <li>Expiry/Best before date</li>
        </ul>
      </div>
    </div>
  );
}

export default Home;
