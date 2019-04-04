from django.test import TestCase

import datetime

from django.utils import timezone

from .models import Cours


class CoursModelTests(TestCase):

    def test_has_short_description(self):
        """
        test_has_short_description() returns False si le test n'a pas de description
        """
        cours = Cours(short_description="")
        self.assertEqual(len(cours.short_description), 0)
