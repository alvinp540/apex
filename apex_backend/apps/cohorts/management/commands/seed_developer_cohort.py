from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from apps.cohorts.models import Cohort, Assessment, Question


class Command(BaseCommand):
    help = 'Seed a real developer cohort with Google/Amazon-style questions.'

    def handle(self, *args, **options):
        cohort, created = Cohort.objects.get_or_create(
            title='Google & Amazon Style Developer Cohort',
            profession='Backend Developer',
            defaults={
                'description': 'Real-world engineering assessment modeled on Google and Amazon interview patterns for developers.',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=21),
                'max_participants': 120,
                'status': 'open',
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created cohort: %s' % cohort.title))
        else:
            self.stdout.write(self.style.WARNING('Cohort already exists: %s' % cohort.title))

        assessment, assessment_created = Assessment.objects.get_or_create(
            cohort=cohort,
            title='Senior Backend Engineer Assessment',
            defaults={
                'instructions': 'Choose the best answer for each developer interview question.',
                'time_limit_minutes': 20,
                'difficulty': 'hard',
                'passing_score': 75,
                'is_active': True,
            },
        )

        if assessment_created:
            self.stdout.write(self.style.SUCCESS('Created assessment: %s' % assessment.title))
        else:
            self.stdout.write(self.style.WARNING('Assessment already exists: %s' % assessment.title))

        questions = [
            {
                'text': 'You are debugging a production API that intermittently times out. The logs show a database query is often blocked while waiting for a lock. Which change gives the best tradeoff for correctness and throughput?',
                'options': [
                    {'id': 'A', 'text': 'Reduce the connection pool size to force fewer concurrent queries.'},
                    {'id': 'B', 'text': 'Add a retry loop around the query without fixing the lock contention.'},
                    {'id': 'C', 'text': 'Use a proper transaction isolation strategy and shorten lock duration by optimizing the query.'},
                    {'id': 'D', 'text': 'Disable the database index to make reads faster.'},
                ],
                'correct_answer': 'C',
                'points': 2,
            },
            {
                'text': 'A service receives millions of requests per minute and must keep latency low. Which pattern is best for protecting shared resources under load?',
                'options': [
                    {'id': 'A', 'text': 'Allow unlimited parallel writes to shared state without coordination.'},
                    {'id': 'B', 'text': 'Use rate limiting, backpressure, and bounded queues near shared resources.'},
                    {'id': 'C', 'text': 'Move all writes to synchronous blocking I/O on the main thread.'},
                    {'id': 'D', 'text': 'Add global retry loops for every failed request.'},
                ],
                'correct_answer': 'B',
                'points': 2,
            },
            {
                'text': 'In a distributed system, a user action is processed by multiple services, but one service fails after the other services have already succeeded. Which design is most important to reduce operational risk?',
                'options': [
                    {'id': 'A', 'text': 'Use idempotent operations and explicit reconciliation or compensating workflows.'},
                    {'id': 'B', 'text': 'Make every service return the same result regardless of input.'},
                    {'id': 'C', 'text': 'Disable logging to avoid noise during failure.'},
                    {'id': 'D', 'text': 'Retry the same request forever until all services succeed.'},
                ],
                'correct_answer': 'A',
                'points': 2,
            },
            {
                'text': 'You need to design an API endpoint that is safe under high concurrency and avoids race conditions. Which approach is best?',
                'options': [
                    {'id': 'A', 'text': 'Use optimistic locking or atomic updates with unique constraints where needed.'},
                    {'id': 'B', 'text': 'Use one global mutex in application memory for all requests.'},
                    {'id': 'C', 'text': 'Perform all validation in the frontend only.'},
                    {'id': 'D', 'text': 'Ignore duplicates and trust the client to be correct.'},
                ],
                'correct_answer': 'A',
                'points': 2,
            },
            {
                'text': 'A hash map is used to cache expensive computations. The service observes high memory usage but stable hit rates. Which change most directly addresses the likely root cause?',
                'options': [
                    {'id': 'A', 'text': 'Increase the cache TTL and remove stale entries with a size limit or eviction policy.'},
                    {'id': 'B', 'text': 'Store a copy of every value in a second cache for safety.'},
                    {'id': 'C', 'text': 'Disable the cache entirely for all writes.'},
                    {'id': 'D', 'text': 'Add duplicate keys to the cache to improve uniqueness.'},
                ],
                'correct_answer': 'A',
                'points': 2,
            },
            {
                'text': 'During a code review, you see a nested loop over a list of users and a list of orders. The code is O(n²). Which is the best next step?',
                'options': [
                    {'id': 'A', 'text': 'Stop the review and ship the code because it works.'},
                    {'id': 'B', 'text': 'Pre-index or transform data to reduce repeated lookups, then re-evaluate complexity.'},
                    {'id': 'C', 'text': 'Convert everything to recursion to reduce runtime.'},
                    {'id': 'D', 'text': 'Add more threads without fixing the algorithm.'},
                ],
                'correct_answer': 'B',
                'points': 2,
            },
        ]

        for index, question in enumerate(questions, start=1):
            Question.objects.update_or_create(
                assessment=assessment,
                text=question['text'],
                defaults={
                    'question_type': 'mcq',
                    'options': question['options'],
                    'correct_answer': question['correct_answer'],
                    'points': question['points'],
                    'order': index,
                },
            )

        self.stdout.write(self.style.SUCCESS('Seeded %s questions for %s' % (len(questions), assessment.title)))
