import { SendOutlined } from "@ant-design/icons";
import { Card } from "antd";

export default function Notepad() {
  return (
    <main className="flex flex-1 flex-col p-6">
      <Card title="Chat" className="flex flex-1 flex-col">
        <div className="flex-1 overflow-y-auto p-6">
          <div>
            <p>
              This is your notebook. Ask questions about your sources, generate
              ideas, or start writing. The AI will use your selected sources to
              ground its responses.
            </p>
            <p>
              Try asking:{" "}
              <span className="text-gray-600 italic">
                "Summarize the key findings from Mixture-of-Agents.pdf"
              </span>
            </p>
          </div>
        </div>

        {/* Input Bar */}
        <div className="border-t p-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Ask a follow-up or start a new topic..."
              className="w-full rounded-full border p-4 focus:border-none focus:ring-1 focus:ring-blue-500"
            />
            <button className="absolute inset-y-0 right-0 flex w-12 items-center justify-center text-gray-500 hover:text-blue-600">
              <SendOutlined size={20} />
            </button>
          </div>
        </div>
      </Card>
    </main>
  );
}
