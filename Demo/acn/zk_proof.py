"""
ZK Proof Module — Schnorr Identification with Fiat-Shamir Heuristic

This implements a mathematically sound (simplified) Schnorr proof over
a prime group. It lets an agent prove "I possess skill X" without
revealing anything about skill X itself.

Math:
  p = 2^127 - 1   (Mersenne prime, public)
  g = 3           (generator, public)

  Private: x = hash(skill_source) % p       ← skill fingerprint, NEVER shared
  Public:  X = g^x mod p                    ← announced to network

  Proof generation:
    k = random nonce
    R = g^k mod p
    c = SHA256(X || R || context) % p       ← Fiat-Shamir challenge
    s = (k + c * x) mod (p - 1)
    → publish (R, s)

  Verification:
    c = SHA256(X || R || context) % p
    check: g^s ≡ R · X^c (mod p)
"""

import hashlib
import secrets
from dataclasses import dataclass

# ── Domain parameters (public) ─────────────────────────────────────────────
P: int = (1 << 127) - 1   # 2^127 - 1, Mersenne prime
G: int = 3                 # primitive root mod P


def _sha256_int(*parts: bytes) -> int:
    """SHA-256 of concatenated parts → integer."""
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return int.from_bytes(h.digest(), "big")


@dataclass(frozen=True)
class SkillKeyPair:
    """
    x  = private key (skill fingerprint) — NEVER leaves the agent process
    X  = public key  — announced to the ACN network
    """
    x: int   # PRIVATE
    X: int   # public

    @classmethod
    def from_skill_source(cls, skill_source: str) -> "SkillKeyPair":
        """Derive key pair deterministically from skill source code."""
        raw = hashlib.sha256(skill_source.encode()).digest()
        x = int.from_bytes(raw, "big") % P
        if x == 0:
            x = 1
        X = pow(G, x, P)
        return cls(x=x, X=X)

    def public_key_hex(self, chars: int = 16) -> str:
        return format(self.X, "x")[:chars]


@dataclass(frozen=True)
class ZKProof:
    """
    Non-interactive Schnorr proof.
    Contains ONLY (R, s, X, capability_tag) — no skill information.
    """
    R: int              # commitment: g^k mod p
    s: int              # response: (k + c*x) mod (p-1)
    X: int              # public key (known to verifier separately, included for clarity)
    capability_tag: str  # human-readable label (e.g. "data_analysis")
    context: str        # task context string used in Fiat-Shamir

    # ── Generation ─────────────────────────────────────────────────────────
    @classmethod
    def generate(cls, keypair: SkillKeyPair,
                 capability_tag: str,
                 task_context: str) -> "ZKProof":
        """
        Called inside the AGENT — x (private key) used here, never transmitted.
        Returns a ZKProof object safe to publish on the network.
        """
        # 1. Random nonce k
        k = secrets.randbelow(P - 2) + 1

        # 2. Commitment R = g^k mod p
        R = pow(G, k, P)

        # 3. Fiat-Shamir challenge (deterministic, non-interactive)
        c = _sha256_int(
            keypair.X.to_bytes(16, "big"),
            R.to_bytes(16, "big"),
            task_context.encode(),
        ) % P

        # 4. Response s = (k + c * x) mod (p - 1)
        s = (k + c * keypair.x) % (P - 1)

        return cls(R=R, s=s, X=keypair.X,
                   capability_tag=capability_tag,
                   context=task_context)

    # ── Verification ───────────────────────────────────────────────────────
    def verify(self) -> bool:
        """
        Called by the ACN NETWORK — uses only public values (R, s, X).
        Returns True iff the prover knows x such that X = g^x mod p.
        """
        # Recompute challenge
        c = _sha256_int(
            self.X.to_bytes(16, "big"),
            self.R.to_bytes(16, "big"),
            self.context.encode(),
        ) % P

        lhs = pow(G, self.s, P)
        rhs = (self.R * pow(self.X, c, P)) % P
        return lhs == rhs

    # ── Display helpers ────────────────────────────────────────────────────
    def r_hex(self, chars: int = 12) -> str:
        return format(self.R, "x")[:chars]

    def s_hex(self, chars: int = 12) -> str:
        return format(self.s, "x")[:chars]

    def x_hex(self, chars: int = 12) -> str:
        return format(self.X, "x")[:chars]
