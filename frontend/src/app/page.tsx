"use client";
import Image from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { UrlInput } from "@/components/url-input";
import { ArrowRight, Play, FileText, Clock } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import { useState, useEffect } from "react";

export default function Home() {
  const videoExamples = [
    {
      title: "Dynamic Programming By Abdul Bari",
      duration: "12:34",
      category: "Computer Science",
    },
    {
      title: "The History of Renaissance Art",
      duration: "18:42",
      category: "Art History",
    },
    {
      title: "Quantum Physics Explained Simply",
      duration: "15:28",
      category: "Physics",
    },
    {
      title: "Machine Learning Fundamentals",
      duration: "22:15",
      category: "Technology",
    },
    {
      title: "Ancient Rome: Rise and Fall",
      duration: "31:07",
      category: "History",
    },
    {
      title: "Organic Chemistry Basics",
      duration: "14:53",
      category: "Chemistry",
    },
    {
      title: "Psychology of Human Behavior",
      duration: "19:36",
      category: "Psychology",
    },
    {
      title: "Financial Markets Overview",
      duration: "25:44",
      category: "Finance",
    },
  ];

  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentVideoIndex((prev) => (prev + 1) % videoExamples.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const currentVideo = videoExamples[currentVideoIndex];
  return (
    <main className="min-h-screen relative flex flex-col">
      <div className="fixed inset-0 z-0 opacity-70">
        <Image
          src="/background.png"
          alt="Purple gradient background"
          fill
          priority
          className="object-cover"
        />
      </div>

      <div className="relative z-10 flex flex-col justify-between min-h-screen p-8 md:p-16">
        <motion.header
          className="mb-16 md:mb-32"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <div className="flex items-center justify-between">
            <h1 className="text-white text-4xl font-medium tracking-tight">
              Captr
            </h1>
            <motion.div
              className="hidden md:flex items-center gap-8 text-white/60 text-sm"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            >
              <span className="hover:text-white/80 transition-colors cursor-pointer">
                About
              </span>
              <span className="hover:text-white/80 transition-colors cursor-pointer">
                Features
              </span>
              <span className="hover:text-white/80 transition-colors cursor-pointer">
                Contact
              </span>
            </motion.div>
          </div>
          <motion.div
            className="w-full h-px bg-white/10 mt-8"
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ duration: 1, delay: 0.4, ease: "easeOut" }}
          ></motion.div>
        </motion.header>

        <div className="flex-1 flex flex-col justify-center w-full max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-12 items-end gap-16 lg:gap-24">
            <motion.div
              className="lg:col-span-7 space-y-12"
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 1, delay: 0.6, ease: "easeOut" }}
            >
              <motion.div className="space-y-8">
                <motion.h2
                  className="text-white text-5xl md:text-6xl lg:text-7xl font-medium leading-[0.9] tracking-tight"
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 1, delay: 0.8, ease: "easeOut" }}
                >
                  Instantly transform
                  <br />
                  YouTube videos into
                  <br />
                  <motion.span
                    className="text-white/70"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 1.2 }}
                  >
                    comprehensive
                  </motion.span>
                  <br />
                  research documents
                </motion.h2>

                <motion.div
                  className="flex items-center gap-4 text-white/60"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 1.4, ease: "easeOut" }}
                >
                  <motion.div
                    className="flex items-center gap-2"
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Play className="w-4 h-4" />
                    <span className="text-sm">Video Processing</span>
                  </motion.div>
                  <div className="w-1 h-1 bg-white/30 rounded-full"></div>
                  <motion.div
                    className="flex items-center gap-2"
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <FileText className="w-4 h-4" />
                    <span className="text-sm">AI Analysis</span>
                  </motion.div>
                  <div className="w-1 h-1 bg-white/30 rounded-full"></div>
                  <motion.div
                    className="flex items-center gap-2"
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Clock className="w-4 h-4" />
                    <span className="text-sm">Instant Results</span>
                  </motion.div>
                </motion.div>
              </motion.div>

              <motion.div
                className="space-y-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 1.6, ease: "easeOut" }}
              >
                <p className="text-white/70 text-lg max-w-2xl leading-relaxed">
                  Extract key insights, generate summaries, and create
                  structured notes from any YouTube video in seconds.
                </p>
                <motion.div
                  className="flex items-center gap-2 text-white/50 text-sm"
                  whileHover={{ x: 5 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <span>Powered by advanced AI</span>
                  <ArrowRight className="w-4 h-4" />
                </motion.div>
              </motion.div>
            </motion.div>

            <motion.div
              className="lg:col-span-5"
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 1, delay: 1, ease: "easeOut" }}
            >
              <motion.div
                whileHover={{ scale: 1.02, y: -5 }}
                transition={{ type: "spring", stiffness: 200, damping: 20 }}
              >
                <Card className="bg-black/80 backdrop-blur-sm text-white border-white/10 shadow-2xl rounded-3xl overflow-hidden hover:bg-black/85 transition-all duration-300 group">
                  <CardHeader className="pb-4">
                    <div className="flex items-start justify-between">
                      <div className="space-y-2 min-h-[80px] flex flex-col justify-center">
                        <AnimatePresence mode="wait">
                          <motion.div
                            key={currentVideoIndex}
                            initial={{ opacity: 0, y: 20, filter: "blur(4px)" }}
                            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                            exit={{ opacity: 0, y: -20, filter: "blur(4px)" }}
                            transition={{ duration: 0.5, ease: "easeInOut" }}
                          >
                            <CardTitle className="text-white/90 font-normal text-lg leading-tight">
                              {currentVideo.title}
                            </CardTitle>
                            <div className="flex items-center gap-3 text-white/50 text-sm">
                              <span>{currentVideo.duration} duration</span>
                              <div className="w-1 h-1 bg-white/30 rounded-full"></div>
                              <span>{currentVideo.category}</span>
                            </div>
                          </motion.div>
                        </AnimatePresence>
                      </div>
                      <motion.div
                        className="w-2 h-2 bg-green-400/80 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{
                          duration: 2,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
                      ></motion.div>
                    </div>
                    <motion.div
                      className="w-full h-px bg-white/10 mt-6"
                      initial={{ scaleX: 0 }}
                      animate={{ scaleX: 1 }}
                      transition={{
                        duration: 0.8,
                        delay: 1.2,
                        ease: "easeOut",
                      }}
                    ></motion.div>
                  </CardHeader>

                  <CardContent className="space-y-6">
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{
                        duration: 0.8,
                        delay: 1.4,
                        ease: "easeOut",
                      }}
                    >
                      <UrlInput />
                    </motion.div>

                    <motion.div
                      className="space-y-4"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{
                        duration: 0.8,
                        delay: 1.6,
                        ease: "easeOut",
                      }}
                    >
                      <div className="text-white/40 text-xs uppercase tracking-wider">
                        Output Preview
                      </div>
                      <div className="space-y-3 p-4 bg-white/5 rounded-xl border border-white/10">
                        <motion.div
                          className="flex items-center gap-3"
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.5, delay: 1.8 }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-white/30 rounded-full"
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{
                              duration: 2,
                              delay: 2,
                              repeat: Infinity,
                              ease: "easeInOut",
                            }}
                          ></motion.div>
                          <span className="text-white/60 text-sm">
                            Key Concepts Extracted
                          </span>
                        </motion.div>
                        <motion.div
                          className="flex items-center gap-3"
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.5, delay: 2 }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-white/30 rounded-full"
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{
                              duration: 2,
                              delay: 2.2,
                              repeat: Infinity,
                              ease: "easeInOut",
                            }}
                          ></motion.div>
                          <span className="text-white/60 text-sm">
                            Structured Summary Generated
                          </span>
                        </motion.div>
                        <motion.div
                          className="flex items-center gap-3"
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.5, delay: 2.2 }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-white/30 rounded-full"
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{
                              duration: 2,
                              delay: 2.4,
                              repeat: Infinity,
                              ease: "easeInOut",
                            }}
                          ></motion.div>
                          <span className="text-white/60 text-sm">
                            Research Notes Compiled
                          </span>
                        </motion.div>
                      </div>
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>
            </motion.div>
          </div>
        </div>

        <motion.footer
          className="mt-16 md:mt-32 pt-8 border-t border-white/10"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 2.4, ease: "easeOut" }}
        >
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div className="space-y-2">
              <p className="text-white/50 text-sm">
                Transform learning with AI-powered video analysis
              </p>
              <div className="flex items-center gap-4 text-white/30 text-xs">
                <span>© 2024 Captr</span>
                <div className="w-1 h-1 bg-white/20 rounded-full"></div>
                <span>Privacy Policy</span>
                <div className="w-1 h-1 bg-white/20 rounded-full"></div>
                <span>Terms of Service</span>
              </div>
            </div>

            <div className="flex items-center gap-6">
              <motion.button
                className="text-white/60 hover:text-white transition-colors text-sm"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                Get Started
              </motion.button>
              <motion.button
                className="flex items-center gap-2 text-white bg-white/10 hover:bg-white/20 transition-all px-6 py-3 rounded-full text-sm backdrop-blur-sm border border-white/20"
                whileHover={{ scale: 1.05, x: 5 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <span>Try Demo</span>
                <ArrowRight className="w-4 h-4" />
              </motion.button>
            </div>
          </div>
        </motion.footer>
      </div>
    </main>
  );
}
