export type Source = {
  name: string;
  size: number;
  type: string;
};

export interface SourcesProps {
  sources: Source[];
  setSources: React.Dispatch<React.SetStateAction<Source[]>>;
  selectedSource: Source | null;
  setSelectedSource: (source: Source | null) => void;
}

export interface PlayerProps {
  selectedSource: Source | null;
}
