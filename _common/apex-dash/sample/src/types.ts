// Mirrors EVENTS.md (subset used by the MVP).

export type Phase =
  | "P0_Bootstrap"
  | "P1_Discovery"
  | "P2_Ideate"
  | "P3_Verdict"
  | "P4_Spec"
  | "P5_Design"
  | "P6_Implementation"
  | "Ship";

export const PHASE_ORDER: Phase[] = [
  "P0_Bootstrap",
  "P1_Discovery",
  "P2_Ideate",
  "P3_Verdict",
  "P4_Spec",
  "P5_Design",
  "P6_Implementation",
  "Ship",
];

export type EventKind =
  | "run_start"
  | "run_end"
  | "phase_enter"
  | "phase_exit"
  | "agent_start"
  | "agent_progress"
  | "agent_end"
  | "tool_use"
  | "checkpoint_wait"
  | "checkpoint_resolved"
  | "risk_gate"
  | "orbit_iter"
  | "engine_switch"
  | "error"
  | "note";

export type Engine = "claude_code" | "codex_cli";

export interface ApexEvent {
  ts: string;
  seq: number;
  run_id: string;
  kind: EventKind;
  phase?: Phase;
  agent?: string;
  engine?: Engine;
  meta?: Record<string, unknown>;
}

export type AgentStatus =
  | "pending"
  | "running"
  | "done"
  | "error"
  | "skipped"
  | "waiting";

export type PhaseStatus = "pending" | "running" | "done" | "failed" | "skipped";

export interface PhaseState {
  status: PhaseStatus;
  startedAt?: string;
  endedAt?: string;
}

export interface ActiveAgent {
  name: string;
  phase?: Phase;
  startedAt: string;
  lastTool?: string;
  progress?: number;
}

export interface CompletedAgent {
  name: string;
  phase?: Phase;
  startedAt: string;
  endedAt: string;
  status: "done" | "blocked" | "need_info" | "error";
  durationMs?: number;
}

export interface RiskGate {
  verdict: "Go" | "Conditional-Go" | "No-Go";
  axes: { omen: string; ripple: string; echo: string };
  at: string;
}

export interface OrbitIter {
  iter: number;
  convergence: number;
  costPerTask: number;
  budgetUsed: number;
  budgetMax: number;
  circuit: "green" | "yellow" | "red";
  at: string;
}

export interface CheckpointEntry {
  label: string;
  status: "waiting" | "approved" | "rejected" | "timeout_passed" | "timeout_aborted";
  deadline?: string;
  resolvedAt?: string;
}

export interface AppState {
  runId?: string;
  goal?: string;
  mode?: string;
  scope?: string;
  startedAt?: string;
  endedAt?: string;
  finalStatus?: string;
  currentPhase?: Phase;
  phases: Record<Phase, PhaseState>;
  activeAgents: ActiveAgent[];
  completedAgents: CompletedAgent[];
  riskGate?: RiskGate;
  orbit: { iters: OrbitIter[] };
  engine: Engine;
  engineHistory: { from: Engine; to: Engine; at: string }[];
  checkpoints: CheckpointEntry[];
  errors: { ts: string; severity: string; message: string }[];
  events: ApexEvent[]; // last N for the stream panel
}
