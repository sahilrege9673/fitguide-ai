"""
FeedGuide AI — Safety & Clinical Guardrails Engine (v1.0.0)
Deterministic invariant enforcement for user safety and age appropriateness.
"""

import re
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class SafetySeverity(str, Enum):
    PASS = "pass"
    ADVISORY = "advisory"
    CRITICAL_STOP = "critical_stop"

class SafetyEvaluation(BaseModel):
    severity: SafetySeverity
    triggered_rule: Optional[str] = None
    user_message: Optional[str] = None
    suggested_action: Optional[str] = None

class SafetyEngine:
    VERSION = "1.0.0"

    RED_FLAG_PATTERNS = [
        (
            r"\b(chest pain|tightness in chest|angina|heart flutter|crushing chest)\b",
            "cardiac_warning",
            "Chest pain or tightness requires immediate clinical medical attention. Stop all physical activity and contact emergency medical services or a physician."
        ),
        (
            r"\b(dizzy|faint|lightheaded|blackout|syncope|loss of consciousness)\b",
            "syncope_warning",
            "Dizziness or lightheadedness can indicate acute cardiovascular, neurological, or metabolic strain. Stop exercise, sit down safely, hydrate, and seek medical evaluation."
        ),
        (
            r"\b(sharp pain|tore my|torn|snapped|dislocated|swollen joint|popped knee)\b",
            "acute_injury",
            "Acute or sharp pain indicates potential ligament, tendon, or structural injury. Do not train through sharp pain. Rest the joint and consult a licensed physiotherapist or physician."
        ),
        (
            r"\b(eating disorder|anorexi|bulimi|purge|throw up after eating|starve myself|extreme fasting)\b",
            "eating_disorder_alert",
            "Your health and well-being are paramount. If you are struggling with eating habits, body image, or extreme food restriction, please reach out to a certified health professional or support helpline."
        ),
        (
            r"\b(pregnant|pregnancy|trimester)\b",
            "pregnancy_advisory",
            "Exercise during pregnancy requires specialized maternal screening. Please consult your obstetrician or certified prenatal fitness specialist for personalized guidelines."
        ),
        (
            r"\b(lose 10 kg in a week|drop 20 lbs in 5 days|rapid weight loss|starvation diet)\b",
            "unsafe_weight_loss",
            "Rapid extreme weight loss (> 1kg/week) is medically hazardous and leads to metabolic dysfunction and lean tissue wasting. We promote sustainable, healthy progressive habits."
        )
    ]

    MINOR_RESTRICTIONS = [
        (
            r"\b(1rm|one rep max|max effort|heavy deadlift max|max out|max bench)\b",
            "minor_max_effort",
            "For athletes under 18, our training strictly prioritizes movement quality, motor mechanics, and injury prevention over maximum-effort 1RM loading."
        ),
        (
            r"\b(cut weight|calorie deficit|diet pill|fat burner|shred fast|weight cut)\b",
            "minor_caloric_restriction",
            "Nutritional guidance for young athletes focuses exclusively on fueling athletic development, energy balance, and growth. Calorie restriction is strictly prohibited."
        )
    ]

    OLDER_ADULT_RESTRICTIONS = [
        (
            r"\b(box jump|depth jump|high impact plyo|max sprint intervals)\b",
            "senior_high_impact_warning",
            "For older adults, low-impact joint-friendly alternatives, balance drills, and controlled tempo movements are prioritized to protect cartilage and enhance stability."
        )
    ]

    @classmethod
    def evaluate_inbound_prompt(cls, prompt: str, age_group: str = "adult_18_64") -> SafetyEvaluation:
        """
        Evaluates user prompts against clinical and age-specific invariants.
        Returns a SafetyEvaluation object.
        """
        if not prompt or not prompt.strip():
            return SafetyEvaluation(severity=SafetySeverity.PASS)

        prompt_clean = prompt.lower()

        # 1. Critical Red Flags (Applicable to all ages)
        for pattern, rule_id, advice in cls.RED_FLAG_PATTERNS:
            if re.search(pattern, prompt_clean):
                return SafetyEvaluation(
                    severity=SafetySeverity.CRITICAL_STOP,
                    triggered_rule=rule_id,
                    user_message=advice,
                    suggested_action="consult_doctor"
                )

        # 2. Minor-specific rules (< 18)
        if age_group == "minor_under_18":
            for pattern, rule_id, advice in cls.MINOR_RESTRICTIONS:
                if re.search(pattern, prompt_clean):
                    return SafetyEvaluation(
                        severity=SafetySeverity.CRITICAL_STOP,
                        triggered_rule=rule_id,
                        user_message=advice,
                        suggested_action="adjust_goals"
                    )

        # 3. Older adult rules (65+)
        if age_group == "senior_65_plus":
            for pattern, rule_id, advice in cls.OLDER_ADULT_RESTRICTIONS:
                if re.search(pattern, prompt_clean):
                    return SafetyEvaluation(
                        severity=SafetySeverity.ADVISORY,
                        triggered_rule=rule_id,
                        user_message=advice,
                        suggested_action="use_low_impact"
                    )

        return SafetyEvaluation(severity=SafetySeverity.PASS)

    @classmethod
    def validate_plan_safety(cls, exercises: List[Dict[str, Any]], age_group: str) -> List[str]:
        """
        Validates a generated workout plan against age and health constraints.
        Returns a list of violation messages if any exist.
        """
        violations = []
        if age_group == "minor_under_18":
            for ex in exercises:
                # Minors must not have high intensity 1-3 rep max sets
                if ex.get("target_reps") and ex["target_reps"] < 5:
                    violations.append(
                        f"Exercise '{ex.get('name', 'Unknown')}' has unsafe low-rep heavy load ({ex['target_reps']} reps) for minors."
                    )
        return violations
