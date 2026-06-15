"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { ShieldAlert, Activity, CheckCircle2, AlertTriangle, Cpu, Terminal, ExternalLink, Play, TerminalSquare } from "lucide-react";

export default function Dashboard() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [stats, setStats] = useState({ total: 0, autoResolved: 0, activeInvestigations: 0 });
  const [terminalLogs, setTerminalLogs] = useState<string[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);

  const simulateAttack = async () => {
    if (isSimulating) return;
    setIsSimulating(true);
    setTerminalLogs([]);

    const sequence = [
      "> Initializing SENTINEL Attack Simulator...",
      "> Compiling ransomware dropper payload...",
      "> Target acquired: 10.0.1.55",
      "> Executing simulated Splunk Webhook...",
    ];

    for (let i = 0; i < sequence.length; i++) {
      setTerminalLogs(prev => [...prev, sequence[i]]);
      await new Promise(resolve => setTimeout(resolve, 800));
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const payload = {
        sid: "DEMO-" + Math.floor(Math.random() * 10000),
        search_name: "Ransomware Behavior Detected",
        app: "search",
        owner: "admin",
        results_link: "https://prd-p-3icdn.splunkcloud.com",
        result: {
          src_ip: "185.156.73.14",
          dest_ip: "10.0.1.55",
          user: "system",
          action: "multiple_file_encryptions"
        }
      };

      const response = await fetch(`${apiUrl}/api/v1/webhook/splunk`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        setTerminalLogs(prev => [...prev, "> [HTTP 200] Webhook accepted by Render Backend.", "> Awaiting Autonomous Agent response..."]);
      } else {
        setTerminalLogs(prev => [...prev, "> [HTTP Error] Failed to send webhook."]);
      }
    } catch (e) {
      setTerminalLogs(prev => [...prev, "> [Network Error] Could not reach backend. Check CORS or URL."]);
    }
    
    setTimeout(() => setIsSimulating(false), 2000);
  };

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/v1/alerts`);
        if (response.ok) {
          const data = await response.json();
          setAlerts(data);
          
          // Calculate stats
          const total = data.length;
          const autoResolved = data.filter((a: any) => a.playbook === "False Positive Triage" || a.status === "Closed (False Positive)").length;
          const active = data.filter((a: any) => a.status === "Remediated" && a.playbook !== "False Positive Triage").length;
          
          setStats({ total, autoResolved, activeInvestigations: active });
        }
      } catch (error) {
        console.error("Failed to fetch alerts:", error);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-50 p-8 font-sans">
      {/* Header */}
      <header className="flex justify-between items-center mb-8 pb-4 border-b border-neutral-800">
        <div className="flex items-center gap-3">
          <ShieldAlert className="h-8 w-8 text-rose-500" />
          <h1 className="text-2xl font-bold tracking-tight">SENTINEL</h1>
          <Badge variant="outline" className="ml-2 bg-rose-500/10 text-rose-500 border-rose-500/20">LIVE</Badge>
        </div>
        <div className="flex items-center gap-4 text-sm text-neutral-400">
          <div className="flex items-center gap-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            Splunk Connected
          </div>
          <div className="flex items-center gap-2">
            <Cpu className="h-4 w-4" />
            Foundation-Sec-1.1 Active
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="bg-neutral-900 border-neutral-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-neutral-400">Total Alerts Processed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-neutral-50">{stats.total}</div>
            <p className="text-xs text-neutral-500 mt-1">Live from Splunk Webhook</p>
          </CardContent>
        </Card>
        <Card className="bg-neutral-900 border-neutral-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-neutral-400">Autonomous Triages</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-emerald-500">{stats.autoResolved}</div>
            <p className="text-xs text-neutral-500 mt-1">Closed as false positive or benign</p>
          </CardContent>
        </Card>
        <Card className="bg-neutral-900 border-neutral-800 relative overflow-hidden">
          <div className="absolute right-0 top-0 opacity-10">
            <Activity className="h-32 w-32" />
          </div>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-neutral-400">Critical Investigations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-rose-500">{stats.activeInvestigations}</div>
            <p className="text-xs text-neutral-500 mt-1">Malicious activity detected and contained</p>
          </CardContent>
        </Card>
      </div>

      {/* Attack Simulator Terminal */}
      <Card className="bg-black border-neutral-800 mb-8 font-mono relative overflow-hidden group shadow-[0_0_30px_-5px_rgba(16,185,129,0.1)]">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 via-emerald-400 to-transparent opacity-50"></div>
        <CardHeader className="pb-2 border-b border-neutral-900 bg-neutral-950 flex flex-row items-center justify-between">
          <CardTitle className="text-sm font-medium text-emerald-500 flex items-center gap-2">
            <TerminalSquare className="h-4 w-4" />
            ATTACK SIMULATOR TERMINAL
          </CardTitle>
          <button 
            onClick={simulateAttack}
            disabled={isSimulating}
            className="flex items-center gap-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-500 px-4 py-1.5 rounded text-xs font-bold transition-all disabled:opacity-50 border border-emerald-500/20 cursor-pointer"
          >
            <Play className="h-3 w-3 fill-emerald-500" />
            {isSimulating ? "DEPLOYING..." : "DEPLOY RANSOMWARE"}
          </button>
        </CardHeader>
        <CardContent className="pt-4 min-h-[120px] text-sm text-emerald-400/90 leading-relaxed">
          {terminalLogs.length === 0 ? (
            <div className="opacity-50 text-neutral-500">root@kali:~# Waiting for command execution...</div>
          ) : (
            <div className="space-y-1">
              <div className="text-emerald-500/50 mb-2">root@kali:~# ./ransomware_dropper.sh --target 10.0.1.55</div>
              {terminalLogs.map((log, i) => (
                <div key={i} className="animate-in fade-in slide-in-from-bottom-1">{log}</div>
              ))}
              {isSimulating && <div className="animate-pulse inline-block w-2 h-4 bg-emerald-500 ml-1 translate-y-1"></div>}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Latest Incident Deep Dive */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="col-span-2">
          <Card className="bg-neutral-900 border-neutral-800 h-full">
            <CardHeader>
              <CardTitle className="flex items-center justify-between text-neutral-50">
                Recent Incident Log
                <Badge variant="outline" className="bg-neutral-800 text-neutral-300">Last 100 events</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow className="border-neutral-800 hover:bg-neutral-800/50">
                    <TableHead className="text-neutral-400">Alert ID</TableHead>
                    <TableHead className="text-neutral-400">Source</TableHead>
                    <TableHead className="text-neutral-400">Target IP</TableHead>
                    <TableHead className="text-neutral-400">AI Score</TableHead>
                    <TableHead className="text-neutral-400">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {alerts.map((alert) => (
                    <TableRow key={alert.id} className="border-neutral-800 hover:bg-neutral-800/50 transition-colors">
                      <TableCell className="font-mono text-sm text-neutral-300">{alert.id}</TableCell>
                      <TableCell className="text-neutral-300">{alert.source}</TableCell>
                      <TableCell className="font-mono text-sm text-neutral-400">{alert.dest_ip}</TableCell>
                      <TableCell>
                        <Badge className={alert.severity > 80 ? "bg-rose-500/20 text-rose-500 hover:bg-rose-500/30" : "bg-amber-500/20 text-amber-500 hover:bg-amber-500/30"}>
                          {alert.severity}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2 text-sm">
                          {alert.status.includes("Remediated") ? <CheckCircle2 className="h-4 w-4 text-emerald-500" /> : <AlertTriangle className="h-4 w-4 text-amber-500" />}
                          <span className={alert.status.includes("Remediated") ? "text-emerald-500" : "text-amber-500"}>{alert.status}</span>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>

        {/* AI Analysis Panel */}
        <div className="col-span-1">
          <Card className="bg-neutral-900 border-rose-500/30 shadow-[0_0_30px_-10px_rgba(244,63,94,0.3)]">
            <CardHeader className="border-b border-neutral-800 bg-neutral-900/50">
              <CardTitle className="text-lg flex items-center gap-2 text-neutral-50">
                <Terminal className="h-5 w-5 text-rose-500" />
                Live Agent Orchestration
              </CardTitle>
              <CardDescription className="text-neutral-400">
                {alerts.length > 0 ? `Processing Alert ${alerts[0].id}` : "Waiting for Splunk alerts..."}
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              {alerts.length > 0 ? (
                <div className="space-y-6">
                  <div className="relative pl-6 border-l border-neutral-800 pb-2">
                    <div className="absolute -left-[5px] top-1 h-2 w-2 rounded-full bg-emerald-500"></div>
                    <h3 className="text-sm font-bold text-emerald-500 flex items-center gap-2">
                      Triage Agent <Badge variant="outline" className="h-5 text-[10px] bg-emerald-500/10 text-emerald-500 border-emerald-500/20">Done</Badge>
                    </h3>
                    <p className="text-xs text-neutral-400 mt-1">
                      {alerts[0].triage?.triage_summary || "Extracted observables and scored event."}
                    </p>
                  </div>

                  <div className="relative pl-6 border-l border-neutral-800 pb-2">
                    <div className="absolute -left-[5px] top-1 h-2 w-2 rounded-full bg-emerald-500"></div>
                    <h3 className="text-sm font-bold text-emerald-500 flex items-center gap-2">
                      Investigate Agent <Badge variant="outline" className="h-5 text-[10px] bg-emerald-500/10 text-emerald-500 border-emerald-500/20">Done</Badge>
                    </h3>
                    <p className="text-xs text-neutral-400 mt-1">
                      {alerts[0].investigation?.investigation_summary || "Checked Threat Intel and Correlated Splunk Logs."}
                    </p>
                  </div>

                  <div className="relative pl-6">
                    <div className="absolute -left-[5px] top-1 h-2 w-2 rounded-full bg-rose-500 animate-pulse shadow-[0_0_10px_rgba(244,63,94,1)]"></div>
                    <h3 className="text-sm font-bold text-rose-500 flex items-center gap-2">
                      Remediate Agent <Badge variant="outline" className="h-5 text-[10px] bg-rose-500/10 text-rose-500 border-rose-500/20 animate-pulse">Action Executed</Badge>
                    </h3>
                    <p className="text-xs text-neutral-400 mt-1">
                      {alerts[0].remediation?.remediation_summary || "Executed automated playbook."}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-neutral-500 text-center py-8">
                  <Activity className="h-8 w-8 mx-auto mb-2 opacity-20 animate-pulse" />
                  No active processing. Awaiting webhook from Splunk.
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
