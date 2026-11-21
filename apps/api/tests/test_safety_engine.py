from app.core.safety_rules import SafetyEngine, SafetySeverity

def test_safe_prompt_passes():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "Can you recommend a 3-day split for strength and hypertrophy?",
        age_group="adult_18_64"
    )
    assert eval_res.severity == SafetySeverity.PASS
    assert eval_res.triggered_rule is None

def test_cardiac_red_flag_triggers_critical_stop():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "I feel sharp chest pain when I do bench press, how do I push through it?",
        age_group="adult_18_64"
    )
    assert eval_res.severity == SafetySeverity.CRITICAL_STOP
    assert eval_res.triggered_rule == "cardiac_warning"
    assert "medical attention" in eval_res.user_message.lower()

def test_syncope_dizziness_triggers_critical_stop():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "I get very dizzy and lightheaded right after deadlifts, should I keep going?",
        age_group="adult_18_64"
    )
    assert eval_res.severity == SafetySeverity.CRITICAL_STOP
    assert eval_res.triggered_rule == "syncope_warning"

def test_acute_injury_triggers_critical_stop():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "I felt a pop in my knee and now my swollen joint hurts when walking",
        age_group="adult_18_64"
    )
    assert eval_res.severity == SafetySeverity.CRITICAL_STOP
    assert eval_res.triggered_rule == "acute_injury"

def test_minor_max_effort_prohibited():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "How can I test my 1RM max effort deadlift today?",
        age_group="minor_under_18"
    )
    assert eval_res.severity == SafetySeverity.CRITICAL_STOP
    assert eval_res.triggered_rule == "minor_max_effort"
    assert "under 18" in eval_res.user_message

def test_minor_caloric_restriction_prohibited():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "What calorie deficit and diet pill should I take to cut weight fast?",
        age_group="minor_under_18"
    )
    assert eval_res.severity == SafetySeverity.CRITICAL_STOP
    assert eval_res.triggered_rule == "minor_caloric_restriction"

def test_senior_high_impact_advisory():
    eval_res = SafetyEngine.evaluate_inbound_prompt(
        "How many high impact plyo depth jumps should I do?",
        age_group="senior_65_plus"
    )
    assert eval_res.severity == SafetySeverity.ADVISORY
    assert eval_res.triggered_rule == "senior_high_impact_warning"
