import Image from "next/image"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { UrlInput } from "@/components/url-input"

export default function Home() {
  return (
    <main className="min-h-screen relative flex flex-col">
      {/* Background Image */}
      <div className="fixed inset-0 z-0">
        <Image src="/background.png" alt="Purple gradient background" fill priority className="object-cover" />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col min-h-screen p-6 md:p-12">
        {/* Logo */}
        <header className="mb-12 md:mb-24">
          <h1 className="text-white text-3xl font-medium">Captr</h1>
        </header>

        {/* Main Content */}
        <div className="flex-1 flex flex-col justify-center max-w-5xl">
          <h2 className="text-white text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-24 max-w-3xl">
            Instantly transform YouTube videos into comprehensive research documents
          </h2>

          {/* Card */}
          <Card className="bg-black/80 text-white border-none shadow-xl self-end max-w-xl w-full">
            <CardHeader>
              <CardTitle className="text-gray-300 font-normal">Dynamic Programming By Abdul Bari</CardTitle>
            </CardHeader>
            <CardContent>
              <UrlInput />
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
