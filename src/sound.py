"""音效播放模組。

優先使用 winsound（Windows），失敗時退回 Tkinter bell。
所有播放操作為非阻塞且不拋出例外。
"""

import platform
import threading


def _beep_loop(duration_seconds: float, interval: float = 0.6) -> None:
    """在背景執行緒中重複播放提示音，持續指定秒數。"""
    import time
    try:
        import winsound
    except ImportError:
        return
    end_time = time.monotonic() + duration_seconds
    while time.monotonic() < end_time:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        time.sleep(interval)


def play_alert(widget=None, duration: float = 5.0) -> None:
    """播放計時結束提示音效，持續 duration 秒。

    在 Windows 上以背景執行緒重複播放 MessageBeep，不阻塞 UI。
    非 Windows 環境退回 Tkinter bell。
    """
    if platform.system() == "Windows":
        try:
            import winsound  # noqa: F401
            t = threading.Thread(target=_beep_loop, args=(duration,), daemon=True)
            t.start()
            return
        except Exception:
            pass

    # 跨平台備用方案：Tkinter bell
    if widget is not None:
        try:
            widget.bell()
        except Exception:
            pass
