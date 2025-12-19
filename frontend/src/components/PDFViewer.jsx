import { Document, Page } from "react-pdf";
import { pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = 
  `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function PDFViewer({ file, page }) {
  return (
    <div className="pdf">
      <h4>PDF Preview</h4>
      <Document file={`http://127.0.0.1:8000/pdf/${file}`}>
        <Page pageNumber={page} />
      </Document>
    </div>
  );
}
