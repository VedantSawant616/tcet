'use client';

import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { AlertTriangle, CheckCircle, Activity, Brain, Server, DollarSign } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function Dashboard() {
    const [metrics, setMetrics] = useState<any[]>([]);
    const [alerts, setAlerts] = useState<any[]>([]);
    const [llmLogs, setLlmLogs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        console.log("Fetching data from:", API_URL);
        try {
            const results = await Promise.allSettled([
                fetch(`${API_URL}/metrics?limit=100`),
                fetch(`${API_URL}/alerts?limit=50`),
                fetch(`${API_URL}/events/llm?limit=20`)
            ]);

            const [metricsRes, alertsRes, llmRes] = results;

            if (metricsRes.status === 'fulfilled' && metricsRes.value.ok) {
                setMetrics(await metricsRes.value.json());
            } else if (metricsRes.status === 'rejected') {
                console.error("Metrics fetch failed:", metricsRes.reason);
            }

            if (alertsRes.status === 'fulfilled' && alertsRes.value.ok) {
                setAlerts(await alertsRes.value.json());
            }

            if (llmRes.status === 'fulfilled' && llmRes.value.ok) {
                setLlmLogs(await llmRes.value.json());
            }
        } catch (error) {
            console.error("Unexpected error in fetchData", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000); // Refresh every 5s
        return () => clearInterval(interval);
    }, []);

    // Process metrics for charts
    const driftData = metrics
        .filter((m: any) => m.metric_name === 'drift_psi')
        .map((m: any) => ({ time: new Date(m.timestamp).toLocaleTimeString(), value: m.value, name: m.entity_name }))
        .reverse();

    const riskData = metrics
        .filter((m: any) => m.metric_name === 'risk_score')
        .map((m: any) => ({ time: new Date(m.timestamp).toLocaleTimeString(), value: m.value, name: m.entity_name }))
        .reverse();

    return (
        <div className="min-h-screen bg-neutral-950 text-neutral-100 p-8 font-sans">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Unified AI Observability</h1>
                    <p className="text-neutral-400">Real-time monitoring for ML models and LLM applications</p>
                </div>
                <div className="flex gap-4">
                    <div className="flex items-center gap-2 bg-green-500/10 text-green-500 px-3 py-1 rounded-full border border-green-500/20">
                        <Activity size={16} />
                        <span className="text-sm font-medium">System Healthy</span>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard title="Total Requests" value={metrics.length.toString()} icon={<Server size={20} />} />
                <StatCard title="Active Alerts" value={alerts.filter((a: any) => !a.resolved).length.toString()} icon={<AlertTriangle size={20} />} highlight={alerts.length > 0} />
                <StatCard title="Avg LLM Cost" value="$0.003" icon={<DollarSign size={20} />} />
                <StatCard title="Drift Detection" value={driftData.length > 0 ? "Active" : "No Data"} icon={<Brain size={20} />} />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <ChartCard title="Model Drift (PSI)" data={driftData} color="#8884d8" />
                <ChartCard title="Risk Score Trends" data={riskData} color="#f43f5e" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-neutral-900 border border-neutral-800 rounded-xl p-6">
                    <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                        <Server size={20} className="text-blue-500" />
                        Recent LLM Transactions
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm text-neutral-400">
                            <thead className="text-xs uppercase bg-neutral-800/50 text-neutral-300">
                                <tr>
                                    <th className="px-4 py-3 rounded-l-lg">Time</th>
                                    <th className="px-4 py-3">App Name</th>
                                    <th className="px-4 py-3">Latency</th>
                                    <th className="px-4 py-3">Tokens</th>
                                    <th className="px-4 py-3">Cost</th>
                                    <th className="px-4 py-3 rounded-r-lg">Risk</th>
                                </tr>
                            </thead>
                            <tbody>
                                {llmLogs.map((log: any) => (
                                    <tr key={log.id} className="border-b border-neutral-800 hover:bg-neutral-800/20 transition-colors">
                                        <td className="px-4 py-3">{new Date(log.timestamp).toLocaleTimeString()}</td>
                                        <td className="px-4 py-3 font-medium text-white">{log.application_name}</td>
                                        <td className="px-4 py-3">{log.latency_ms}ms</td>
                                        <td className="px-4 py-3">{log.tokens_used}</td>
                                        <td className="px-4 py-3 text-emerald-400">${log.cost_usd?.toFixed(4)}</td>
                                        <td className="px-4 py-3">
                                            <span className="bg-blue-500/10 text-blue-400 px-2 py-1 rounded text-xs border border-blue-500/20">
                                                Low
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                                {llmLogs.length === 0 && (
                                    <tr>
                                        <td colSpan={6} className="text-center py-8 text-neutral-500">No recent logs found.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
                    <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                        <AlertTriangle size={20} className="text-amber-500" />
                        Active Alerts
                    </h2>
                    <div className="space-y-4">
                        {alerts.map((alert: any) => (
                            <div key={alert.id} className="bg-red-500/5 border border-red-500/20 p-4 rounded-lg flex items-start gap-3">
                                <AlertTriangle size={18} className="text-red-500 mt-1 shrink-0" />
                                <div>
                                    <h4 className="text-sm font-medium text-red-200">{alert.message}</h4>
                                    <span className="text-xs text-red-500/70">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                                </div>
                            </div>
                        ))}
                        {alerts.length === 0 && (
                            <div className="flex flex-col items-center justify-center h-48 text-neutral-500 text-sm">
                                <CheckCircle size={32} className="mb-2 opacity-20" />
                                No active alerts
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, icon, highlight }: any) {
    return (
        <div className={cn("bg-neutral-900 border border-neutral-800 rounded-xl p-6 flex items-center justify-between", highlight && "border-red-500/50 bg-red-500/5")}>
            <div>
                <p className="text-neutral-400 text-sm font-medium mb-1">{title}</p>
                <h3 className="text-2xl font-bold text-white">{value}</h3>
            </div>
            <div className={cn("p-3 bg-neutral-800 rounded-lg text-neutral-400", highlight && "text-red-400 bg-red-500/10")}>
                {icon}
            </div>
        </div>
    );
}

function ChartCard({ title, data, color }: any) {
    return (
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 h-[400px]">
            <h2 className="text-lg font-semibold mb-6 text-white">{title}</h2>
            <ResponsiveContainer width="100%" height="85%">
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis dataKey="time" stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#171717', border: '1px solid #333', borderRadius: '8px' }}
                        itemStyle={{ color: '#fff' }}
                    />
                    <Line type="monotone" dataKey="value" stroke={color} strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
