"use client"

import { useEffect, useRef } from "react"
import { motion } from "framer-motion"

interface RobotAvatarProps {
    isSpeaking: boolean
    isListening: boolean
    className?: string
}

export default function RobotAvatar({ isSpeaking, isListening, className = "" }: RobotAvatarProps) {
    return (
        <div className={`relative flex items-center justify-center ${className}`}>
            {/* Main Head Container */}
            <div className="relative w-64 h-64">

                {/* Glow Effect */}
                <div className={`absolute inset-0 rounded-full blur-3xl transition-all duration-500 ${isSpeaking ? "bg-blue-500/40 scale-110" : "bg-blue-900/20 scale-100"}`} />

                {/* Head Shape */}
                <svg viewBox="0 0 200 200" className="w-full h-full drop-shadow-2xl">
                    <defs>
                        <linearGradient id="headGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#1e293b" />
                            <stop offset="100%" stopColor="#0f172a" />
                        </linearGradient>
                        <linearGradient id="eyeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#60a5fa" />
                            <stop offset="100%" stopColor="#3b82f6" />
                        </linearGradient>
                    </defs>

                    {/* Helmet/Head */}
                    <path
                        d="M40,100 C40,50 60,30 100,30 C140,30 160,50 160,100 C160,140 140,170 100,170 C60,170 40,140 40,100 Z"
                        fill="url(#headGradient)"
                        stroke="#334155"
                        strokeWidth="2"
                    />

                    {/* Face Plate (Glass) */}
                    <path
                        d="M55,100 C55,70 70,60 100,60 C130,60 145,70 145,100 C145,130 130,145 100,145 C70,145 55,130 55,100 Z"
                        fill="#000000"
                        opacity="0.8"
                    />

                    {/* Eyes Container */}
                    <g transform="translate(0, 0)">
                        {/* Left Eye */}
                        <motion.ellipse
                            cx="80"
                            cy="95"
                            rx="12"
                            ry="8"
                            fill="url(#eyeGradient)"
                            animate={{
                                ry: isListening ? [8, 2, 8] : 8,
                                scale: isSpeaking ? [1, 1.1, 1] : 1
                            }}
                            transition={{
                                ry: { repeat: Infinity, duration: 3, repeatDelay: 2 },
                                scale: { repeat: Infinity, duration: 0.5 }
                            }}
                        />
                        {/* Right Eye */}
                        <motion.ellipse
                            cx="120"
                            cy="95"
                            rx="12"
                            ry="8"
                            fill="url(#eyeGradient)"
                            animate={{
                                ry: isListening ? [8, 2, 8] : 8,
                                scale: isSpeaking ? [1, 1.1, 1] : 1
                            }}
                            transition={{
                                ry: { repeat: Infinity, duration: 3, repeatDelay: 2 },
                                scale: { repeat: Infinity, duration: 0.5 }
                            }}
                        />
                    </g>

                    {/* Mouth Visualization */}
                    <g transform="translate(100, 125)">
                        {isSpeaking ? (
                            <motion.path
                                d="M-20,0 Q0,10 20,0"
                                stroke="#60a5fa"
                                strokeWidth="3"
                                fill="none"
                                animate={{ d: ["M-20,0 Q0,15 20,0", "M-20,0 Q0,5 20,0", "M-20,0 Q0,15 20,0"] }}
                                transition={{ repeat: Infinity, duration: 0.3 }}
                            />
                        ) : (
                            <path d="M-15,0 Q0,5 15,0" stroke="#334155" strokeWidth="2" fill="none" />
                        )}
                    </g>

                    {/* Antenna */}
                    <line x1="100" y1="30" x2="100" y2="10" stroke="#334155" strokeWidth="2" />
                    <circle cx="100" cy="10" r="4" fill={isListening ? "#ef4444" : "#334155"} className="transition-colors duration-300" />
                </svg>

                {/* Listening Ring */}
                {isListening && (
                    <motion.div
                        className="absolute inset-0 rounded-full border-2 border-blue-500/30"
                        animate={{ scale: [1, 1.2], opacity: [1, 0] }}
                        transition={{ repeat: Infinity, duration: 1.5 }}
                    />
                )}
            </div>
        </div>
    )
}
