export interface Message {
  id: string;
  content: string;
  isAI: boolean;
  timestamp: Date;
}

export interface ChatState {
  message: string;
  chatName: string;
} 