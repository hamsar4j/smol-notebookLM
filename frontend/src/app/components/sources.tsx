"use client";

import { useState, useRef } from "react";
import { PlusOutlined, FileTextOutlined } from "@ant-design/icons";
import { Card } from "antd";
import { BACKEND_BASE_URL } from "../constants";
import { SourcesProps } from "../types";

export default function Sources({
  sources,
  setSources,
  selectedSource,
  setSelectedSource,
}: SourcesProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleAddSourcesClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      return;
    }

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/upload-pdf`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to upload file.");
      }
      const data = await response.json();
      console.log("File uploaded successfully:", data);
      const newSource = {
        name: file.name,
        size: file.size,
        type: file.type,
      };
      setSources([...sources, newSource]);
    } catch (err) {
      setError("Failed to upload source.");
    } finally {
      setIsLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  return (
    // {/* Left Panel: Sources */}
    <aside className="flex w-1/3 flex-col p-6">
      <Card
        title="Sources"
        variant="borderless"
        className="flex flex-1 flex-col"
      >
        <div className="flex items-center justify-between p-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept="application/pdf"
            className="hidden"
          />
          <button
            onClick={handleAddSourcesClick}
            disabled={isLoading}
            className="flex items-center gap-2 rounded-full bg-black px-4 py-2 text-sm text-white hover:opacity-70"
          >
            <PlusOutlined />
            {isLoading ? "Uploading..." : "Add Source"}
          </button>
        </div>
        {error && <p className="text-sm text-red-500">{error}</p>}
        <div className="flex-1 space-y-2 overflow-y-auto p-2">
          {/* Source Item Card */}
          {sources.length > 0 ? (
            sources.map((source, index) => (
              <div
                key={index}
                onClick={() => setSelectedSource(source)}
                className={`cursor-pointer rounded-lg border bg-gray-100 p-4 shadow-md${
                  selectedSource?.name === source.name
                    ? "border border-blue-500"
                    : "border-gray-100 hover:opacity-70"
                }`}
              >
                <div className="flex items-center gap-4">
                  <FileTextOutlined />
                  <div className="flex-1">
                    <h3 className="font-semibold">{source.name}</h3>
                    <p className="text-sm text-gray-500">
                      {Math.round(source.size / 1024)} KB
                    </p>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="py-10 text-center text-gray-500">
              <p>No sources added yet.</p>
              <p className="text-sm">Click "Add Source" to upload a PDF.</p>
            </div>
          )}
        </div>
      </Card>
    </aside>
  );
}
