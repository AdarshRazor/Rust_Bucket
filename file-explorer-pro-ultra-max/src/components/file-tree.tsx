"use client";

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { type TreeNode } from '@/lib/files';
import { Folder, FileText, File as FileIcon } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { useColorModeStore } from '@/lib/color-mode-store';

interface FileTreeProps {
  nodes: TreeNode[];
  level?: number;
}

function getIcon(node: TreeNode) {
  if (node.type === 'directory') {
    return <Folder className="h-4 w-4" />;
  }
  if (node.name.endsWith('.md')) {
    return <FileText className="h-4 w-4" />;
  }
  if (node.name.endsWith('.pdf')) {
    return <FileIcon className="h-4 w-4" />;
  }
  return <FileIcon className="h-4 w-4" />;
}

// Helper to get color class based on folder level
function getLevelColor(level: number) {
  const colors = [
    'text-blue-600', // root
    'text-green-600', // 1st subfolder
    'text-purple-600', // 2nd subfolder
    'text-pink-600', // 3rd subfolder
    'text-yellow-600', // 4th subfolder
    'text-red-600', // 5th subfolder
  ];
  return colors[level % colors.length];
}

export function FileTree({ nodes, level = 0 }: FileTreeProps) {
  const pathname = usePathname();
  const folderWise = useColorModeStore((state) => state.folderWise);

  const getActiveAccordionItems = React.useCallback((nodes: TreeNode[], currentPath: string): string[] => {
    let activeItems: string[] = [];
    for (const node of nodes) {
      if (node.type === 'directory' && currentPath.startsWith(`/view/${node.path}`)) {
        activeItems.push(node.path);
        activeItems = [...activeItems, ...getActiveAccordionItems(node.children, currentPath)];
      }
    }
    return activeItems;
  }, []);

  const defaultValues = React.useMemo(() => getActiveAccordionItems(nodes, pathname), [pathname, nodes, getActiveAccordionItems]);

  if (!nodes || nodes.length === 0) {
    return null;
  }
  
  return (
    <Accordion type="multiple" defaultValue={defaultValues} className="w-full">
      {nodes.map((node) => {
        const url = `/view/${node.path}`;
        const isActive = pathname === url;
        const colorClass = folderWise ? getLevelColor(level) : undefined;

        if (node.type === 'directory') {
          return (
            <AccordionItem value={node.path} key={node.path} className="border-none">
              <AccordionTrigger className="py-1 px-2 rounded-md hover:bg-sidebar-accent text-sm justify-start">
                <div className="flex items-center gap-2">
                  {getIcon(node)}
                  <span className={cn('truncate', colorClass)}>{node.name}</span>
                </div>
              </AccordionTrigger>
              <AccordionContent className="pb-0 pl-4">
                <FileTree nodes={node.children} level={level + 1} />
              </AccordionContent>
            </AccordionItem>
          );
        }

        return (
          <li key={node.path} className="list-none">
            <Button
              asChild
              variant="ghost"
              size="sm"
              className={cn(
                "w-full justify-start gap-2 px-2",
                isActive && "bg-primary text-white font-bold ring-2 ring-primary ring-offset-2 ring-offset-sidebar-accent shadow-lg"
              )}
            >
              <Link href={url}>
                {getIcon(node)}
                <span className={cn('truncate', colorClass)}>{node.name}</span>
              </Link>
            </Button>
          </li>
        );
      })}
    </Accordion>
  );
}
