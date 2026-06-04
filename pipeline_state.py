from typing import List, Dict
from dataclasses import dataclass, field


# ---------------------------
# Layer 1
# ---------------------------
@dataclass
class IsolatedContent:
    source: str
    content: str
    trust_level: int
    role: str = "data"


# ---------------------------
# Layer 3
# ---------------------------
@dataclass
class HeuristicResult:
    matched_patterns: List[str] = field(default_factory=list)
    score: float = 0.0


# ---------------------------
# Layer 4
# ---------------------------
@dataclass
class SemanticResult:
    risk_score: float = 0.0
    intent_class: str = ""
    latency_ms: float = 0.0


# ---------------------------
# Layer 5
# ---------------------------
@dataclass
class DecisionResult:
    final_score: float = 0.0
    decision: str = ""
    confidence: float = 0.0
    reason: str = ""
    regime: str = ""


# ---------------------------
# Pipeline State
# ---------------------------
@dataclass
class PipelineState:
    input_type: str
    source_tag: str
    raw_input_ref: str

    threshold_regime: str = "balanced"
    current_stage: str = "initialized"
    stage_history: List[str] = field(default_factory=list)

    # Layer 1
    isolated_segments: List[IsolatedContent] = field(default_factory=list)

    # Layer 2
    normalized_text: str = ""
    cleaned_text: str = ""

    # Layer 3
    heuristic: HeuristicResult = field(default_factory=HeuristicResult)

    # Layer 4
    semantic: SemanticResult = field(default_factory=SemanticResult)

    # Layer 5
    decision: DecisionResult = field(default_factory=DecisionResult)

    # Extra metadata (optional)
    metadata: Dict = field(default_factory=dict)

    # Stage control
    def advance_stage(self, stage: str):
        self.stage_history.append(self.current_stage)
        self.current_stage = stage