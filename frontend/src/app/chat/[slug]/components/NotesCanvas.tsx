"use client";

import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import { DUMMY_MARKDOWN } from "../constants";

export function NotesCanvas() {
  return (
    <div className="bg-background flex flex-col h-full">
      {/* Right Section - Canvas for Notes */}
      <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
        <h2 className="text-xl font-bold text-foreground mb-4">
          Video Notes Canvas
        </h2>
        <div className="prose dark:prose-invert max-w-none bg-card p-6 rounded-lg border border-border shadow-sm">
          <ReactMarkdown rehypePlugins={[rehypeRaw]}>
            {DUMMY_MARKDOWN}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
} 