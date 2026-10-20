"""
APEX Anti-Cheat Engine
Detection: tab switches, speed anomalies, uniform answer patterns, time anomalies
"""

from apps.cohorts.models import AssessmentAttempt

MAX_TAB_SWITCHES = 5
MIN_TIME_PER_QUESTION_SECONDS = 2
SUSPICIOUS_UNIFORM_ANSWER_RATIO = 0.95
MIN_ANSWERS_FOR_UNIFORM_PATTERN = 5


def score_penalty(severity: str) -> int:
    return {'low': 5, 'medium': 10, 'high': 20}.get(severity, 0)


def analyze_attempt(attempt: AssessmentAttempt) -> dict:
    flags = []

    if attempt.tab_switches > MAX_TAB_SWITCHES:
        flags.append(f"Excessive tab switches: {attempt.tab_switches}")

    questions_count = attempt.assessment.questions.count()
    if attempt.submitted_at and attempt.started_at and questions_count > 0:
        duration = (attempt.submitted_at - attempt.started_at).total_seconds()
        avg_per_q = duration / questions_count
        if avg_per_q < MIN_TIME_PER_QUESTION_SECONDS:
            flags.append(f"Abnormally fast: avg {avg_per_q:.1f}s/question")

    if attempt.answers:
        values = list(attempt.answers.values())
        if values:
            most_common = max(set(values), key=values.count)
            ratio = values.count(most_common) / len(values)
            if len(values) >= MIN_ANSWERS_FOR_UNIFORM_PATTERN and ratio >= SUSPICIOUS_UNIFORM_ANSWER_RATIO:
                flags.append(f"Uniform answer pattern: {ratio*100:.0f}% same answer")

    if attempt.time_anomalies > 2:
        flags.append(f"Multiple time anomalies: {attempt.time_anomalies}")

    is_flagged = len(flags) > 0
    severity = 'low'
    if len(flags) >= 3:
        severity = 'high'
    elif len(flags) == 2:
        severity = 'medium'

    reason = ' | '.join(flags) if flags else ''

    if is_flagged:
        from apps.fraud.models import FraudLog
        FraudLog.objects.create(
            user=attempt.user,
            event_type='assessment_cheating_detected',
            severity=severity,
            description=reason,
            ip_address=attempt.ip_address,
            metadata={
                'attempt_id': str(attempt.id),
                'assessment_id': str(attempt.assessment_id),
                'tab_switches': attempt.tab_switches,
                'time_anomalies': attempt.time_anomalies,
            },
        )

    return {
        'flagged': is_flagged,
        'reason': reason,
        'severity': severity,
        'penalty_percent': score_penalty(severity),
    }


def flag_attempt(attempt_id: str):
    attempt = AssessmentAttempt.objects.get(id=attempt_id)
    result = analyze_attempt(attempt)
    if result['flagged']:
        attempt.is_flagged = True
        attempt.flag_reason = result['reason']
        attempt.save(update_fields=['is_flagged', 'flag_reason'])
    return result
