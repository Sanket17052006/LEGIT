import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

function Scan() {
  const [mode, setMode] = useState('upload'); // 'upload' or 'camera'
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  const webcamRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setPreview(imageSrc);
    setResult(null);
    setError(null);
  }, [webcamRef]);

  const submitScan = async () => {
    if (!preview) {
      setError('Please upload or capture an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let formData = new FormData();
      
      if (mode === 'camera') {
        // Convert base64 to blob for camera capture
        const res = await fetch(preview);
        const blob = await res.blob();
        formData.append('file', blob, 'capture.jpg');
      } else {
        const fileInput = fileInputRef.current;
        if (fileInput && fileInput.files[0]) {
          formData.append('file', fileInput.files[0]);
        }
      }

      const response = await axios.post('/api/scans/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error processing scan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Scan Product</h1>

      {/* Mode Toggle */}
      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setMode('upload')}
          className={`px-4 py-2 rounded-md font-medium transition-colors ${
            mode === 'upload'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Upload Image
        </button>
        <button
          onClick={() => setMode('camera')}
          className={`px-4 py-2 rounded-md font-medium transition-colors ${
            mode === 'camera'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Live Camera
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            {mode === 'upload' ? 'Upload Product Image' : 'Capture Product Image'}
          </h2>

          {mode === 'upload' ? (
            <div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current.click()}
                className="w-full border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-500 transition-colors"
              >
                <div className="text-gray-500">
                  <svg className="mx-auto h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p>Click to upload product image</p>
                  <p className="text-sm">JPG, PNG, WEBP up to 10MB</p>
                </div>
              </button>
            </div>
          ) : (
            <div>
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="w-full rounded-lg"
                videoConstraints={{ facingMode: 'environment' }}
              />
              <button
                onClick={capture}
                className="mt-4 w-full bg-primary-600 text-white py-2 rounded-md hover:bg-primary-700"
              >
                Capture
              </button>
            </div>
          )}

          {/* Preview */}
          {preview && (
            <div className="mt-4">
              <img src={preview} alt="Preview" className="w-full rounded-lg shadow" />
            </div>
          )}

          {/* Submit Button */}
          <button
            onClick={submitScan}
            disabled={!preview || loading}
            className={`mt-4 w-full py-3 rounded-md font-semibold transition-colors ${
              preview && !loading
                ? 'bg-green-600 text-white hover:bg-green-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {loading ? 'Processing...' : 'Check Compliance'}
          </button>

          {error && (
            <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
              {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Compliance Results</h2>

          {!result ? (
            <p className="text-gray-500 text-center py-8">
              Upload or capture a product image to see compliance results
            </p>
          ) : (
            <div>
              {/* Status Badge */}
              <div className={`mb-4 p-3 rounded-md text-center font-semibold ${
                result.compliance_status === 'compliant'
                  ? 'bg-green-100 text-green-800'
                  : result.compliance_status === 'non_compliant'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {result.compliance_status === 'compliant'
                  ? 'COMPLIANT'
                  : result.compliance_status === 'non_compliant'
                  ? 'NON-COMPLIANT'
                  : 'PARTIAL COMPLIANCE'}
              </div>

              {/* Checks */}
              <div className="space-y-3">
                {result.checks?.map((check) => (
                  <div
                    key={check.rule_id}
                    className={`p-3 rounded-md border-l-4 ${
                      check.is_compliant
                        ? 'border-green-500 bg-green-50'
                        : check.severity === 'error'
                        ? 'border-red-500 bg-red-50'
                        : 'border-yellow-500 bg-yellow-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sm">{check.rule_id}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        check.is_compliant ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                      }`}>
                        {check.is_compliant ? 'Pass' : 'Fail'}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{check.rule_name}</p>
                    <p className="text-xs text-gray-500 mt-1">{check.details}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Scan;
