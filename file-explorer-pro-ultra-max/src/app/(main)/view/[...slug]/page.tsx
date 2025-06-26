import { getFileContent } from '@/lib/files';
import { MarkdownPreview } from '@/components/markdown-preview';
import { PdfViewer } from '@/components/pdf-viewer';
import { notFound } from 'next/navigation';
import { Card } from '@/components/ui/card';

function getFileType(fileName: string) {
  if (fileName.endsWith('.md')) return 'md';
  if (fileName.endsWith('.csv')) return 'csv';
  if (fileName.endsWith('.json')) return 'json';
  return '';
}

export default async function FileViewPage({ params }: { params: { slug: string[] } }) {
  const { slug } = params;
  
  if (!slug || slug.length === 0) {
    notFound();
  }

  const fileName = slug[slug.length - 1].toLowerCase();
  const fileType = getFileType(fileName);

  if (fileType === 'md' || fileType === 'csv' || fileType === 'json') {
    const content = await getFileContent(slug);
    if (content.startsWith("Error:")) {
        notFound();
    }
    return (
      <Card className="flex-1 p-6 md:p-8 lg:p-10">
        <MarkdownPreview content={content} fileType={fileType} />
      </Card>
    );
  }

  if (fileName.endsWith('.pdf')) {
    const pdfPath = `/content/${slug.join('/')}`;
    return (
        <div className="flex-1 w-full h-full min-h-0">
             <PdfViewer path={pdfPath} />
        </div>
    );
  }

  return (
    <div className="flex items-center justify-center h-full">
      <Card className="p-8">
        <h1 className="text-2xl font-bold">Unsupported File Type</h1>
        <p className="text-muted-foreground mt-2">Cannot display this file. Please select a .md, .csv, .json, or .pdf file.</p>
      </Card>
    </div>
  );
}
