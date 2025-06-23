"use client";

interface PdfViewerProps {
  path: string;
}

export function PdfViewer({ path }: PdfViewerProps) {
  return (
    <div className="w-full h-full flex-grow rounded-lg overflow-hidden border">
      <iframe src={path} title="PDF Viewer" className="w-full h-full border-none" />
    </div>
  );
}
