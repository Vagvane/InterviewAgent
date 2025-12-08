"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import api from "@/lib/api"
import { Loader2 } from "lucide-react"

export default function ReportPage() {
    const searchParams = useSearchParams()
    const type = searchParams.get("type") // 'assessment', 'coding', 'interview'
    const id = searchParams.get("id")
    const [data, setData] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (type && id) {
            fetchDetails()
        }
    }, [type, id])

    const fetchDetails = async () => {
        try {
            const res = await api.get(`/profile/history/${type}/${id}`)
            setData(res.data)
            // Auto print after content loads
            setTimeout(() => {
                window.print()
            }, 1000)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return <div className="flex justify-center items-center h-screen"><Loader2 className="animate-spin" /></div>
    }

    if (!data) return <div>Data not found</div>

    return (
        <div className="p-8 max-w-4xl mx-auto print:p-0">
            <div className="text-center mb-8 border-b pb-4">
                <h1 className="text-3xl font-bold mb-2">Interview Agent Report</h1>
                <p className="text-gray-500">Generated on {new Date().toLocaleDateString()}</p>
            </div>

            <div className="mb-6">
                <h2 className="text-xl font-semibold bg-gray-100 p-2 rounded">{data.title}</h2>
                <div className="grid grid-cols-2 gap-4 mt-2">
                    <div><strong>Date:</strong> {data.date}</div>
                    <div><strong>Score/Status:</strong> {data.score || data.status}</div>
                </div>
            </div>

            {type === 'assessment' && data.responses && (
                <div className="space-y-4">
                    <h3 className="text-lg font-bold">Responses</h3>
                    {Object.entries(data.responses).map(([q, a]: any, i) => (
                        <div key={i} className="border p-4 rounded">
                            <p className="font-semibold">{q}</p>
                            <p className="mt-1 text-blue-700">Answer: {a}</p>
                        </div>
                    ))}
                </div>
            )}

            {type === 'coding' && (
                <div className="space-y-4">
                    <h3 className="text-lg font-bold">Submitted Code</h3>
                    <div className="bg-gray-100 p-4 rounded font-mono text-sm whitespace-pre-wrap border">
                        {data.code}
                    </div>
                </div>
            )}

            {type === 'interview' && (
                <div className="space-y-6">
                    {data.job_description && (
                        <div>
                            <h3 className="text-lg font-bold">Job Description</h3>
                            <p className="text-sm text-gray-700">{data.job_description}</p>
                        </div>
                    )}

                    {data.feedback && (
                        <div>
                            <h3 className="text-lg font-bold">Feedback</h3>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <h4 className="font-semibold text-green-700">Strengths</h4>
                                    <ul className="list-disc pl-5">{data.feedback.strengths?.map((s: any, i: any) => <li key={i}>{s}</li>)}</ul>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-red-700">Areas for Improvement</h4>
                                    <ul className="list-disc pl-5">{data.feedback.weaknesses?.map((w: any, i: any) => <li key={i}>{w}</li>)}</ul>
                                </div>
                            </div>
                        </div>
                    )}

                    <div>
                        <h3 className="text-lg font-bold">Transcript</h3>
                        <div className="space-y-2 mt-2">
                            {data.transcript?.map((msg: any, i: number) => (
                                <div key={i} className={`p-2 rounded ${msg.role === 'assistant' ? 'bg-blue-50 border-l-4 border-blue-500' : 'bg-gray-50 border-1-4 border-gray-500'}`}>
                                    <span className="font-bold uppercase text-xs text-gray-500">{msg.role}</span>
                                    <p>{msg.content}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
