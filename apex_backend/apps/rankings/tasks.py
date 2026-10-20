from celery import shared_task


@shared_task
def update_user_ranking(user_id: str):
    from apps.accounts.models import User
    from apps.rankings.models import Ranking
    from apps.trust_engine.models import TrustScore
    from apps.profiles.models import Profile

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        trust = TrustScore.objects.get(user=user)
    except Exception:
        return

    # Global rank: position among all professionals by overall_merit_score
    global_rank = (
        TrustScore.objects
        .filter(overall_merit_score__gt=trust.overall_merit_score)
        .count() + 1
    )

    # Profession rank
    profession_rank = (
        TrustScore.objects
        .filter(
            user__profile__profession__iexact=profile.profession,
            overall_merit_score__gt=trust.overall_merit_score,
        )
        .count() + 1
    )

    # Country rank
    country_rank = (
        TrustScore.objects
        .filter(
            user__profile__country__iexact=profile.country,
            overall_merit_score__gt=trust.overall_merit_score,
        )
        .count() + 1
    )

    ranking, _ = Ranking.objects.get_or_create(user=user)
    previous = ranking.global_rank

    ranking.profession = profile.profession
    ranking.global_rank = global_rank
    ranking.profession_rank = profession_rank
    ranking.country_rank = country_rank
    ranking.previous_global_rank = previous
    ranking.rank_movement = (previous or global_rank) - global_rank
    ranking.save()


@shared_task
def recalculate_all_rankings():
    from apps.accounts.models import User
    for user in User.objects.filter(role='professional'):
        update_user_ranking.delay(str(user.id))
