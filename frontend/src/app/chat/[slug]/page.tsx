"use client";

import { useState } from "react";
import {
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
} from "@/components/ui/resizable";
import { Header } from "./components/Header";
import { ChatSection } from "./components/ChatSection";
import { NotesCanvas } from "./components/NotesCanvas";
import { DEFAULT_CHAT_NAME } from "./constants";
import { Toaster } from "sonner";
import "./styles.css";

export default function Page() {
  const [message, setMessage] = useState("");
  const [chatName] = useState(DEFAULT_CHAT_NAME);

  return (
    <div className="h-screen flex flex-col bg-background antialiased font-sans">
      <Toaster position="bottom-right" />
      <Header chatName={chatName} />
      <section className="flex-1 flex overflow-hidden">
        <ResizablePanelGroup direction="horizontal" className="w-full">
          <ResizablePanel minSize={25} defaultSize={50}>
            <ChatSection message={message} setMessage={setMessage} />
          </ResizablePanel>
          <ResizableHandle className="w-2 bg-border hover:bg-border/70 transition-colors" />
          <ResizablePanel minSize={50} defaultSize={50}>
            <NotesCanvas />
          </ResizablePanel>
        </ResizablePanelGroup>
      </section>
    </div>
  );
}
