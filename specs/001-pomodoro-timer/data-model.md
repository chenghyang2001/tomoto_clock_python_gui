# Data Model: 基本番茄鐘

**Branch**: `001-pomodoro-timer` | **Date**: 2026-02-17

## Entities

### TimerState（計時器運行狀態）

列舉值，代表計時器當前的運行狀態。

| 值 | 說明 |
|----|------|
| IDLE | 計時器停止，尚未開始或已重置 |
| RUNNING | 計時器正在倒數 |
| PAUSED | 計時器已暫停 |

### TimerMode（計時器模式）

列舉值，代表目前處於工作或休息階段。

| 值 | 說明 | 預設時間 |
|----|------|----------|
| WORK | 工作模式 | 25 分鐘（1500 秒） |
| BREAK | 休息模式 | 5 分鐘（300 秒） |

### Timer（計時器）

核心實體，管理倒數計時的所有狀態與邏輯。

| 屬性 | 型別 | 說明 |
|------|------|------|
| state | TimerState | 當前運行狀態 |
| mode | TimerMode | 當前模式（工作/休息） |
| remaining_seconds | int | 剩餘秒數 |
| work_duration | int | 工作時間長度（秒） |
| break_duration | int | 休息時間長度（秒） |

**行為**:

| 方法 | 說明 | 前置條件 |
|------|------|----------|
| start() | 開始倒數 | state == IDLE 或 PAUSED |
| pause() | 暫停倒數 | state == RUNNING |
| reset() | 重置至工作模式初始時間 | 任何狀態 |
| tick() | 減少 1 秒並檢查是否到達 00:00 | state == RUNNING |
| switch_mode() | 切換工作/休息模式 | 計時結束時 |

## State Transitions（狀態轉換）

```text
          start()          pause()
 IDLE ──────────→ RUNNING ────────→ PAUSED
  ↑                  │                 │
  │    reset()       │    reset()      │ start()
  ←──────────────────←─────────────────│
  ↑                                    │
  ←────────────────────────────────────←
                reset()

計時結束（tick() 到達 0）:
 RUNNING → IDLE（觸發音效 + 切換模式提示）
```

## Validation Rules

- `remaining_seconds` MUST >= 0 且 <= max(work_duration, break_duration)
- `start()` 在 `state == RUNNING` 時 MUST 為無操作（no-op）
- `pause()` 在 `state != RUNNING` 時 MUST 為無操作
- `reset()` MUST 將 state 設為 IDLE、mode 設為 WORK、
  remaining_seconds 設為 work_duration
