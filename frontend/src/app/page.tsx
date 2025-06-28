export default function Home() {
  return (
    <div className="flex flex-col h-screen bg-gray-50 font-sans text-gray-900">
      {/* Header */}
      <header className="flex items-center justify-between h-16 px-6 border-b bg-white shrink-0">
        <h1 className="text-lg font-semibold">Smol NotebookLM</h1>
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm font-bold text-gray-600">
          H
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel: Sources */}
        <aside className="w-1/3 border-r bg-white p-6 flex flex-col gap-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Sources</h2>
            <button className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
              {/* <Plus size={16} /> */}
              Add Source
            </button>
          </div>
          <div className="flex flex-col gap-3 overflow-y-auto">
            {/* Source Item Card */}
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <div className="flex items-center gap-3">
                {/* <FileText className="text-blue-500" size={20} /> */}
                <div className="flex-1">
                  <h3 className="font-semibold">Mixture-of-Agents.pdf</h3>
                  <p className="text-sm text-gray-500">12 pages</p>
                </div>
              </div>
            </div>
            {/* Source Item Card */}
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <div className="flex items-center gap-3">
                {/* <FileText className="text-green-500" size={20} /> */}
                <div className="flex-1">
                  <h3 className="font-semibold">Research_Notes.docx</h3>
                  <p className="text-sm text-gray-500">5 pages</p>
                </div>
              </div>
            </div>
          </div>
        </aside>

        {/* Right Panel: Notepad */}
        <main className="flex-1 flex flex-col">
          <div className="flex-1 p-8 overflow-y-auto">
            <div className="prose prose-stone lg:prose-lg max-w-full">
              <h2>Untitled Note</h2>
              <p>
                This is your notebook. Ask questions about your sources,
                generate ideas, or start writing. The AI will use your selected
                sources to ground its responses.
              </p>
              <p>
                Try asking:{" "}
                <span className="italic text-gray-600">
                  "Summarize the key findings from Mixture-of-Agents.pdf"
                </span>
              </p>
            </div>
          </div>

          {/* Input Bar */}
          <div className="p-4 border-t bg-white">
            <div className="relative">
              <input
                type="text"
                placeholder="Ask a follow-up or start a new topic..."
                className="w-full p-4 pr-14 text-base border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button className="absolute inset-y-0 right-0 flex items-center justify-center w-12 text-gray-500 hover:text-blue-600">
                {/* <Send size={20} /> */}
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
