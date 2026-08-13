from __future__ import annotations

import unittest

from autobox.app.core.config import Settings


class SettingsTest(unittest.TestCase):
    def test_rejects_placeholder_base_url(self) -> None:
        settings = Settings(
            ollama_api_key="test-key",
            ollama_base_url="your_ollama_cloud_endpoint",
            ollama_model="gpt-oss:120b-cloud",
            app_timezone="Asia/Ho_Chi_Minh",
            ollama_timeout_seconds=1,
            agent_max_tokens=512,
        )

        with self.assertRaises(RuntimeError):
            settings.require_ollama_credentials()


if __name__ == "__main__":
    unittest.main()
