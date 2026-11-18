import os
import sys
import types
import unittest

# Permitir importar los módulos sin instalar 'requests' (solo se usa en config.py)
sys.modules.setdefault("requests", types.ModuleType("requests"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from modules.ffmpeg import build_cmd, to_int  # noqa: E402


class ToIntTest(unittest.TestCase):
    def test_parses_and_defaults(self):
        self.assertEqual(to_int("90", 0), 90)
        self.assertEqual(to_int(180, 0), 180)
        self.assertEqual(to_int("", 0), 0)
        self.assertEqual(to_int(None, 30), 30)
        self.assertEqual(to_int("AUTO", 30), 30)


class BuildCmdTest(unittest.TestCase):
    def test_empty_rotation_and_auto_fps_do_not_crash(self):
        # Caso real: cámaras auto-registradas por heartbeat llegan con rotation "" y fps "AUTO"
        cmd, _, _, source_type = build_cmd({"name": "salon", "sourceType": "v4l2", "rotation": "", "fps": "AUTO"})
        self.assertEqual(source_type, "v4l2")
        self.assertIn("30", cmd)
        self.assertNotIn("transpose=1", " ".join(cmd))

    def test_rotation_as_string(self):
        cmd, _, _, _ = build_cmd({"name": "salon", "sourceType": "v4l2", "rotation": "90"})
        self.assertIn("transpose=1", cmd)

    def test_rtsp_copy_without_rotation(self):
        cmd, _, _, source_type = build_cmd({"name": "ip", "sourceType": "rtsp", "sourceUrl": "rtsp://cam/stream"})
        self.assertEqual(source_type, "rtsp")
        self.assertIn("copy", cmd)


if __name__ == "__main__":
    unittest.main()
