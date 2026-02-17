"""番茄鐘計時器邏輯模組。

將計時邏輯與 UI 完全分離，確保可獨立測試。
"""

from enum import Enum


class TimerState(Enum):
    """計時器運行狀態。"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"


class TimerMode(Enum):
    """計時器模式：工作或休息。"""
    WORK = "work"
    BREAK = "break"


class Timer:
    """番茄鐘計時器，管理倒數計時的狀態與邏輯。"""

    def __init__(
        self, work_duration: int = 60, break_duration: int = 60
    ) -> None:
        self._work_duration = work_duration
        self._break_duration = break_duration
        self._state = TimerState.IDLE
        self._mode = TimerMode.WORK
        self._remaining_seconds = work_duration

    @property
    def state(self) -> TimerState:
        return self._state

    @property
    def mode(self) -> TimerMode:
        return self._mode

    @property
    def remaining_seconds(self) -> int:
        return self._remaining_seconds

    @property
    def work_duration(self) -> int:
        return self._work_duration

    @property
    def break_duration(self) -> int:
        return self._break_duration

    def start(self) -> None:
        """開始或恢復倒數。RUNNING 時為 no-op。"""
        if self._state in (TimerState.IDLE, TimerState.PAUSED):
            self._state = TimerState.RUNNING

    def tick(self) -> bool:
        """減少 1 秒。回傳 True 若到達 00:00。"""
        if self._state != TimerState.RUNNING:
            return False
        if self._remaining_seconds > 0:
            self._remaining_seconds -= 1
        if self._remaining_seconds == 0:
            self._state = TimerState.IDLE
            return True
        return False

    def pause(self) -> None:
        """暫停倒數。非 RUNNING 時為 no-op。"""
        if self._state == TimerState.RUNNING:
            self._state = TimerState.PAUSED

    def reset(self) -> None:
        """重置至工作模式初始狀態。"""
        self._state = TimerState.IDLE
        self._mode = TimerMode.WORK
        self._remaining_seconds = self._work_duration

    def set_durations(self, work_duration: int, break_duration: int) -> None:
        """設定工作與休息時長（秒），僅在 IDLE 狀態生效。"""
        if self._state != TimerState.IDLE:
            return
        self._work_duration = work_duration
        self._break_duration = break_duration
        if self._mode == TimerMode.WORK:
            self._remaining_seconds = work_duration
        else:
            self._remaining_seconds = break_duration

    def switch_mode(self) -> None:
        """切換工作/休息模式並重設時間。"""
        if self._mode == TimerMode.WORK:
            self._mode = TimerMode.BREAK
            self._remaining_seconds = self._break_duration
        else:
            self._mode = TimerMode.WORK
            self._remaining_seconds = self._work_duration
        self._state = TimerState.IDLE

    def formatted_time(self) -> str:
        """回傳 'MM:SS' 格式字串。"""
        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
