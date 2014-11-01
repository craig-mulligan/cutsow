import datetime
from django.utils import timezone
from django.test import TestCase

from polls.models import Poll


class ChoiceValueTests(TestCase):

    def choice_has_zero_value(self):
        """
        All choices should have a positive or negative value """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)
