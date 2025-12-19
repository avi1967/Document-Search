import { useState } from "react";
import Answer from "./components/Answer";
import PDFViewer from "./components/PDFViewer";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [pdf, setPdf] = useState(null);
  const [status, setStatus] = useState("");

  async function uploadPDF(file) {
    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading PDF...");

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setStatus(`Uploaded: ${data.file}`);
  }

  async function askQuestion() {
    setStatus("Thinking...");

    const res = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    setResponse(data);
    setStatus("");
  }

  return (
    <div className="container">
      <h2>📄 LLM Document Query System</h2>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => uploadPDF(e.target.files[0])}
      />

      <textarea
        placeholder="Ask a question about the document..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>Ask</button>

      <p>{status}</p>

      {response && (
        <Answer
          answer={response.answer}
          citations={response.citations}
          setPdf={setPdf}
        />
      )}

      {pdf && <PDFViewer file={pdf.file} page={pdf.page} />}
    </div>
  );
}

export default App;
