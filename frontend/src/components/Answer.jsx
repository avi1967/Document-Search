export default function Answer({ answer, citations = [], onCitationClick }) {
  return (
    <div className="answer-card">
      <div className="answer-header">
        <span className="sparkle-icon">✨</span>
        <h3>Generated Response</h3>
      </div>
      <div className="answer-body">
        <p className="answer-text">{answer}</p>
      </div>

      {citations && citations.length > 0 && (
        <div className="sources-section">
          <h4>Reference Citations</h4>
          <div className="citations-grid">
            {citations.map((c, i) => (
              <button
                key={i}
                className="citation-pill"
                onClick={() => onCitationClick(c.document, c.page)}
                title={`Click to view page ${c.page} of ${c.document}`}
              >
                <span className="file-icon">📄</span>
                <span className="file-name">{c.document}</span>
                <span className="page-badge">Page {c.page}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
