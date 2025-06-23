import { getFileTree } from '@/lib/files';
import { FileTree } from '@/components/file-tree';
import { SidebarProvider, Sidebar, SidebarHeader, SidebarContent, SidebarInset, SidebarTrigger, SidebarResizer, SidebarFooter } from '@/components/ui/sidebar';
import { ScrollArea } from '@/components/ui/scroll-area';
import { FileCode2 } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';

export default async function MainLayout({ children }: { children: React.ReactNode }) {
  const fileTree = await getFileTree();

  return (
    <SidebarProvider defaultOpen>
      <div className="flex min-h-screen">
        <Sidebar className="border-r">
          <SidebarResizer />
          <SidebarHeader className="p-4">
            <div className="flex items-center gap-2">
                <FileCode2 className="h-6 w-6 text-primary" />
                <h1 className="text-xl font-semibold font-headline">File Explorer Pro</h1>
            </div>
          </SidebarHeader>
          <SidebarContent className="p-2">
            <ScrollArea className="h-full">
              <FileTree nodes={fileTree} />
            </ScrollArea>
          </SidebarContent>
          <SidebarFooter>
            <ThemeToggle />
          </SidebarFooter>
        </Sidebar>
        <SidebarInset className="flex-1 flex flex-col">
          <header className="flex items-center justify-between p-4 border-b md:justify-end">
            <SidebarTrigger className="md:hidden"/>
          </header>
          <main className="flex-1 p-4 md:p-6 overflow-auto flex flex-col">
            {children}
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
}
