import unittest
from app.render import render_message
class Rendering(unittest.TestCase):
    def test_notice(self):
        self.assertEqual(render_message('Alice', 'notice.j2'), 'To: Alice\nYour total is 42.\nSent with NotifyHub\n')
    def test_loop(self):
        self.assertEqual(render_message('Bo', 'report.j2'), 'Report for Bo\nItem 1: 1\nItem 2: 4\nItem 3: 9\n')
