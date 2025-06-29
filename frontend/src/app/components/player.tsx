import { PlayCircleOutlined, SoundOutlined } from "@ant-design/icons";

export default function Player() {
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
        <h3 className="text-lg font-semibold">AI-Generated Podcast</h3>
        <p className="text-sm text-gray-500">
          Your generated audio will appear here.
        </p>
        <audio controls className="mt-4 w-full">
          {/* This will be loaded dynamically */}
          {/* <source src="null" type="audio/wav" /> */}
          Your browser does not support the audio element.
        </audio>
        <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-md bg-green-600 px-3 py-2 text-sm font-medium text-white hover:bg-green-700">
          <PlayCircleOutlined />
          Generate Podcast
        </button>
      </div>
    </aside>
  );
}
