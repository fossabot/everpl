import unittest
import uuid
import threading
import asyncio

from dpl.auth.auth_context import AuthContext


class TestAuthContext(unittest.TestCase):
    def test_same_thread(self):
        ac = AuthContext()
        token = uuid.uuid4().hex

        self.assertIsNone(ac.current_token)

        with ac(token=token):
            self.assertEqual(ac.current_token, token)

        self.assertIsNone(ac.current_token)

    def test_thread_separation(self):
        def _check_token_unavailable():
            self.assertIsNone(ac.current_token)

        ac = AuthContext()
        token = uuid.uuid4().hex

        thread = threading.Thread(target=_check_token_unavailable)
        thread2 = threading.Thread(target=_check_token_unavailable)

        with ac(token=token):
            thread.start()
            thread2.start()

            thread.join()
            thread2.join()

    def test_thread_unique_tokens(self):
        def _enter_context_and_save_token():
            token = uuid.uuid4().hex

            with ac(token=token):
                tokens.append(token)

        tokens = list()
        ac = AuthContext()

        thread = threading.Thread(target=_enter_context_and_save_token)
        thread2 = threading.Thread(target=_enter_context_and_save_token)

        thread.start()
        thread2.start()

        thread.join()
        thread2.join()

        self.assertTrue(
            len(tokens) == 2
        )

        self.assertNotEqual(
            tokens[0], tokens[1]
        )

    def test_task_separation(self):
        async def _check_token_unavailable():
            self.assertIsNone(ac.current_token)

        ac = AuthContext()
        token = uuid.uuid4().hex
        loop = asyncio.get_event_loop()

        with ac(token=token):
            loop.run_until_complete(_check_token_unavailable())
            loop.run_until_complete(_check_token_unavailable())

    def test_task_unique_tokens(self):
        async def _enter_context_and_save_token():
            token = uuid.uuid4().hex

            with ac(token=token):
                tokens.append(token)
                await asyncio.sleep(0.02)

                self.assertTrue(
                    len(tokens) == 2
                )

        tokens = list()
        ac = AuthContext()
        loop = asyncio.get_event_loop()

        t1 = asyncio.ensure_future(_enter_context_and_save_token())
        t2 = asyncio.ensure_future(_enter_context_and_save_token())

        loop.run_until_complete(t1)
        loop.run_until_complete(t2)

        self.assertTrue(
            len(tokens) == 2
        )

        self.assertNotEqual(
            tokens[0], tokens[1]
        )
