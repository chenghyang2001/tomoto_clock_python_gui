"""Timer 類別單元測試。"""

from src.timer import Timer, TimerMode, TimerState


class TestTimerInit:
    """建構子測試。"""

    def test_default_values(self) -> None:
        t = Timer()
        assert t.state == TimerState.IDLE
        assert t.mode == TimerMode.WORK
        assert t.remaining_seconds == 1500
        assert t.work_duration == 1500
        assert t.break_duration == 300

    def test_custom_durations(self) -> None:
        t = Timer(work_duration=600, break_duration=120)
        assert t.remaining_seconds == 600
        assert t.work_duration == 600
        assert t.break_duration == 120


class TestTimerStart:
    """start() 測試。"""

    def test_idle_to_running(self) -> None:
        t = Timer()
        t.start()
        assert t.state == TimerState.RUNNING

    def test_paused_to_running(self) -> None:
        t = Timer()
        t.start()
        t.pause()
        t.start()
        assert t.state == TimerState.RUNNING

    def test_running_is_noop(self) -> None:
        t = Timer()
        t.start()
        t.start()
        assert t.state == TimerState.RUNNING


class TestTimerPause:
    """pause() 測試。"""

    def test_running_to_paused(self) -> None:
        t = Timer()
        t.start()
        t.pause()
        assert t.state == TimerState.PAUSED

    def test_idle_is_noop(self) -> None:
        t = Timer()
        t.pause()
        assert t.state == TimerState.IDLE

    def test_paused_is_noop(self) -> None:
        t = Timer()
        t.start()
        t.pause()
        t.pause()
        assert t.state == TimerState.PAUSED


class TestTimerReset:
    """reset() 測試。"""

    def test_from_running(self) -> None:
        t = Timer()
        t.start()
        t.tick()
        t.reset()
        assert t.state == TimerState.IDLE
        assert t.mode == TimerMode.WORK
        assert t.remaining_seconds == 1500

    def test_from_paused(self) -> None:
        t = Timer()
        t.start()
        t.tick()
        t.pause()
        t.reset()
        assert t.state == TimerState.IDLE
        assert t.remaining_seconds == 1500

    def test_from_break_mode(self) -> None:
        """休息模式下重置 MUST 回到工作模式。"""
        t = Timer(work_duration=2, break_duration=60)
        t.start()
        t.tick()
        t.tick()  # 到達 00:00 → IDLE
        t.switch_mode()  # 切換到休息
        t.reset()
        assert t.mode == TimerMode.WORK
        assert t.remaining_seconds == 2


class TestTimerTick:
    """tick() 測試。"""

    def test_decrements_by_one(self) -> None:
        t = Timer(work_duration=10)
        t.start()
        t.tick()
        assert t.remaining_seconds == 9

    def test_returns_false_when_not_finished(self) -> None:
        t = Timer(work_duration=10)
        t.start()
        assert t.tick() is False

    def test_returns_true_at_zero(self) -> None:
        t = Timer(work_duration=1)
        t.start()
        assert t.tick() is True
        assert t.remaining_seconds == 0
        assert t.state == TimerState.IDLE

    def test_idle_is_noop(self) -> None:
        t = Timer()
        result = t.tick()
        assert result is False
        assert t.remaining_seconds == 1500

    def test_paused_is_noop(self) -> None:
        t = Timer()
        t.start()
        t.tick()
        t.pause()
        remaining = t.remaining_seconds
        result = t.tick()
        assert result is False
        assert t.remaining_seconds == remaining


class TestTimerSwitchMode:
    """switch_mode() 測試。"""

    def test_work_to_break(self) -> None:
        t = Timer(work_duration=1500, break_duration=300)
        t.switch_mode()
        assert t.mode == TimerMode.BREAK
        assert t.remaining_seconds == 300
        assert t.state == TimerState.IDLE

    def test_break_to_work(self) -> None:
        t = Timer(work_duration=1500, break_duration=300)
        t.switch_mode()
        t.switch_mode()
        assert t.mode == TimerMode.WORK
        assert t.remaining_seconds == 1500
        assert t.state == TimerState.IDLE


class TestTimerFormattedTime:
    """formatted_time() 測試。"""

    def test_full_time(self) -> None:
        t = Timer(work_duration=1500)
        assert t.formatted_time() == "25:00"

    def test_zero(self) -> None:
        t = Timer(work_duration=1)
        t.start()
        t.tick()
        assert t.formatted_time() == "00:00"

    def test_single_digit_seconds(self) -> None:
        t = Timer(work_duration=65)
        assert t.formatted_time() == "01:05"

    def test_break_time(self) -> None:
        t = Timer(break_duration=300)
        t.switch_mode()
        assert t.formatted_time() == "05:00"
