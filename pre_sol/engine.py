"""Pre-SOL Engine v0.1: Main entry point for autonomous Task Framing.

Coordinates proposition extraction, dual-axis classification,
epistemic/physical diagnostics, and readiness evaluation.
"""

from typing import Dict, Any, Optional
from .models import TaskFramingReport
from .classifier import StatementClassifier
from .diagnostics import DiagnosticAnalyzer
from .evaluator import PreSolEvaluator


class PreSolEngine:
    """Autonomous Pre-SOL Task Framing Engine."""

    def __init__(
        self,
        classifier: Optional[StatementClassifier] = None,
        analyzer: Optional[DiagnosticAnalyzer] = None,
        evaluator: Optional[PreSolEvaluator] = None,
    ):
        self.classifier = classifier or StatementClassifier()
        self.analyzer = analyzer or DiagnosticAnalyzer()
        self.evaluator = evaluator or PreSolEvaluator()

    def analyze(
        self,
        raw_query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> TaskFramingReport:
        """Analyzes a raw query and generates a structured TaskFramingReport.

        Guarantees:
        - raw_query is retained byte-for-byte unmodified.
        - Safety barrier is never DISENGAGED or AUTHORIZED.
        - Dual-axis classification is applied to all propositions.
        - No mock evidence records are generated.
        """
        # 1. Parse and classify statements
        statements = self.classifier.extract_and_classify(raw_query, context)

        # 2. Run diagnostic checks
        findings = self.analyzer.analyze(statements, raw_query)

        # 3. Evaluate readiness and safety barrier
        (
            analysis_readiness,
            formalization_readiness,
            safety_barrier_state,
            mutation_requested,
            clarification_questions,
            summary_explanation,
            provisional_flags,
        ) = self.evaluator.evaluate(raw_query, statements, findings)

        # 4. Construct and return final report
        return TaskFramingReport(
            raw_query=raw_query,  # Exact byte preservation
            analysis_readiness=analysis_readiness,
            formalization_readiness=formalization_readiness,
            safety_barrier_state=safety_barrier_state,
            mutation_requested=mutation_requested,
            statements=statements,
            findings=findings,
            clarification_questions=clarification_questions,
            summary_explanation=summary_explanation,
            provisional_flags=provisional_flags,
        )
