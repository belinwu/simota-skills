import { useEffect, useState } from "react";
import { useDash } from "../store";

function formatElapsed(ms: number): string {
  const total = Math.floor(ms / 1000);
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function Header() {
  const runId = useDash((s) => s.runId);
  const connected = useDash((s) => s.connected);
  const goal = useDash((s) => s.state.goal);
  const mode = useDash((s) => s.state.mode);
  const startedAt = useDash((s) => s.state.startedAt);
  const endedAt = useDash((s) => s.state.endedAt);
  const engine = useDash((s) => s.state.engine);

  const [, force] = useState(0);
  useEffect(() => {
    if (endedAt) return;
    const id = setInterval(() => force((n) => n + 1), 1000);
    return () => clearInterval(id);
  }, [endedAt]);

  const elapsedMs = startedAt
    ? (endedAt ? new Date(endedAt).getTime() : Date.now()) -
      new Date(startedAt).getTime()
    : 0;

  return (
    <header className="header">
      <div className="header-left">
        <span className="run-id">{runId ?? "—"}</span>
        <span className="dot" data-on={connected ? "1" : "0"} title={connected ? "live" : "disconnected"} />
        <span className="goal">{goal ?? "(no goal)"}</span>
        {mode && <span className="badge mode">{mode}</span>}
        <span className={`badge engine engine-${engine}`}>{engine}</span>
      </div>
      <div className="header-right">
        <span className="elapsed">⏱ {formatElapsed(elapsedMs)}</span>
        {endedAt && <span className="badge done">DONE</span>}
        {endedAt && runId && (
          <a
            className="btn-postmortem"
            href={`/api/postmortem/${encodeURIComponent(runId)}`}
            target="_blank"
            rel="noreferrer"
            title="Generate / view postmortem markdown"
          >
            📄 postmortem
          </a>
        )}
      </div>
    </header>
  );
}
