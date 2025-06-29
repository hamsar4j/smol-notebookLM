"use client";

import { PlayCircleOutlined, SoundOutlined } from "@ant-design/icons";
import { PlayerProps } from "../types";
import { useState } from "react";
import { BACKEND_BASE_URL } from "../constants";

export default function Player({ selectedSource }: PlayerProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const handleGeneratePodcast = async () => {
    if (!selectedSource) {
      setError("Please select a source first.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setAudioUrl(null);

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/generate-audio`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename: selectedSource.name }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to generate podcast.");
      }

      const audioBlob = await response.blob();
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <aside className="flex w-1/4 flex-col gap-4 border-l bg-white p-6">
      <h2 className="text-xl font-bold">Podcast Player</h2>
      <div className="mt-4 flex flex-col items-center gap-4 text-center">
        <div className="flex h-48 w-48 items-center justify-center rounded-lg bg-gray-100">
          <SoundOutlined
            className="text-gray-400"
            style={{ fontSize: "64px" }}
          />
        </div>
        <h3 className="text-lg font-semibold">
          {selectedSource ? selectedSource.name : "AI-Generated Podcast"}
        </h3>
        <p className="text-sm text-gray-500">
          {audioUrl
            ? "Your podcast is ready."
            : "Your generated audio will appear here."}
        </p>
        {audioUrl && (
          <audio controls autoPlay src={audioUrl} className="mt-4 w-full" />
        )}
        {error && <p className="text-sm text-red-500">{error}</p>}
        <button
          onClick={handleGeneratePodcast}
          disabled={!selectedSource || isLoading}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-md bg-green-600 px-3 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
        >
          <PlayCircleOutlined />
          {isLoading ? "Generating..." : "Generate Podcast"}
        </button>
      </div>
    </aside>
  );
}
