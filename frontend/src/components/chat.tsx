"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { ArrowUp, Code, Copy, Eye, Loader2, RotateCcw } from "lucide-react"
import { cn } from "@/lib/utils"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"

type Message = {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
  codeBlocks?: Array<{
    id: string
    language: string
    code: string
  }>
}

export function ChatInterface() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<"preview" | "code">("preview")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content:
          "I've created a simple button component using shadcn/ui. You can see the preview in the Preview tab and the code in the Code tab.",
        role: "assistant",
        timestamp: new Date(),
        codeBlocks: [
          {
            id: "code-1",
            language: "tsx",
            code: `import { Button } from "@/components/ui/button"

export default function ButtonComponent() {
  return (
    <div className="flex flex-col space-y-4 p-4">
      <h1 className="text-2xl font-bold">Button Component</h1>
      <div className="flex flex-wrap gap-4">
        <Button variant="default">Default</Button>
        <Button variant="destructive">Destructive</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link</Button>
      </div>
    </div>
  )
}`,
          },
        ],
      }
      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1000)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [input])

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  const renderCodeBlock = (codeBlock: { id: string; language: string; code: string }) => {
    return (
      <div key={codeBlock.id} className="relative mt-4 rounded-md bg-zinc-900 font-mono text-sm text-zinc-100">
        <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-2">
          <div className="text-xs text-zinc-400">{codeBlock.language}</div>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 text-zinc-400 hover:text-zinc-100"
            onClick={() => copyToClipboard(codeBlock.code)}
          >
            <Copy className="h-4 w-4" />
            <span className="sr-only">Copy code</span>
          </Button>
        </div>
        <pre className="overflow-x-auto p-4">{codeBlock.code}</pre>
      </div>
    )
  }

  return (
    <div className="flex h-full flex-col">
      <ResizablePanelGroup direction="vertical">
        <ResizablePanel defaultSize={70} minSize={30}>
          <Tabs
            defaultValue="preview"
            value={activeTab}
            onValueChange={(value) => setActiveTab(value as "preview" | "code")}
            className="flex h-full flex-col"
          >
            <div className="flex items-center justify-between border-b px-4">
              <TabsList className="h-12">
                <TabsTrigger value="preview" className="flex items-center gap-2">
                  <Eye className="h-4 w-4" />
                  Preview
                </TabsTrigger>
                <TabsTrigger value="code" className="flex items-center gap-2">
                  <Code className="h-4 w-4" />
                  Code
                </TabsTrigger>
              </TabsList>
              <div className="flex items-center gap-2">
                <Button variant="ghost" size="icon">
                  <RotateCcw className="h-4 w-4" />
                  <span className="sr-only">Reset</span>
                </Button>
              </div>
            </div>
            <TabsContent
              value="preview"
              className="flex-1 overflow-hidden p-0 data-[state=active]:flex-col data-[state=active]:flex"
            >
              <ScrollArea className="flex-1 p-4">
                <div className="mx-auto max-w-3xl">
                  {messages.length === 0 ? (
                    <div className="flex h-full flex-col items-center justify-center py-16 text-center">
                      <div className="mb-4 rounded-full bg-primary/10 p-3">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          className="h-6 w-6 text-primary"
                        >
                          <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
                          <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
                          <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0" />
                          <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" />
                        </svg>
                      </div>
                      <h2 className="text-2xl font-bold tracking-tight">What can I help you ship?</h2>
                      <p className="mt-2 text-muted-foreground">
                        Ask me to create UI components, layouts, or complete pages.
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-6 pb-20">
                      {messages.map((message) => (
                        <div
                          key={message.id}
                          className={cn(
                            "flex items-start gap-4 rounded-lg p-4",
                            message.role === "assistant" && "bg-muted/50",
                          )}
                        >
                          <Avatar className="h-8 w-8">
                            {message.role === "assistant" ? (
                              <>
                                <AvatarImage src="/placeholder.svg?height=32&width=32" alt="v0" />
                                <AvatarFallback>v0</AvatarFallback>
                              </>
                            ) : (
                              <>
                                <AvatarImage src="/placeholder.svg?height=32&width=32" alt="User" />
                                <AvatarFallback>U</AvatarFallback>
                              </>
                            )}
                          </Avatar>
                          <div className="flex-1 space-y-2">
                            <div className="prose prose-sm dark:prose-invert">{message.content}</div>
                            {message.codeBlocks?.map((codeBlock) => renderCodeBlock(codeBlock))}
                            {message.role === "assistant" && message.codeBlocks && (
                              <div className="mt-4 flex items-center gap-2">
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-xs"
                                  onClick={() => setActiveTab("code")}
                                >
                                  View Code
                                </Button>
                                <Button variant="outline" size="sm" className="text-xs">
                                  Add to Codebase
                                </Button>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                      <div ref={messagesEndRef} />
                    </div>
                  )}
                </div>
              </ScrollArea>
            </TabsContent>
            <TabsContent
              value="code"
              className="flex-1 overflow-hidden p-0 data-[state=active]:flex-col data-[state=active]:flex"
            >
              <div className="flex h-full flex-col">
                <div className="flex-1 overflow-auto bg-zinc-900 p-4 font-mono text-sm text-zinc-100">
                  <pre>
                    {(() => {
                      const lastMessage = messages[messages.length - 1];
                      const codeBlocks = lastMessage?.codeBlocks;
                      const firstCodeBlock = codeBlocks?.[0];
                      
                      return firstCodeBlock?.code || `// No code generated yet
// Ask v0 to create a component`;
                    })()}
                  </pre>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </ResizablePanel>
        <ResizableHandle withHandle />
        <ResizablePanel defaultSize={30} minSize={20}>
          <div className="border-t bg-background p-4">
            <div className="mx-auto max-w-3xl">
              <form onSubmit={handleSubmit} className="relative">
                <Textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask v0 to build..."
                  className="min-h-10 resize-none border-0 p-3 shadow-none focus-visible:ring-0"
                />
                <div className="absolute bottom-0 right-0 flex items-center p-3">
                  <Button
                    type="submit"
                    size="icon"
                    disabled={!input.trim() || isLoading}
                    className={cn("h-8 w-8 rounded-full", !input.trim() && "opacity-50")}
                  >
                    {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowUp className="h-4 w-4" />}
                    <span className="sr-only">Send</span>
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  )
}
