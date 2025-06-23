"use client";

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { type TreeNode } from '@/lib/files';
import { Folder, FileText, File as FileIcon } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

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

export function FileTree({ nodes, level = 0 }: FileTreeProps) {
  const pathname = usePathname();

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

        if (node.type === 'directory') {
          return (
            <AccordionItem value={node.path} key={node.path} className="border-none">
              <AccordionTrigger className="py-1 px-2 rounded-md hover:bg-sidebar-accent text-sm justify-start">
                <div className="flex items-center gap-2">
                  {getIcon(node)}
                  <span className="truncate">{node.name}</span>
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
                isActive && "bg-sidebar-accent text-sidebar-accent-foreground"
              )}
            >
              <Link href={url}>
                {getIcon(node)}
                <span className="truncate">{node.name}</span>
              </Link>
            </Button>
          </li>
        );
      })}
    </Accordion>
  );
}
