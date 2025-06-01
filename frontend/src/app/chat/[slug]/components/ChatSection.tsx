"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Bot, Paperclip, Send } from "lucide-react";

interface ChatSectionProps {
  message: string;
  setMessage: (message: string) => void;
}

export function ChatSection({ message, setMessage }: ChatSectionProps) {
  return (
    <div className="flex-1 flex flex-col border-r border-border bg-card h-full">
      {/* Chat Section */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar max-w-3xl mx-auto">
        {/* AI summary message */}
        <div className="flex items-start gap-3">
          <Avatar className="h-8 w-8">
            <AvatarFallback>
              <Bot className="w-5 h-5 text-muted-foreground" />
            </AvatarFallback>
          </Avatar>
          <div className="bg-primary/10 text-primary-foreground p-3 rounded-lg max-w-[70%]">
            <p className="">
              Here&apos;s a summary of the YouTube video: It covers the basics of Artificial Intelligence, including Machine Learning, Deep Learning, and Natural Language Processing. It discusses real-world applications in healthcare, finance, autonomous vehicles, and more. The video also highlights ethical considerations like bias, job displacement, and privacy, and emphasizes the importance of responsible AI development. Would you like to modify or add anything to these notes?
            </p>
          </div>
        </div>
        {/* Human asks for changes */}
        <div className="flex items-start gap-3">
          <Avatar className="h-8 w-8">
            <AvatarImage
              src="https://randomuser.me/api/portraits/men/32.jpg"
              alt="User"
            />
            <AvatarFallback>Y</AvatarFallback>
          </Avatar>
          <div className="bg-background text-foreground p-3 rounded-lg max-w-[70%] border border-border">
            <p className="">
              Can you add a section about recent breakthroughs in AI, like GPT-4 and generative models?
            </p>
          </div>
        </div>
        {/* AI responds with updated notes */}
        <div className="flex items-start gap-3">
          <Avatar className="h-8 w-8">
            <AvatarFallback>
              <Bot className="w-5 h-5 text-muted-foreground" />
            </AvatarFallback>
          </Avatar>
          <div className="bg-primary/10 text-primary-foreground p-3 rounded-lg max-w-[70%]">
            <p className="">
              Absolutely! I&apos;ve added a new section on recent breakthroughs:
              <br />
              <br />
              <strong>Recent Breakthroughs in AI:</strong> The field has seen rapid progress with models like GPT-4, which can generate human-like text, and other generative models that create images, music, and more. These advancements are pushing the boundaries of what AI can achieve in creativity and problem-solving.
            </p>
          </div>
        </div>
        <div className="text-center text-muted-foreground italic mt-8">
          Start typing to begin your conversation.
        </div>
      </div>
      {/* Chat Input Area */}
      <div className="border-t border-border bg-card p-4 w-full max-w-3xl mx-auto">
        <div className="flex items-center gap-3">
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 rounded-lg border border-input px-4 py-2 bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none min-h-[48px]"
            rows={1}
          />
          <Button
            variant="ghost"
            size="icon"
            className="text-muted-foreground hover:bg-accent hover:text-accent-foreground rounded-lg transition-colors"
            title="Attach File"
          >
            <Paperclip className="w-5 h-5" />
          </Button>
          <Button
            variant="default"
            size="icon"
            className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg shadow-md transition-colors"
            title="Send Message"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
        <p className="mt-3 text-xs text-muted-foreground text-center">
          Disclaimer: We may or may not provide the best responses. Use at
          your own discretion.
        </p>
      </div>
    </div>
  );
} 