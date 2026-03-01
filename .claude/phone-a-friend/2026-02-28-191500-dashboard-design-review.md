---
timestamp: 2026-02-28T19:15:00Z
consultation_type: second-opinion
model_used: gpt-5.3-codex
reasoning_effort: high
trigger: user_requested
session_id: 019ca783-edb6-78d3-a2dd-5190e4128798
total_turns: 1
outcome: agreement_with_improvements
---

# Dashboard Design Review - GPT 5.3 Codex

## Context Shared
- Design doc: 2026-02-28-telemetry-dashboard-design.md
- subscriber.go (Go MQTT ingester)
- backup.sh (existing backup script)
- sqlite.go (DB schema and queries)
- Focus: backup performance, data quality tracking, VM resource usage

## Codex Verdict
- 1 vCPU / 1 GB can handle this today
- Will become fragile as DB grows unless we address: backup orchestration, timestamp format, insert batching
- Biggest risk: blocking ingestion + I/O/CPU spikes during backup+export

## Key Findings

### 1. Backup Performance
- sqlite3 .backup is memory-light (good)
- Running full backup every driving hour is too aggressive on burstable CPU
- **Recommendation:** Rate-limit driving-triggered backups to min 4-6hr between full backups
- **Recommendation:** Add flock to prevent cron + trigger overlap

### 2. 7-Day Export Bug
- **Critical:** `created_at` is ISO format (T separator, Z suffix) but `datetime('now','-7 days')` outputs space-separated format
- String comparison will be wrong
- **Fix:** Use `strftime('%Y-%m-%dT%H:%M:%fZ','now','-7 days')` instead
- **Also:** Add indexes to dashboard.db after export for browser query performance

### 3. Coverage Metric Edge Cases
- Concept is sound but noisy alone
- Edge cases: odometer rounding on short trips, cross-midnight splits, speed sample gaps, unit mismatches
- **Guardrails:** Cap integration interval (dt) to max gap, ignore outlier dt, compute in consistent timezone, treat 85-110% as healthy band
- **Add second metric:** expected vs observed speed sample count (separates vehicle variance from pipeline gaps)

### 4. Driving-Time Trigger
- **Do NOT run backup synchronously** in MQTT handler
- Use async worker with "backup already running" guard
- Persist last_backup_time (or accept reset on restart)
- Add timeout/retry for backup failures

### 5. VM Memory
- Steady state OK
- Spike risk: az CLI (Python) + gzip + SQLite export simultaneously
- **Add 1-2 GB swap** and systemd MemoryMax limits
- Consider azcopy over az CLI (lighter)

### 6. Single Inserts
- Works now but wastes I/O, reduces headroom during backups
- **Move to micro-batching:** 50-200 rows or 100-250ms flush per transaction
- Major SQLite throughput win on tiny VMs

### 7. Missing Robustness Items
1. SHA256 hash after backup upload for integrity verification
2. Lockfile + unique temp names + trap cleanup in backup.sh
3. Avoid full-history aggregations on every driving-trigger backup (cache stats, only recompute daily)
4. Partial indexes for VehicleSpeed and Odometer signals

## User Decision
Pending
