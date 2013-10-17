from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


### Authentication

class AuthenticationTests(TestCase):
    def test_login(self):

        # create a user

        # log in with that user

        # test authentication
        pass

    def test_logout(self):

        # create a user

        # log in with that user

        # test authentication

        # log out

        # test authentication
        pass

    def test_still_logged_in_after_going_to_another_page(self):

        # create a user

        # log in with that user

        # test authentication

        # go to another view

        # test authentication
        pass

    def test_still_logged_out_after_going_to_another_page(self):
        # create a user

        # log in with that user

        # test authentication

        # go to another view

        # test authentication
        
        # log out

        # test authentication

        # got to another view

        # test authentication
        pass

