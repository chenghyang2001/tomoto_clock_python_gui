"""音效播放模組。

使用標準庫產生可調音量的提示音。
優先使用 winsound（Windows），失敗時退回 Tkinter bell。
所有播放操作為非阻塞且不拋出例外。
"""

import io
import math
import platform
import struct
import threading
import wave


def _generate_tone_wav(
    frequency: int = 880,
    duration_ms: int = 400,
    volume: float = 1.0,
    sample_rate: int = 44100,
) -> bytes:
    """產生指定頻率、時長與音量的 WAV 音訊資料（記憶體中）。"""
    n_samples = sample_rate * duration_ms // 1000
    amplitude = int(32767 * max(0.0, min(1.0, volume)))
    samples = []
    for i in range(n_samples):
        value = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(struct.pack("<h", int(value)))
    raw = b"".join(samples)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw)
    return buf.getvalue()


def _beep_loop(duration_seconds: float, volume: float) -> None:
    """在背景執行緒中重複播放提示音，持續指定秒數。"""
    import time

    try:
        import winsound
    except ImportError:
        return

    tone_data = _generate_tone_wav(frequency=880, duration_ms=400, volume=volume)
    end_time = time.monotonic() + duration_seconds
    while time.monotonic() < end_time:
        winsound.PlaySound(tone_data, winsound.SND_MEMORY)
        time.sleep(0.15)


def play_alert(widget=None, duration: float = 5.0, volume: float = 1.0) -> None:
    """播放計時結束提示音效，持續 duration 秒。

    volume: 0.0（靜音）到 1.0（最大音量）。
    在 Windows 上以背景執行緒播放自訂音調，不阻塞 UI。
    非 Windows 環境退回 Tkinter bell。
    """
    if volume <= 0.0:
        return

    if platform.system() == "Windows":
        try:
            import winsound  # noqa: F401

            t = threading.Thread(
                target=_beep_loop, args=(duration, volume), daemon=True
            )
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
