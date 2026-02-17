# Research: 基本番茄鐘

**Branch**: `001-pomodoro-timer` | **Date**: 2026-02-17

## R1: Tkinter 計時器實作方式

**Decision**: 使用 Tkinter 的 `after()` 方法實作每秒回呼

**Rationale**:
- `after(ms, callback)` 是 Tkinter 內建的非阻塞定時器機制
- 不需要額外的 threading 或 asyncio
- 在主事件迴圈中執行，天然線程安全
- 視窗最小化或失去焦點時仍會觸發回呼

**Alternatives considered**:
- `threading.Timer`：需處理線程同步問題，且 Tkinter
  不支援從非主線程更新 UI，增加不必要的複雜度
- `time.sleep()` 搭配迴圈：會阻塞主線程，導致 UI 凍結
- `sched` 模組：適合一次性排程，不適合每秒重複回呼

**實作要點**:
- 每次 `after()` 回呼中計算實際經過的時間差（而非假設固定
  1000ms），以避免長時間運行後的累積誤差
- 使用 `time.monotonic()` 作為時間基準，不受系統時鐘調整影響

## R2: 音效提醒方案

**Decision**: 使用 Tkinter 的 `widget.bell()` 作為主要音效，
搭配 `winsound.MessageBeep()` 作為 Windows 增強方案

**Rationale**:
- `widget.bell()` 是 Tkinter 內建方法，跨平台可用，
  零外部依賴
- Windows 上 `winsound` 屬於標準庫，可提供更明顯的提示音
- 兩者皆為標準庫，符合「標準庫優先」原則

**Alternatives considered**:
- `playsound` 第三方套件：功能更豐富但違反標準庫優先原則
- `pygame.mixer`：過度引入大型依賴
- 直接寫入 WAV 位元組並用 `winsound.PlaySound()`：
  增加不必要的複雜度

**實作要點**:
- 嘗試 `winsound`（Windows），失敗時退回 `widget.bell()`
- 音效播放 MUST 為非阻塞（使用 `winsound.SND_ASYNC` 旗標）

## R3: 計時器狀態管理

**Decision**: 使用簡單的列舉（Enum）管理狀態，不引入狀態機
框架

**Rationale**:
- 番茄鐘只有 3 種運行狀態（IDLE、RUNNING、PAUSED）
  和 2 種模式（WORK、BREAK），複雜度極低
- Python 的 `enum.Enum` 屬於標準庫
- 簡單的 if/elif 分支即可處理所有狀態轉換

**Alternatives considered**:
- `transitions` 第三方狀態機：功能強大但對此場景過度設計
- 字串比對（如 `state == "running"`）：容易打錯字，
  缺乏 IDE 補全支援
- dataclass + property：增加程式碼量但無明顯收益

## R4: UI 佈局設計

**Decision**: 使用 Tkinter 的 `pack` 佈局管理器，
垂直排列所有元件

**Rationale**:
- 番茄鐘 UI 為簡單的垂直佈局：模式標籤 → 計時器 → 按鈕列
- `pack` 是最簡單的 Tkinter 佈局管理器，
  適合線性排列的場景
- 不需要 `grid` 或 `place` 的定位精確度

**Alternatives considered**:
- `grid` 佈局：對此簡單佈局多餘，但如果按鈕排列複雜
  可考慮按鈕區域用 grid
- `place` 絕對定位：不利於視窗縮放
- ttk 主題化元件：外觀更現代，但增加了學習成本。
  按鈕區域可考慮使用 `ttk.Button` 提升外觀
