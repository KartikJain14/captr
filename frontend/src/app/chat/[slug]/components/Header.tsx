"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import {
  Settings,
  Share2,
  Copy,
  Download,
  Menu,
} from "lucide-react";
import { handleCopy, handleDownload } from "../utils";
import { DUMMY_MARKDOWN } from "../constants";

interface HeaderProps {
  chatName: string;
}

export function Header({ chatName }: HeaderProps) {
  return (
    <nav className="border-b border-border bg-card shadow-sm">
      <div className="flex w-full items-center justify-between px-6 py-3">
        {/* Left: Sidebar Trigger & Chat Name */}
        <div className="flex items-center gap-4">
          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="text-muted-foreground hover:bg-accent rounded-md transition-colors"
                title="Open Sidebar"
              >
                <Menu className="w-5 h-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-64 bg-card p-4">
              <SheetHeader className="mb-6">
                <SheetTitle className="flex items-center gap-3 text-lg font-bold text-foreground">
                  <Avatar className="h-9 w-9">
                    <AvatarImage
                      src="https://randomuser.me/api/portraits/men/32.jpg"
                      alt="User Photo"
                    />
                    <AvatarFallback>Y</AvatarFallback>
                  </Avatar>
                  Yash&apos;s Hub
                </SheetTitle>
              </SheetHeader>
              {/* Sidebar Content */}
              <div className="space-y-4">
                <Button
                  variant="ghost"
                  className="w-full justify-start text-foreground hover:bg-accent"
                >
                  New Chat
                </Button>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-foreground hover:bg-accent"
                >
                  Past Conversations
                </Button>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-foreground hover:bg-accent"
                >
                  Settings
                </Button>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-foreground hover:bg-accent"
                >
                  Help
                </Button>
              </div>
            </SheetContent>
          </Sheet>

          <span className="text-lg font-semibold text-foreground">
            {chatName}
          </span>
        </div>

        {/* Right: Copy, Download, Settings, Share, Profile menu */}
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            title="Copy Notes"
            className="text-muted-foreground hover:bg-accent rounded-md transition-colors"
            onClick={() => handleCopy(DUMMY_MARKDOWN)}
          >
            <Copy className="w-5 h-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            title="Download Notes"
            className="text-muted-foreground hover:bg-accent rounded-md transition-colors"
            onClick={() => handleDownload(DUMMY_MARKDOWN, chatName)}
          >
            <Download className="w-5 h-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            title="Settings"
            className="text-muted-foreground hover:bg-accent rounded-md transition-colors"
          >
            <Settings className="w-5 h-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            title="Share"
            className="text-muted-foreground hover:bg-accent rounded-md transition-colors"
          >
            <Share2 className="w-5 h-5" />
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="p-1 rounded-full hover:bg-accent transition-colors"
              >
                <Avatar className="h-8 w-8">
                  <AvatarImage
                    src="https://randomuser.me/api/portraits/men/32.jpg"
                    alt="Profile"
                  />
                  <AvatarFallback>Y</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              align="end"
              className="bg-popover shadow-lg rounded-md py-1"
            >
              <DropdownMenuItem asChild>
                <a
                  href="/settings"
                  className="block px-4 py-2  text-foreground hover:bg-accent cursor-pointer"
                >
                  Settings
                </a>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <span className="block px-4 py-2  text-foreground hover:bg-accent cursor-pointer">
                  Logout
                </span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </nav>
  );
} 