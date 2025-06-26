"use client";

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function renderCsvTable(content: string) {
  const rows = content.trim().split(/\r?\n/).map(row => row.split(','));
  return (
    <div className="overflow-auto">
      <table className="table-auto border-collapse border border-gray-300 w-full text-sm">
        <tbody>
          {rows.map((cols, i) => (
            <tr key={i} className={i === 0 ? 'font-bold bg-muted' : ''}>
              {cols.map((col, j) => (
                <td key={j} className="border border-gray-300 px-2 py-1 whitespace-pre">{col}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function renderJson(content: string) {
  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch {
    return <pre className="text-red-500">Invalid JSON</pre>;
  }
  return (
    <div className="overflow-auto max-h-[70vh] min-h-[400px]">
      <pre className="bg-muted p-4 rounded text-xs overflow-auto whitespace-pre-wrap min-h-[400px]">{JSON.stringify(parsed, null, 2)}</pre>
    </div>
  );
}

interface MarkdownPreviewProps {
  content: string;
  fileType?: string;
}

export function MarkdownPreview({ content, fileType }: MarkdownPreviewProps) {
  if (fileType === 'csv') {
    return renderCsvTable(content);
  }
  if (fileType === 'json') {
    return renderJson(content);
  }
  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}
