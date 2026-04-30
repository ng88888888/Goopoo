"""
Desktop Goose Pet
- Appears when Telegram opens
- Plays a random animation from the library
- Auto-quits after Telegram is idle (not frontmost) for 15 minutes
- Lives in the upper-right corner of the screen
"""

import sys
import os
import random
import subprocess
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

import Cocoa  # pyobjc — detects frontmost app on macOS

SPRITE_DIR = os.path.join(os.path.dirname(__file__), "sprites")
IDLE_TIMEOUT_MS = 15 * 60 * 1000  # 15 minutes in milliseconds
POLL_INTERVAL_MS = 3000            # check Telegram every 3 seconds
FRAME_MS = 180                     # animation speed (ms per frame)
SCALE = 6                          # must match sprites.py
CANVAS = 32                        # logical pixel canvas size


# Animation sequences (lists of sprite filenames without extension)
ANIMATIONS = {
    "enter": [f"enter_{i}" for i in range(1, 7)],
    "dance":        [f"dance_{i}"        for i in range(1, 7)],
    "sleep":        [f"sleep_{i}"        for i in range(1, 5)],
    "bye":          [f"bye_{i}"          for i in range(1, 5)],
    "idle":         [f"idle_{i}"         for i in range(1, 5)],
    "poop_waddle":  [f"poop_waddle_{i}"  for i in range(1, 9)],
}

# Animations that can be randomly picked on startup (after enter plays)
RANDOM_POOL = ["dance", "sleep", "idle", "poop_waddle"]


def is_telegram_running():
    result = subprocess.run(["pgrep", "-x", "Telegram"], capture_output=True)
    return result.returncode == 0


def frontmost_app_name():
    try:
        app = Cocoa.NSWorkspace.sharedWorkspace().frontmostApplication()
        return app.localizedName() if app else ""
    except Exception:
        return ""


class GoosePet(QWidget):
    def __init__(self):
        super().__init__()
        self._build_window()
        self._load_sprites()

        self.current_frames = []
        self.frame_index = 0
        self.loop_animation = True
        self.pending_animation = None

        # Timers
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self._next_frame)

        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self._check_telegram)
        self.poll_timer.start(POLL_INTERVAL_MS)

        self.idle_timer = QTimer()
        self.idle_timer.setSingleShot(True)
        self.idle_timer.timeout.connect(self._quit_with_bye)
        self.idle_timer.start(IDLE_TIMEOUT_MS)

        # Start: play enter animation, then random
        self._play("enter", loop=False, then=self._pick_random_loop)

    # ── Window setup ──────────────────────────────────────────────

    def _build_window(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool                 # hides from Dock and Cmd+Tab
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(CANVAS * SCALE, CANVAS * SCALE)

        screen = QApplication.primaryScreen().geometry()
        margin = 20
        self.move(screen.width() - self.width() - margin, margin)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, CANVAS * SCALE, CANVAS * SCALE)

    # ── Sprite loading ────────────────────────────────────────────

    def _load_sprites(self):
        self.pixmaps = {}
        for name_list in ANIMATIONS.values():
            for name in name_list:
                path = os.path.join(SPRITE_DIR, f"{name}.png")
                if os.path.exists(path):
                    self.pixmaps[name] = QPixmap(path)

    # ── Animation control ─────────────────────────────────────────

    def _play(self, anim_name, loop=True, then=None):
        self.frame_timer.stop()
        frames = ANIMATIONS.get(anim_name, ANIMATIONS["idle"])
        self.current_frames = [self.pixmaps[f] for f in frames if f in self.pixmaps]
        self.frame_index = 0
        self.loop_animation = loop
        self._on_anim_done = then
        if self.current_frames:
            self.label.setPixmap(self.current_frames[0])
        self.frame_timer.start(FRAME_MS)

    def _next_frame(self):
        if not self.current_frames:
            return
        self.frame_index += 1
        if self.frame_index >= len(self.current_frames):
            if self.loop_animation:
                self.frame_index = 0
            else:
                self.frame_timer.stop()
                if callable(self._on_anim_done):
                    self._on_anim_done()
                return
        self.label.setPixmap(self.current_frames[self.frame_index])

    def _pick_random_loop(self):
        choice = random.choice(RANDOM_POOL)
        self._play(choice, loop=True)

    # ── Telegram watching ─────────────────────────────────────────

    def _check_telegram(self):
        name = frontmost_app_name()
        if name == "Telegram":
            # User is actively using Telegram — reset idle timer
            self.idle_timer.start(IDLE_TIMEOUT_MS)

    # ── Quit ──────────────────────────────────────────────────────

    def _quit_with_bye(self):
        self._play("bye", loop=False, then=QApplication.quit)

    # ── Quit ──────────────────────────────────────────────────────

    def _quit_with_bye(self):
        self._play("bye", loop=False, then=QApplication.quit)

    # ── Mouse events ──────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.pos()
        elif event.button() == Qt.RightButton:
            self._quit_with_bye()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._play("poop_waddle", loop=False, then=self._pick_random_loop)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_offset)


def wait_for_telegram():
    """Block until Telegram is running, then launch the pet."""
    print("Waiting for Telegram to open...")
    while not is_telegram_running():
        import time
        time.sleep(2)
    print("Telegram detected — launching goose!")


if __name__ == "__main__":
    wait_for_telegram()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    pet = GoosePet()
    pet.show()

    sys.exit(app.exec_())
