"""番茄鐘 Tkinter UI 模組。

負責所有視窗元件的建立、事件處理與計時器更新迴圈。
"""

import time
import tkinter as tk

from src.sound import play_alert
from src.timer import Timer, TimerMode, TimerState

# 模式對應的中文顯示文字與顏色
_MODE_DISPLAY = {
    TimerMode.WORK: ("工作中", "#D32F2F"),
    TimerMode.BREAK: ("休息中", "#388E3C"),
}


class PomodoroApp:
    """番茄鐘主視窗應用程式。"""

    # after() 呼叫間隔（毫秒）
    TICK_INTERVAL_MS = 200

    def __init__(self, root: tk.Tk, timer: Timer) -> None:
        self._root = root
        self._timer = timer
        self._after_id: str | None = None
        # 用於校正計時誤差的時間基準
        self._last_tick_time: float = 0.0

        self._setup_window()
        self._create_widgets()
        self._update_display()

    def _setup_window(self) -> None:
        self._root.title("番茄時鐘")
        self._root.resizable(False, False)

    def _create_widgets(self) -> None:
        """建立所有 UI 元件。"""
        # 模式顯示標籤
        self._mode_label = tk.Label(
            self._root,
            text="工作中",
            font=("Helvetica", 20),
            fg="#D32F2F",
        )
        self._mode_label.pack(pady=(20, 0))

        # 計時器顯示（大型 MM:SS）
        self._time_label = tk.Label(
            self._root,
            text=self._timer.formatted_time(),
            font=("Helvetica", 72, "bold"),
        )
        self._time_label.pack(pady=(10, 20))

        # 按鈕區域
        button_frame = tk.Frame(self._root)
        button_frame.pack(pady=(0, 30))

        self._start_pause_button = tk.Button(
            button_frame,
            text="開始",
            font=("Helvetica", 16),
            width=8,
            command=self._on_start_pause,
        )
        self._start_pause_button.pack(side=tk.LEFT, padx=5)

        self._reset_button = tk.Button(
            button_frame,
            text="重置",
            font=("Helvetica", 16),
            width=8,
            command=self._on_reset,
            state=tk.DISABLED,
        )
        self._reset_button.pack(side=tk.LEFT, padx=5)

    def _on_start_pause(self) -> None:
        """處理開始/暫停/繼續按鈕點擊。

        根據目前計時器狀態決定行為：
        IDLE → start，RUNNING → pause，PAUSED → start（繼續）。
        """
        if self._timer.state == TimerState.RUNNING:
            self._timer.pause()
            self._cancel_tick()
        else:
            self._timer.start()
            self._last_tick_time = time.monotonic()
            self._schedule_tick()
        self._update_display()

    def _on_reset(self) -> None:
        """處理重置按鈕點擊。"""
        self._cancel_tick()
        self._timer.reset()
        self._update_display()

    def _cancel_tick(self) -> None:
        """取消排程中的 tick 回呼。"""
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None

    def _schedule_tick(self) -> None:
        """排程下一次 tick 回呼。"""
        self._cancel_tick()
        self._after_id = self._root.after(
            self.TICK_INTERVAL_MS, self._tick_callback
        )

    def _tick_callback(self) -> None:
        """Tkinter after() 回呼：根據實際經過時間執行 tick。

        使用 time.monotonic() 計算實際經過時間，
        避免 after() 延遲造成的累積誤差。
        """
        if self._timer.state != TimerState.RUNNING:
            self._after_id = None
            return

        now = time.monotonic()
        elapsed = now - self._last_tick_time

        # 每經過 1 秒執行一次 tick
        if elapsed >= 1.0:
            ticks = int(elapsed)
            self._last_tick_time += ticks
            for _ in range(ticks):
                finished = self._timer.tick()
                if finished:
                    self._on_timer_finished()
                    return

        self._update_display()
        self._schedule_tick()

    def _on_timer_finished(self) -> None:
        """計時結束時的處理：播放音效並自動切換模式。"""
        self._after_id = None
        play_alert(self._root)
        self._timer.switch_mode()
        self._update_display()

    def _update_display(self) -> None:
        """更新所有 UI 元件以反映當前計時器狀態。"""
        self._time_label.config(text=self._timer.formatted_time())

        # 模式顯示
        mode_text, mode_color = _MODE_DISPLAY[self._timer.mode]
        self._mode_label.config(text=mode_text, fg=mode_color)

        # 按鈕文字與狀態連動
        state = self._timer.state
        if state == TimerState.IDLE:
            self._start_pause_button.config(text="開始")
            self._reset_button.config(state=tk.DISABLED)
        elif state == TimerState.RUNNING:
            self._start_pause_button.config(text="暫停")
            self._reset_button.config(state=tk.NORMAL)
        elif state == TimerState.PAUSED:
            self._start_pause_button.config(text="繼續")
            self._reset_button.config(state=tk.NORMAL)
