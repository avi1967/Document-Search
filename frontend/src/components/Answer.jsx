export default function Answer({ answer, citations = [], setPdf }) {
  return (
    <div className="answer">
      <h3>Answer</h3>
      <p>{answer}</p>

      {citations.length > 0 && (
        <>
          <h4>Sources</h4>
          {citations.map((c, i) => (
            <div key={i}>
              <span
                className="citation"
                onClick={() => setPdf({ file: c.document, page: c.page })}
              >
                {c.document} (page {c.page})
              </span>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
