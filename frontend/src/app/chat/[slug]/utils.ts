import { toast } from "sonner";

export const handleCopy = (text: string) => {
  navigator.clipboard.writeText(text);
  toast.success("Notes copied to clipboard!", {
    description: "You can now paste the notes anywhere you want.",
  });
};

export const handleDownload = (text: string, chatName: string) => {
  const element = document.createElement("a");
  const file = new Blob([text], { type: "text/plain" });
  element.href = URL.createObjectURL(file);
  element.download = `${chatName.replace(/\s+/g, "-")}_notes.md`;
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
  toast.success("Notes downloaded!", {
    description: "Your notes have been saved to your device.",
  });
}; 