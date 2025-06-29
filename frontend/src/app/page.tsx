"use client";

import Sources from "./components/sources";
import Notepad from "./components/notepad";
import Player from "./components/player";
import { useState } from "react";
import { Source } from "./types";

export default function Home() {
  const [sources, setSources] = useState<Source[]>([]);
  const [selectedSource, setSelectedSource] = useState<Source | null>(null);

  return (
    <div className="flex h-screen flex-col font-sans text-gray-900">
      {/* Header */}
      <header className="flex h-16 shrink-0 items-center justify-between border-b bg-white px-6">
        <h1 className="text-xl">Smol NotebookLM</h1>
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-sm font-bold text-white">
          H
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel: Sources */}
        <Sources
          sources={sources}
          setSources={setSources}
          selectedSource={selectedSource}
          setSelectedSource={setSelectedSource}
        />
        {/* Middle Panel: Notepad */}
        <Notepad />
        {/* Right Panel: Podcast Player */}
        <Player selectedSource={selectedSource} />
      </div>
    </div>
  );
}
