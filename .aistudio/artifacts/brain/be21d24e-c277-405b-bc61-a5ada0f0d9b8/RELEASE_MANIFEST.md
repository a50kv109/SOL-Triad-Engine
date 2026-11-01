# SOL-Triad-Engine v0.4.0 & Pre-SOL v0.1-exp — Distribution Manifest

**Environment:** Linux x86_64, Python 3.10+, Vite/React SPA  
**Baseline Test Status:** 52/52 passed (100% OK, 0.078s)  
- `tests/test_pre_sol.py`: 32/32 tests passed (boundary, syntax, invariant isolation)
- `tests/test_o7_triad_semantics.py`: 9/9 tests passed (O7 primitive mapping & structural gap validation)
- `tests/test_hash_chain.py`: 11/11 tests passed (tamper-evident hash chain & PreSolTriadBridge)

---

## Key Modules

1. **`sol_triad/` (Core Kernel & Adapter):**
   - Deterministic verification engine $\langle S, C, D \rangle$, pairwise projectors ($P_{SC}, P_{SD}, P_{CD}$), unit registry, and `SolTriadJsonAdapter`.
2. **`sol_triad/o7_mapping.py`:**
   - Formal O7 primitive mapping (`O7Source`, `O7State`, `O7Flow`, `O7Constraint`, `O7Compare`, `O7Dissipate`, `O7Capability`, `O7Bundle`) with explicit unrepresented field audits.
3. **`pre_sol/hash_chain.py` (Finding 4 — `belov-fiber-sdk` pattern):**
   - Tamper-evident `DiagnosticHashChain` ensuring raw query, extracted statements, findings, and barrier states are immutably sealed across TSK diagnostic stages.
4. **`pre_sol/adapter_bridge.py`:**
   - Fail-closed bridge enforcing Anti-Self-Minting, safety barrier locking, and cryptographic evidence binding (`payload_hash == audit_trail_hash`) for `SolTriadJsonAdapter`.
5. **`pre_sol/` (Autonomous Diagnostics):**
   - Dual-axis proposition classifier, interval contradiction and *petitio principii* analyzer, and readiness evaluator.
