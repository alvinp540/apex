"""
APEX Router Engine
Routing Score:
  router_score = 0.40*merit + 0.30*profession_match + 0.20*location_match + 0.10*availability
Top 5 professionals receive Opportunity records.
"""

from django.utils import timezone
from datetime import timedelta

TOP_N = 5
OPPORTUNITY_TTL_HOURS = 48


def route_job(job_id: str) -> int:
    from apps.vendor.models import VendorJob
    from apps.trust_engine.models import TrustScore
    from apps.profiles.models import Profile
    from apps.fraud.models import Opportunity
    from apps.notifications.utils import send_notification

    job = VendorJob.objects.select_related('vendor__profile').get(id=job_id)

    candidate_profiles = Profile.objects.filter(
        profession__iexact=job.profession_required,
        availability='available',
    ).select_related('user', 'user__trust_score')

    results = []
    for profile in candidate_profiles:
        user = profile.user
        try:
            trust = user.trust_score
        except TrustScore.DoesNotExist:
            continue
        if trust.overall_merit_score < job.min_trust_score:
            continue
        score = _compute_router_score(job, profile, trust)
        results.append((user, score))

    results.sort(key=lambda x: x[1], reverse=True)
    top_candidates = results[:TOP_N]

    expires_at = timezone.now() + timedelta(hours=OPPORTUNITY_TTL_HOURS)

    for user, router_score in top_candidates:
        Opportunity.objects.update_or_create(
            job=job,
            professional=user,
            defaults={
                'router_score': router_score,
                'status': 'active',
                'expires_at': expires_at,
            },
        )
        vendor_name = getattr(getattr(job.vendor, 'profile', None), 'full_name', 'A vendor')
        send_notification(
            user=user,
            notification_type='opportunity',
            title=f'New Opportunity: {job.title}',
            message=(
                f'{vendor_name} is looking for a {job.profession_required}. '
                f'Budget: {job.currency} {job.budget_min}–{job.budget_max}.'
            ),
            action_url=f'/opportunities/{job.id}/',
            metadata={'job_id': str(job.id), 'router_score': router_score},
        )

    return len(top_candidates)


def _compute_router_score(job, profile, trust) -> float:
    merit_component = (trust.overall_merit_score / 100.0) * 40

    profession_match = 30 if profile.profession.lower() == job.profession_required.lower() else 15

    if job.location_preference:
        if job.location_preference.lower() in (profile.location or '').lower():
            location_component = 20
        elif job.location_preference.lower() in (profile.country or '').lower():
            location_component = 10
        else:
            location_component = 0
    else:
        location_component = 20

    availability_bonus = 10 if profile.availability == 'available' else 0

    return round(merit_component + profession_match + location_component + availability_bonus, 2)
