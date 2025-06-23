import fs from 'fs/promises';
import path from 'path';

export type FileNode = {
  name: string;
  path: string;
  type: 'file';
};

export type DirectoryNode = {
  name: string;
  path: string;
  type: 'directory';
  children: TreeNode[];
};

export type TreeNode = FileNode | DirectoryNode;

const contentDir = path.join(process.cwd(), 'content');
const validExtensions = ['.md', '.pdf'];

async function getTree(dir: string, relativePath: string): Promise<TreeNode[]> {
  const dirents = await fs.readdir(dir, { withFileTypes: true });
  const children: TreeNode[] = [];

  for (const dirent of dirents) {
    const fullPath = path.join(dir, dirent.name);
    const newRelativePath = path.join(relativePath, dirent.name);
    if (dirent.isDirectory()) {
      children.push({
        name: dirent.name,
        path: newRelativePath,
        type: 'directory',
        children: await getTree(fullPath, newRelativePath),
      });
    } else if (validExtensions.includes(path.extname(dirent.name).toLowerCase())) {
      children.push({
        name: dirent.name,
        path: newRelativePath,
        type: 'file',
      });
    }
  }

  // Sort directories first, then files, all alphabetically
  children.sort((a, b) => {
    if (a.type === 'directory' && b.type === 'file') return -1;
    if (a.type === 'file' && b.type === 'directory') return 1;
    return a.name.localeCompare(b.name);
  });
  return children;
}

export async function getFileTree(): Promise<TreeNode[]> {
    try {
        await fs.access(contentDir);
        return await getTree(contentDir, '');
    } catch (error) {
        console.warn("Content directory not found. Creating 'content'. Please add your files there.");
        try {
            await fs.mkdir(contentDir, { recursive: true });
        } catch (mkdirError) {
            console.error("Failed to create content directory:", mkdirError);
        }
        return [];
    }
}


export async function getFileContent(slug: string[]): Promise<string> {
    const filePath = path.join(contentDir, ...slug);
    try {
        const content = await fs.readFile(filePath, 'utf-8');
        return content;
    } catch (error) {
        console.error(`Error reading file: ${filePath}`, error);
        return "Error: Could not read file content.";
    }
}
