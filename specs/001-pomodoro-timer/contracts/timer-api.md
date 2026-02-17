# Internal API Contract: Timer 模組

**Branch**: `001-pomodoro-timer` | **Date**: 2026-02-17

此為桌面應用程式的內部模組契約（非 REST API）。
定義 `timer.py` 模組對外暴露的公開介面。

## Timer 類別

### 建構子

```text
Timer(work_duration: int = 1500, break_duration: int = 300)
```

- `work_duration`：工作時間（秒），預設 1500（25 分鐘）
- `break_duration`：休息時間（秒），預設 300（5 分鐘）
- 初始狀態：state=IDLE, mode=WORK, remaining_seconds=work_duration

### 公開方法

| 方法 | 回傳值 | 說明 |
|------|--------|------|
| `start()` | `None` | 開始或恢復倒數 |
| `pause()` | `None` | 暫停倒數 |
| `reset()` | `None` | 重置至 WORK/IDLE/25:00 |
| `tick()` | `bool` | 減 1 秒，回傳 `True` 若到達 00:00 |
| `switch_mode()` | `None` | 切換 WORK ↔ BREAK 並重設時間 |
| `formatted_time()` | `str` | 回傳 "MM:SS" 格式字串 |

### 公開屬性（唯讀）

| 屬性 | 型別 | 說明 |
|------|------|------|
| `state` | `TimerState` | 當前運行狀態 |
| `mode` | `TimerMode` | 當前模式 |
| `remaining_seconds` | `int` | 剩餘秒數 |

### 行為契約

- `start()`: IDLE/PAUSED → RUNNING；RUNNING 時無效果
- `pause()`: RUNNING → PAUSED；非 RUNNING 時無效果
- `reset()`: 任何狀態 → IDLE + WORK + work_duration
- `tick()`: RUNNING 且 remaining_seconds > 0 → 減 1；
  到達 0 時回傳 True 並將 state 設為 IDLE
- `switch_mode()`: WORK → BREAK（設 break_duration）；
  BREAK → WORK（設 work_duration）；state 設為 IDLE

## Sound 模組

### 公開函式

```text
play_alert() -> None
```

- 播放提示音效，非阻塞
- Windows 上使用 `winsound.MessageBeep()`
- 其他平台使用 Tkinter `bell()`
- 播放失敗時靜默處理（不拋出例外）
