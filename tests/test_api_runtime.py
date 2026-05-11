from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import requests

from talentlens.api import app


class APIRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self._original_env = os.environ.copy()
        os.environ["TALENTLENS_DATA_DIR"] = self._temp_dir.name
        os.environ["EMBEDDING_BACKEND"] = "hash"
        os.environ["LLM_PROVIDER"] = "mock"
        self.client = TestClient(app)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._original_env)
        self._temp_dir.cleanup()

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_upload_resume_works_with_default_mock_provider(self) -> None:
        payload = b"Alex Johnson\nSkills: Python, SQL\nExperience:\nBuilt analytics pipelines."
        response = self.client.post(
            "/upload_resume",
            files={"file": ("resume.txt", payload, "text/plain")},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("resume_id", body)
        self.assertIn("chunks_indexed", body)
        self.assertIsInstance(body["chunks_indexed"], int)

    def test_upload_resume_returns_503_when_ollama_unreachable(self) -> None:
        os.environ["LLM_PROVIDER"] = "ollama"
        payload = b"Alex Johnson\nSkills: Python, SQL"
        with patch("talentlens.llm.requests.post", side_effect=requests.RequestException):
            response = self.client.post(
                "/upload_resume",
                files={"file": ("resume.txt", payload, "text/plain")},
            )
        self.assertEqual(response.status_code, 503)
        self.assertIn("ollama", response.json()["detail"].lower())

    def test_chat_nonexistent_resume_id_returns_404(self) -> None:
        response = self.client.post(
            "/chat",
            json={
                "resume_id": "fake_resume_id",
                "question": "What skills are listed?",
                "top_k": 2,
            },
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"].lower())

    def test_chat_malformed_resume_id_returns_422(self) -> None:
        response = self.client.post(
            "/chat",
            json={
                "resume_id": "../bad",
                "question": "What skills are listed?",
                "top_k": 2,
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("string_pattern_mismatch", response.text)

    def test_chat_nonexistent_generated_style_resume_id_returns_404(self) -> None:
        response = self.client.post(
            "/chat",
            json={
                "resume_id": "res_upload_abcdef12",
                "question": "What skills are listed?",
                "top_k": 2,
            },
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"].lower())

    def test_chat_works_for_existing_resume_id(self) -> None:
        upload_response = self.client.post(
            "/upload_resume",
            files={
                "file": (
                    "resume.txt",
                    b"Alex Johnson\nSkills: Python, SQL\nExperience:\nData Engineer at Example Corp",
                    "text/plain",
                )
            },
        )
        self.assertEqual(upload_response.status_code, 200)
        resume_id = upload_response.json()["resume_id"]

        chat_response = self.client.post(
            "/chat",
            json={"resume_id": resume_id, "question": "What skills are listed?", "top_k": 2},
        )
        self.assertEqual(chat_response.status_code, 200)
        payload = chat_response.json()
        self.assertIn("answer", payload)
        self.assertIn("citations", payload)
        self.assertIsInstance(payload["citations"], list)


if __name__ == "__main__":
    unittest.main()
