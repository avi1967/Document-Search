import { useState } from "react";
import Answer from "./components/Answer";
import PDFViewer from "./components/PDFViewer";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [activePdf, setActivePdf] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [status, setStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [error, setError] = useState(null);

  async function uploadPDF(file) {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading document...");
    setError(null);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setUploadedFile(data.file);
      setStatus(`Successfully uploaded: ${data.file}`);
      
      // Auto-preview uploaded PDF immediately
      setActivePdf({ file: data.file });
      setPageNumber(1);
    } catch (err) {
      setStatus("");
      setError("Failed to upload file. Please ensure the backend server is running on port 8000.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  async function askQuestion() {
    if (!question.trim()) return;
    setStatus("Analyzing context...");
    setError(null);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error("Query failed");

      const data = await res.json();
      setResponse(data);
      setStatus("");
      
      // If there are citations, open/highlight the first citation's PDF
      if (data.citations && data.citations.length > 0) {
        setActivePdf({ file: data.citations[0].document });
        setPageNumber(data.citations[0].page);
      }
    } catch (err) {
      setStatus("");
      setError("Failed to fetch response. Please ensure the backend server is running on port 8000.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      uploadPDF(e.dataTransfer.files[0]);
    }
  };

  const handleCitationClick = (documentName, page) => {
    setActivePdf({ file: documentName });
    setPageNumber(page);
  };

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <div className="logo-container">
          <span className="logo-icon">🔮</span>
          <div className="logo-text">
            <h1>Document Search</h1>
            <p>High-Fidelity Document Search System</p>
          </div>
        </div>
        <div className="header-badge">
          <span className="pulse-dot"></span>
          <span>System Active</span>
        </div>
      </header>

      <div className="dashboard-grid">
        {/* Sidebar Controls */}
        <aside className="sidebar-panel">
          {/* Card 1: Upload */}
          <div className="glass-card">
            <h2 className="card-title">
              <span>📥</span> Document Upload
            </h2>
            <div
              className={`upload-zone ${isDragging ? "dragging" : ""}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById("filePicker").click()}
            >
              <input
                id="filePicker"
                type="file"
                className="file-input"
                accept="application/pdf"
                onChange={(e) => uploadPDF(e.target.files[0])}
              />
              <span className="upload-icon">📄</span>
              <p className="upload-text">Drag & drop your PDF here</p>
              <p className="upload-subtext">or click to browse local files</p>
            </div>

            {uploadedFile && (
              <div className="file-list">
                <div className="uploaded-file-item">
                  <span className="success-dot">✓</span>
                  <span className="file-name-span">{uploadedFile}</span>
                </div>
              </div>
            )}
          </div>

          {/* Card 2: Question Input */}
          <div className="glass-card query-box">
            <h2 className="card-title">
              <span>💬</span> Query Console
            </h2>
            <textarea
              className="query-textarea"
              placeholder="Ask a question about the document..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  askQuestion();
                }
              }}
            />
            <button
              className="search-button"
              onClick={askQuestion}
              disabled={isLoading || !question.trim()}
            >
              {isLoading ? (
                <>
                  <span className="loading-spinner"></span>
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <span>✨</span>
                  <span>Analyze</span>
                </>
              )}
            </button>

            {status && (
              <div className="status-container">
                {isLoading && <span className="loading-spinner"></span>}
                <span>{status}</span>
              </div>
            )}
          </div>
        </aside>

        {/* Main Workspace Display */}
        <main className="main-workspace">
          {error ? (
            <div className="glass-card error-state">
              <span className="error-icon">⚠️</span>
              <h3>System Error</h3>
              <p>{error}</p>
            </div>
          ) : !response && !activePdf ? (
            <div className="glass-card empty-state">
              <span className="empty-icon">📂</span>
              <h3>No Document Loaded</h3>
              <p>
                Upload a PDF file in the sidebar to start asking questions and analyzing its content with instant citations.
              </p>
            </div>
          ) : (
            <div className={activePdf ? "workspace-split" : "results-column"}>
              {/* Answer Column */}
              {response && (
                <div className="results-column">
                  <Answer
                    answer={response.answer}
                    citations={response.citations}
                    onCitationClick={handleCitationClick}
                  />
                </div>
              )}

              {/* PDF Preview Column */}
              {activePdf && (
                <div className="pdf-column">
                  <PDFViewer
                    file={activePdf.file}
                    pageNumber={pageNumber}
                    setPageNumber={setPageNumber}
                    onClose={() => setActivePdf(null)}
                  />
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
