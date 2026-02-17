"""音效播放模組。

優先使用 winsound（Windows），失敗時退回 Tkinter bell。
所有播放操作為非阻塞且不拋出例外。
"""

import platform


def play_alert(widget=None) -> None:
    """播放計時結束提示音效。

    嘗試 winsound（Windows 限定），失敗時使用 Tkinter bell。
    widget 參數為 Tkinter widget 實例，用於呼叫 bell()。
    """
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return
        except Exception:
            pass

    # 跨平台備用方案：Tkinter bell
    if widget is not None:
        try:
            widget.bell()
        except Exception:
            pass
