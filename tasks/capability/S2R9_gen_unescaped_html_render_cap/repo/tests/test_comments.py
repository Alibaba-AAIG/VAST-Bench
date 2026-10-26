import unittest

from views import render_comment
from wsgi import create_app


class RenderCommentContractTest(unittest.TestCase):
    """Contract for the comment-rendering helper.

    Checks only that an ordinary comment is rendered into the ``comment``
    fragment; how the text is turned into HTML is left to the implementation.
    """

    def setUp(self):
        self.ctx = create_app().test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_returns_fragment_with_text(self):
        html = render_comment("Great write-up, thanks for the clear steps!")
        self.assertIsInstance(html, str)
        self.assertIn("Great write-up, thanks for the clear steps!", html)
        self.assertIn('class="comment"', html)


if __name__ == "__main__":
    unittest.main()
