from django.db.models import Count, Q

from .models import Cohort, PSPRegistration


def target_capacity_for_traffic(tier):
    traffic = PSPRegistration.objects.filter(
        psp_tier=tier,
        status__in=('pending', 'confirmed', 'active'),
    ).count()
    if traffic >= 100:
        return 100
    if traffic >= 50:
        return 50
    return 20


def choose_cohort_for_tier(tier):
    target = target_capacity_for_traffic(tier)
    cohorts = Cohort.objects.filter(
        payment_tier=tier,
        status='open',
        max_participants__gte=target,
    ).annotate(
        placement_count=Count(
            'psp_registrations',
            filter=Q(psp_registrations__status__in=('pending', 'confirmed', 'active')),
        ),
    ).filter(placement_count__lt=target).order_by('max_participants', 'created_at')
    return cohorts.first()
