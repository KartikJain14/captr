"use client"

import { useState } from "react"
import { Link, ArrowUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function UrlInput() {
    const [url, setUrl] = useState("")

    const handleSubmit = () => {
        if (!url) return

        // Process the URL (this would connect to your actual implementation)
        console.log("Processing URL:", url)
        // Here you would typically call an API or perform some action with the URL
    }

    return (
        <div className="flex gap-2 items-center">
            <div className="relative flex-1">
                <Input
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Or Enter URL!"
                    className="bg-gray-200 text-black pl-10 py-6 rounded-md"
                />
                <Link className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
            </div>
            <Button
                onClick={handleSubmit}
                size="icon"
                className="rounded-full h-10 w-10 bg-white text-black hover:bg-gray-100"
                aria-label="Submit URL"
            >
                <ArrowUp size={20} />
            </Button>
        </div>
    )
}
