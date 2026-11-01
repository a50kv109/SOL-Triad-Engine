# Pre-SOL Changelog

All notable changes to the `pre_sol` autonomous diagnostics module are documented here.
This project follows a strict empirical verification policy: changes are recorded with their verifying tests and actual test execution outputs.

> **Environment Note:** This workspace operates in a containerized environment without an initialized `.git` repository (`fatal: not a git repository`). No synthetic commit hashes, git branches, or timestamps are fabricated. Version tags represent verified test baselines.

---

## [v0.1-exp] — Round 2: Boundary Cases & Baseline Hardening (2026-11-01)

### Fixed & Enhanced
- **Imperative Mutation Verb Recognition (`pre_sol/config.py`):**
  Added imperative forms (`удали`, `удаляй`, `выполни`, `выполняй`, `сбрось`, `сбрасывай`, `запусти`, `запускай`, `останови`, `останавливай`) to `PROVISIONAL_MUTATION_VERBS`. Enables accurate recognition of both direct commands and negative prohibitions.
- **Sequential Action Clause Splitting (`pre_sol/classifier.py`):**
  Added split patterns for sequential action connectors (`", а затем "`, `", затем "`, `", после чего "`, `", and then "`). Prevents requests from masking subsequent execution commands behind analytical preambles.
- **Quoted Action Masquerade Protection (`pre_sol/classifier.py`):**
  Added `unquoted_text` evaluation in `_classify_type`. If an action command verb occurs outside quoted content (e.g., `'проанализируй "удали", а затем выполни её'`), the clause is unconditionally classified as `ACTION_COMMAND`, triggering `safety_barrier_state = ENGAGED`.
- **Conditional Action Directive Detection (`pre_sol/classifier.py`):**
  Enhanced conditional clause classification: purely hypothetical scenarios (`"Если p < 1 bar, оценить последствия"`) remain `HYPOTHESIS`, while conditional action directives (`"Если p > 10 bar, то выполни сброс"`) trigger `ACTION_COMMAND` and engage the safety barrier.
- **Single-Point Interval Support (`pre_sol/diagnostics.py`):**
  Added `math.isclose` tolerance to boundary checks in `_check_logical_contradictions`. Boundaries that meet exactly at a single point after physical unit conversion (e.g., `p >= 1 bar` and `p <= 100 kPa`, both equal to $100\,000\text{ Pa}$) are recognized as a valid single-point interval $[100000, 100000]\text{ Pa}$ rather than a `LOGICAL_CONTRADICTION`.

### Added Tests
- `tests/test_pre_sol.py`: Added 6 boundary test cases (`test_23` to `test_28`):
  - `test_23_negative_prohibition_not_mutation_command`: Validates `"не удаляй таблицы"` as `CONSTRAINT`, non-mutating, barrier `NOT_APPLICABLE`.
  - `test_24_quoted_command_with_subsequent_action_request`: Validates prompt masquerading detection.
  - `test_25_conditional_scenario_vs_conditional_action_request`: Validates hypothesis vs action in conditional branches.
  - `test_26_unit_conversion_equivalent_bounds_single_point_and_incompatible`: Validates $[1\text{ bar}, 100\text{ kPa}]$ single point pass and incompatible dimension failure.
  - `test_27_circular_reasoning_positive_vs_linear_deduction`: Validates *petitio principii* detection vs linear causal chain.
  - `test_28_exact_raw_query_byte_preservation_utf8`: Validates byte-for-byte SHA256 immutability of multiline Unicode input.

### Verification
- `python3 -m unittest tests/test_pre_sol.py -v`: **28 tests passing (100% OK, ~0.06s)**.

---

## [v0.1-exp] — Round 1: Autonomous Diagnostics Prototype (2026-11-01)

### Added
- **Core Architecture (`pre_sol/`):**
  - `models.py`: Immutable data structures (`Statement`, `PreSolReport`, `DiagnosticIssue`, `UnitInterval`) with strict enums (`StatementType`, `GroundingSource`, `PreSolCode`, `SafetyBarrierState`, `ReadinessStatus`).
  - `classifier.py`: Two-axis classification (`StatementType` x `GroundingSource`) without coupling to external proof systems.
  - `diagnostics.py`: Independent checks for logical contradictions, physical unit consistency, circular reasoning (*petitio principii*), ungrounded fact assertions, and qualitative unmeasurable goals.
  - `engine.py`: Pre-SOL pipeline orchestrator enforcing strict byte-level preservation of `raw_query` in UTF-8.
  - `config.py`: Declarative dictionaries of provisional markers and SI physical unit dimension registry (`pressure`, `time`, `length`, `mass`, `temperature`).

### Added Tests
- `tests/test_pre_sol.py`: Initial test suite of 22 test cases covering:
  - Hypothesis exploration without operator consent barrier.
  - Working assumption tracking.
  - Fact claims without verification.
  - Qualitative goal detection.
  - Dimensional unit verification.
  - Safety barrier guarantees (`ENGAGED` under mutation, never `AUTHORIZED` or `DISENGAGED`).
  - Deserialization tampering rejection (`from_dict` validation).
