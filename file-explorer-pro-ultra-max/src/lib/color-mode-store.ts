import { create } from 'zustand';

interface ColorModeState {
  folderWise: boolean;
  toggleFolderWise: () => void;
}

export const useColorModeStore = create<ColorModeState>((set) => ({
  folderWise: false,
  toggleFolderWise: () => set((state) => ({ folderWise: !state.folderWise })),
}));
