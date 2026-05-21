from unittest.mock import patch


def test_rapid_internal_llm_gateway_forwards_caller_token_as_default_header():
    from run_agent import AIAgent

    captured = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    with patch("run_agent.OpenAI", FakeOpenAI):
        AIAgent(
            model="openai/GPT54",
            provider="custom",
            base_url="http://127.0.0.1:3000/api/internal/llm/v1",
            api_key="no-key-required",
            quiet_mode=True,
            skip_context_files=True,
            skip_memory=True,
            request_context={
                "rapid_context": {
                    "internal_caller_token": "caller-token",
                },
            },
        )

    assert captured["default_headers"]["X-RAPID-Internal-Caller-Token"] == "caller-token"

