# =========================================================
# decision.py
# ADVANCED MULTI-LAYER DECISION FUSION ENGINE
# =========================================================

import statistics

# =========================================================
# DECISION FUSION LAYER
# =========================================================

class DecisionEngine:

    def __init__(self):

        # =================================================
        # WEIGHTS
        # =================================================

        self.weights = {

            "semantic": 0.50,

            "heuristic": 0.28,

            "scpi": 0.15,

            "ambiguity": 0.04,

            "sophistication": 0.03
        }

        # =================================================
        # THRESHOLDS
        # =================================================

        self.thresholds = {

            "ALLOW": 20,

            "SANITIZE": 40,

            "BLOCK": 65,

            "ESCALATE": 88
        }

        # =================================================
        # CRITICAL CATEGORIES
        # =================================================

        self.critical_categories = [

            "prompt_extraction",

            "execution_attack",

            "jailbreak",

            "roleplay_attack",

            "unauthorized_access",

            "data_exfiltration",

            "agent_hijacking",

            "memory_poisoning",

            "tool_abuse",

            "indirect_injection"
        ]

    # =====================================================
    # CATEGORY BONUS
    # =====================================================

    def category_risk_bonus(

        self,

        attack_categories
    ):

        bonus = 0

        for category in attack_categories:

            if category in self.critical_categories:

                bonus += 15

            else:

                bonus += 6

        # ---------------------------------------------
        # Multi-category escalation
        # ---------------------------------------------

        if len(attack_categories) >= 3:

            bonus += 10

        if len(attack_categories) >= 5:

            bonus += 18

        return min(bonus, 45)

    # =====================================================
    # AMBIGUITY PENALTY
    # =====================================================

    def ambiguity_penalty(

        self,

        ambiguity_score
    ):

        return ambiguity_score * 18

    # =====================================================
    # CONFIDENCE ADJUSTMENT
    # =====================================================

    def confidence_adjustment(

        self,

        confidence
    ):

        if confidence >= 0.97:

            return -8

        elif confidence >= 0.90:

            return -3

        elif confidence >= 0.80:

            return 0

        elif confidence >= 0.65:

            return 8

        else:

            return 15

    # =====================================================
    # ATTACK CHAIN BONUS
    # =====================================================

    def attack_chain_bonus(

        self,

        attack_categories
    ):

        dangerous_chains = [

            ("prompt_extraction", "data_exfiltration"),

            ("execution_attack", "unauthorized_access"),

            ("jailbreak", "execution_attack"),

            ("tool_abuse", "agent_hijacking"),

            ("memory_poisoning", "instruction_override"),

            ("indirect_injection", "prompt_extraction"),
        ]

        bonus = 0

        for a, b in dangerous_chains:

            if a in attack_categories and b in attack_categories:

                bonus += 12

        return min(bonus, 35)

    # =====================================================
    # UNCERTAINTY ESCALATION
    # =====================================================

    def uncertainty_escalation(

        self,

        confidence,

        ambiguity_score,

        entropy
    ):

        escalation = 0

        # ---------------------------------------------
        # High ambiguity
        # ---------------------------------------------

        if ambiguity_score >= 0.80:

            escalation += 10

        # ---------------------------------------------
        # Low confidence
        # ---------------------------------------------

        if confidence <= 0.60:

            escalation += 15

        # ---------------------------------------------
        # High entropy
        # ---------------------------------------------

        if entropy >= 0.90:

            escalation += 10

        return escalation

    # =====================================================
    # SAFE CONTEXT REDUCTION
    # =====================================================

    def safe_context_adjustment(

        self,

        semantic_result,

        attack_categories
    ):

        reduction = 0

        if semantic_result.get(

            "safe_context_detected",

            False
        ):

            reduction += 12

        # ---------------------------------------------
        # Educational context with low categories
        # ---------------------------------------------

        if len(attack_categories) == 0:

            reduction += 8

        return reduction

    # =====================================================
    # MAIN FUSION
    # =====================================================

    def fuse(

        self,

        semantic_result,

        heuristic_result,

        scpi_result
    ):

        # =================================================
        # SEMANTIC
        # =================================================

        semantic_score = semantic_result.get(

            "semantic_risk_score",

            0
        )

        # =================================================
        # HEURISTIC
        # =================================================

        heuristic_score = heuristic_result.get(

            "heuristic_risk_score",

            0
        )

        # =================================================
        # SCPI
        # =================================================

        scpi_score = scpi_result.get(

            "scpi_score",

            0
        )

        # =================================================
        # STRONG SEMANTIC OVERRIDE
        # =================================================

        if semantic_score >= 92:

            heuristic_score += 45

            scpi_score += 35

        elif semantic_score >= 80:

            heuristic_score += 25

            scpi_score += 20

        elif semantic_score >= 70:

            heuristic_score += 12

            scpi_score += 10

        # =================================================
        # AMBIGUITY
        # =================================================

        ambiguity_score = semantic_result.get(

            "ambiguity_score",

            0
        )

        # =================================================
        # SOPHISTICATION
        # =================================================

        sophistication = semantic_result.get(

            "adversarial_sophistication",

            0
        )

        # =================================================
        # CONFIDENCE
        # =================================================

        confidence = semantic_result.get(

            "confidence",

            0
        )

        # =================================================
        # ENTROPY
        # =================================================

        entropy = semantic_result.get(

            "entropy_uncertainty",

            0
        )

        # =================================================
        # ATTACK CATEGORIES
        # =================================================

        attack_categories = semantic_result.get(

            "attack_categories",

            []
        )

        # =================================================
        # WEIGHTED SCORE
        # =================================================

        weighted_score = (

            semantic_score
            *
            self.weights["semantic"]

            +

            heuristic_score
            *
            self.weights["heuristic"]

            +

            scpi_score
            *
            self.weights["scpi"]

            +

            ambiguity_score
            * 100
            *
            self.weights["ambiguity"]

            +

            sophistication
            *
            self.weights["sophistication"]
        )

        # =================================================
        # CATEGORY BONUS
        # =================================================

        weighted_score += self.category_risk_bonus(

            attack_categories
        )

        # =================================================
        # ATTACK CHAIN BONUS
        # =================================================

        weighted_score += self.attack_chain_bonus(

            attack_categories
        )

        # =================================================
        # CONFIDENCE ADJUSTMENT
        # =================================================

        weighted_score += self.confidence_adjustment(

            confidence
        )

        # =================================================
        # AMBIGUITY PENALTY
        # =================================================

        weighted_score += self.ambiguity_penalty(

            ambiguity_score
        )

        # =================================================
        # UNCERTAINTY ESCALATION
        # =================================================

        weighted_score += self.uncertainty_escalation(

            confidence,

            ambiguity_score,

            entropy
        )

        # =================================================
        # SAFE CONTEXT REDUCTION
        # =================================================

        weighted_score -= self.safe_context_adjustment(

            semantic_result,

            attack_categories
        )

        # =================================================
        # HIGH SOPHISTICATION ESCALATION
        # =================================================

        if sophistication >= 80:

            weighted_score += 10

        elif sophistication >= 60:

            weighted_score += 5

        # =================================================
        # NORMALIZATION
        # =================================================

        final_risk_score = max(

            0,

            min(100, weighted_score)
        )

        # =================================================
        # FINAL DECISION
        # =================================================

        if (

            final_risk_score >= self.thresholds[
                "ESCALATE"
            ]

            or

            (
                confidence < 0.55
                and
                ambiguity_score > 0.85
            )
        ):

            action = "ESCALATE"

            reason = (
                "Critical adversarial behavior detected"
            )

        elif final_risk_score >= self.thresholds[
            "BLOCK"
        ]:

            action = "BLOCK"

            reason = (
                "High confidence malicious prompt detected"
            )

        elif final_risk_score >= self.thresholds[
            "SANITIZE"
        ]:

            action = "SANITIZE"

            reason = (
                "Potentially unsafe prompt detected"
            )

        else:

            action = "ALLOW"

            reason = (
                "Prompt appears safe"
            )

        # =================================================
        # SIGNAL STABILITY
        # =================================================

        signals = [

            semantic_score,

            heuristic_score,

            scpi_score
        ]

        signal_variance = statistics.pvariance(
            signals
        )

        if signal_variance < 50:

            stability = "VERY_STABLE"

        elif signal_variance < 150:

            stability = "STABLE"

        elif signal_variance < 400:

            stability = "MODERATE"

        else:

            stability = "UNSTABLE"

        # =================================================
        # THREAT LEVEL
        # =================================================

        if final_risk_score >= 90:

            threat_level = "CRITICAL"

        elif final_risk_score >= 75:

            threat_level = "HIGH"

        elif final_risk_score >= 45:

            threat_level = "MEDIUM"

        else:

            threat_level = "LOW"

        # =================================================
        # EXPLAINABILITY
        # =================================================

        explanation = {

            "semantic_contribution": round(

                semantic_score
                *
                self.weights["semantic"],

                2
            ),

            "heuristic_contribution": round(

                heuristic_score
                *
                self.weights["heuristic"],

                2
            ),

            "scpi_contribution": round(

                scpi_score
                *
                self.weights["scpi"],

                2
            ),

            "ambiguity_penalty": round(

                self.ambiguity_penalty(
                    ambiguity_score
                ),

                2
            ),

            "category_bonus": round(

                self.category_risk_bonus(
                    attack_categories
                ),

                2
            ),

            "attack_chain_bonus": round(

                self.attack_chain_bonus(
                    attack_categories
                ),

                2
            ),

            "uncertainty_escalation": round(

                self.uncertainty_escalation(

                    confidence,

                    ambiguity_score,

                    entropy
                ),

                2
            ),
        }

        # =================================================
        # RETURN
        # =================================================

        return {

            "final_action": action,

            "reason": reason,

            "final_risk_score": round(
                final_risk_score,
                2
            ),

            "threat_level":
                threat_level,

            "system_stability":
                stability,

            "signal_variance": round(
                signal_variance,
                2
            ),

            "attack_categories":
                attack_categories,

            "confidence":
                confidence,

            "severity":
                semantic_result.get(
                    "severity",
                    "UNKNOWN"
                ),

            "entropy":
                entropy,

            "ambiguity_score":
                ambiguity_score,

            "explanation":
                explanation,

            "semantic_result":
                semantic_result,

            "heuristic_result":
                heuristic_result,

            "scpi_result":
                scpi_result
        }