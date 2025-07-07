"use client";

import { SendOutlined, UserOutlined, RobotOutlined } from "@ant-design/icons";
import { Card, message, Spin } from "antd";
import { useState, useRef, useEffect } from "react";
import { ChatMessage, ChatRequest, ChatResponse, NotepadProps } from "../types";
import { BACKEND_BASE_URL } from "../constants";

export default function Notepad({ selectedPdf }: NotepadProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messageApi, contextHolder] = message.useMessage();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    if (!selectedPdf) {
      messageApi.error("Please upload a PDF first before asking questions.");
      return;
    }

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: inputMessage.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const chatRequest: ChatRequest = {
        filename: selectedPdf,
        message: userMessage.content,
      };

      const response = await fetch(`${BACKEND_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(chatRequest),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to get response");
      }

      const data: ChatResponse = await response.json();

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      messageApi.error(
        error instanceof Error ? error.message : "Failed to send message",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <>
      {contextHolder}
      <div className="flex min-h-0 flex-1 flex-col p-6">
        <Card
          title="Chat"
          className="flex min-h-0 flex-1 flex-col"
          styles={{
            body: {
              padding: 0,
              display: "flex",
              flexDirection: "column",
              height: "100%",
              minHeight: 0,
            },
          }}
        >
          {/* Messages Container */}
          <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-4">
            {messages.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                <p className="mb-4">
                  This is your notebook. Ask questions about your sources,
                  generate ideas, or start writing. The AI will use your
                  selected sources to ground its responses.
                </p>
                {selectedPdf && (
                  <p className="mb-4">
                    Current PDF:{" "}
                    <span className="font-semibold">{selectedPdf}</span>
                  </p>
                )}
                <p>
                  Try asking:{" "}
                  <span className="text-gray-600 italic">
                    "Summarize the key findings from this document"
                  </span>
                </p>
              </div>
            ) : (
              <>
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex gap-3 ${
                      msg.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    {/* User Messages - Right Side */}
                    {msg.role === "user" ? (
                      <div className="flex max-w-[70%] flex-row-reverse gap-3">
                        <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-600 text-white">
                          <UserOutlined className="text-xs" />
                        </div>
                        <div className="rounded-2xl bg-blue-600 p-3 text-white shadow-sm">
                          <div className="break-words whitespace-pre-wrap">
                            {msg.content}
                          </div>
                          <div className="mt-1 text-xs text-blue-100">
                            {formatTimestamp(msg.timestamp)}
                          </div>
                        </div>
                      </div>
                    ) : (
                      /* Assistant Messages - Left Side */
                      <div className="flex max-w-[70%] gap-3">
                        <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-green-100 text-green-600">
                          <RobotOutlined className="text-xs" />
                        </div>
                        <div className="rounded-2xl border border-gray-200 bg-white p-3 text-gray-800 shadow-sm">
                          <div className="break-words whitespace-pre-wrap">
                            {msg.content}
                          </div>
                          <div className="mt-1 text-xs text-gray-500">
                            {formatTimestamp(msg.timestamp)}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex justify-start gap-3">
                    <div className="flex max-w-[70%] gap-3">
                      <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-green-100 text-green-600">
                        <RobotOutlined className="text-xs" />
                      </div>
                      <div className="rounded-2xl border border-gray-200 bg-white p-3 shadow-sm">
                        <div className="flex items-center gap-2">
                          <Spin size="small" />
                          <span className="text-gray-600">
                            AI is thinking...
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input Bar - Fixed at bottom */}
          <div className="flex-shrink-0 border-t bg-white p-4">
            <div className="relative">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={
                  selectedPdf
                    ? "Ask a follow-up or start a new topic..."
                    : "Please upload a PDF first..."
                }
                disabled={!selectedPdf || isLoading}
                className="w-full rounded-full border border-gray-300 p-3 pr-12 focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:bg-gray-100"
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || !selectedPdf || isLoading}
                className="absolute inset-y-0 right-0 flex w-12 items-center justify-center text-gray-400 transition-colors hover:text-blue-600 disabled:text-gray-300"
              >
                <SendOutlined className="text-lg" />
              </button>
            </div>
            {!selectedPdf && (
              <p className="mt-2 text-center text-sm text-gray-500">
                Upload a PDF to start chatting with your document
              </p>
            )}
          </div>
        </Card>
      </div>
    </>
  );
}
