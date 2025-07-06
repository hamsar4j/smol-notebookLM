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

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  filename: string;
  message: string;
}

export interface ChatResponse {
  response: string;
}

export interface NotepadProps {
  selectedPdf?: string;
}
