import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

// Configure pdfjs worker source
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function PDFViewer({ file, pageNumber, setPageNumber, onClose }) {
  const [numPages, setNumPages] = useState(null);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    if (!pageNumber || pageNumber > numPages) {
      setPageNumber(1);
    }
  }

  const handlePrevPage = () => {
    if (pageNumber > 1) {
      setPageNumber(pageNumber - 1);
    }
  };

  const handleNextPage = () => {
    if (pageNumber < numPages) {
      setPageNumber(pageNumber + 1);
    }
  };

  return (
    <div className="pdf-viewer-card">
      <div className="pdf-viewer-header">
        <div className="pdf-title-info">
          <span className="pdf-icon">📄</span>
          <h3>{file}</h3>
        </div>
        <button className="pdf-close-btn" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="pdf-document-scroll">
        <Document
          file={`http://127.0.0.1:8000/pdf/${file}`}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={<div className="pdf-loading">Loading PDF file...</div>}
          error={<div className="pdf-error">Failed to load PDF preview.</div>}
        >
          <Page 
            pageNumber={pageNumber || 1} 
            renderTextLayer={false}
            renderAnnotationLayer={false}
            scale={1.2}
          />
        </Document>
      </div>

      {numPages && (
        <div className="pdf-viewer-footer">
          <button 
            onClick={handlePrevPage} 
            disabled={pageNumber <= 1}
            className="pdf-nav-btn"
          >
            ← Prev
          </button>
          <span className="pdf-page-indicator">
            Page {pageNumber || 1} of {numPages}
          </span>
          <button 
            onClick={handleNextPage} 
            disabled={pageNumber >= numPages}
            className="pdf-nav-btn"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
