import unittest

from runtime.channel import normalize_turn_request
from runtime.context_assembly import LatencyTracker
from runtime.orchestrator import (
    AgentOrchestrator,
    ModelInput,
    ModelStep,
    ToolCall,
    VerificationDecision,
)
from runtime.recording import build_recording


class _Context:
    async def resolve(self, request):
        return {"service": "payment-api", "request_id": request.request_id}


class _Surface:
    async def resolve(self, request):
        return {"skills": ["incident-analysis"], "tools": ["metrics.read"]}


class _Model:
    def __init__(self):
        self.calls = 0

    async def complete(self, model_input: ModelInput):
        self.calls += 1
        if self.calls == 1:
            return ModelStep(
                text="I need current latency evidence.",
                tool_calls=(ToolCall("metrics.read", {"service": "payment-api"}),),
                input_tokens=100,
                output_tokens=20,
            )
        self.assert_tool_result(model_input)
        return ModelStep(
            text="Latency is elevated; current evidence does not prove recovery.",
            input_tokens=120,
            output_tokens=24,
        )

    @staticmethod
    def assert_tool_result(model_input):
        assert model_input.tool_results
        assert model_input.tool_results[-1]["tool_name"] == "metrics.read"


class _Tools:
    async def execute(self, call):
        return {"ok": True, "p95_ms": 820}


class _Verifier:
    async def verify(self, *, request, final_text, event_log):
        return VerificationDecision(
            verified=True,
            code="ASSESSMENT_EVIDENCE_BACKED",
            evidence_refs=("metric:payment-api:p95",),
        )


class OrchestratorTests(unittest.IsolatedAsyncioTestCase):
    async def test_turn_converges_model_tool_and_verification_on_one_event_log(self):
        request = normalize_turn_request(
            channel="test",
            principal_id="operator-1",
            session_id="session-1",
            text="Why is payment-api slow?",
        )
        orchestrator = AgentOrchestrator(
            context_resolver=_Context(),
            surface_resolver=_Surface(),
            model=_Model(),
            tool_executor=_Tools(),
            verifier=_Verifier(),
        )

        outcome = await orchestrator.run(request)

        self.assertEqual("verified", outcome.status)
        self.assertEqual(2, outcome.model_turns)
        self.assertEqual(1, outcome.tool_calls)
        event_types = outcome.event_log.replay_types()
        self.assertEqual("run/started", event_types[0])
        self.assertIn("context/snapshot", event_types)
        self.assertEqual(2, event_types.count("model/request"))
        self.assertEqual(2, event_types.count("model/response"))
        self.assertIn("tool/requested", event_types)
        self.assertIn("tool/result", event_types)
        self.assertIn("verification/result", event_types)
        self.assertIn("telemetry/span_started", event_types)
        self.assertIn("telemetry/span_ended", event_types)
        self.assertEqual("run/ended", event_types[-2])

        verification_event = next(
            event for event in outcome.event_log.events if event.type == "verification/result"
        )
        self.assertEqual(("metric:payment-api:p95",), verification_event.evidence_refs)

        latency = LatencyTracker.from_event_log(outcome.event_log).summary()
        self.assertEqual(2, latency["model_turns"])
        self.assertEqual(1, latency["tool_calls"])
        self.assertEqual(220, latency["input_tokens"])
        self.assertEqual(44, latency["output_tokens"])

        recording = build_recording(
            outcome.event_log,
            source="fixture",
            runtime_revision="test",
            agent="infrastructure-engineering",
            model="scripted",
            final_status=outcome.status,
        )
        recorded_verification = next(
            event for event in recording["events"] if event["type"] == "verification/result"
        )
        self.assertEqual(["metric:payment-api:p95"], recorded_verification["evidence_refs"])

    async def test_orchestrator_cannot_execute_change_authority(self):
        class _WriteModel:
            async def complete(self, model_input):
                return ModelStep(
                    text="apply change",
                    tool_calls=(
                        ToolCall(
                            "cloud.change",
                            {"resource": "prod"},
                            execution_authority="change",
                        ),
                    ),
                )

        request = normalize_turn_request(
            channel="test",
            principal_id="operator-1",
            session_id="session-1",
            text="change production",
        )
        orchestrator = AgentOrchestrator(
            context_resolver=_Context(),
            surface_resolver=_Surface(),
            model=_WriteModel(),
            tool_executor=_Tools(),
            verifier=_Verifier(),
        )

        with self.assertRaises(PermissionError):
            await orchestrator.run(request)

    async def test_unverified_outcome_is_not_marked_complete(self):
        class _AnswerModel:
            async def complete(self, model_input):
                return ModelStep(text="The service is recovered.")

        class _RejectVerifier:
            async def verify(self, *, request, final_text, event_log):
                return VerificationDecision(
                    verified=False,
                    code="RECOVERY_NOT_INDEPENDENTLY_VERIFIED",
                )

        request = normalize_turn_request(
            channel="test",
            principal_id="operator-1",
            session_id="session-1",
            text="is it recovered?",
        )
        orchestrator = AgentOrchestrator(
            context_resolver=_Context(),
            surface_resolver=_Surface(),
            model=_AnswerModel(),
            tool_executor=_Tools(),
            verifier=_RejectVerifier(),
        )

        outcome = await orchestrator.run(request)
        self.assertEqual("unverified", outcome.status)
        self.assertFalse(outcome.verification.verified)


if __name__ == "__main__":
    unittest.main()
