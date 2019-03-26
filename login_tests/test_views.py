from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from login.views import error_message_incorrect_userpass, error_message_empty_input


class LoginInstanceViewTest(TestCase):
    def setUp(self):
        # Create an existing User
        test_user1 = User.objects.create(username='testuser1')
        test_user1.set_password('HelloWorld123')
        test_user1.save()

    # Test for correct template being used
    def test_uses_correct_template(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'login/not_logged_in.html')

    # Test for Get Request, should return an empty Login form
    def test_new_login(self):
        response = self.client.get(reverse('login:index'))
        self.assertEqual(response.status_code, 200)

    # Test for Post Request
    def test_valid_login(self):
        # sucessful login and redirected to home page
        user_login = self.client.login(username = 'testuser1', password = 'HelloWorld123')
        self.assertTrue(user_login)
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)


    def test_invalid_login(self):
        # upon entering invalid details, user is not redirected
        response = self.client.post(reverse("login:index"), {'username': 'testuser3',
                                                             'password': 'HelloWorld123'})

        # in context object -> act like a dictionary with 'error_message" as a key
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_incorrect_userpass)

    def test_invalid_login_all_empty(self): # this may be covered by testing of Forms
        # upon entering invalid details, user is not redirected
        response = self.client.post(reverse("login:index"), {'username': None,
                                                             'password': None})

        # in context object -> act like a dictionary with 'error_message" as a key
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)



    def test_valid_logout(self):
        # Log user in
        user_login  = self.client.login(username = 'testuser1', password = 'HelloWorld123')
        # Check response Code
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        # Log User out
        user_logout = self.client.logout()
        #Check Response code
        response1 = self.client.get(reverse("login:index"))
        self.assertEqual(response.status_code, 200)
        # Check Error messages
        self.assertTrue('error_message' in response.context)
        self.assertEqual(response.context['error_message'], None)


# following are failed possible methods

    # self.assertTrue(response.status_code, 200)
    # message = QueryDict.get("error_message")
    # self.assertEqual(message,error_message_incorrect_userpass )
    # def test_invalid_login(self):
    #     # account has not been created
    #     user_login = self.client.login(username = 'testuser3', password = 'HelloWorld123')
    #     self.assertFalse(user_login)
    #     response = self.client.get(reverse("login:index"), )
    #     # response = self.client.get(reverse("login:index"))
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertTrue('"error_message":error_message_incorrect_userpass' in response.content)
    #
    #     #self.assertFormError(response, LoginForm(), 'error_message', "Login failure, username or password is incorrect")
    #     # exp_data = {
    #     #     'empty_input_state': True,
    #     #     'error_message': "Login failure, username or password is incorrect"
    #     # }
    #     self.assertEqual("Login failure, username or password is incorrect", 'error_message')

    # def test_invalid_login_all_empty(self):
    #     #username field is blank
    #     user_login = self.client.login(username = None,password = None )
    #     self.assertFalse(user_login)
    #     response = self.client.post(reverse("login:index"), {'error_message': error_message_empty_input})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'form', 'error_message', "Please fill in all input fields" )

    # Test all possible invalid Post Request
    # def test_invalid_login_empty(self):
    #     # submit empty form
    #     # use assertFormError() to verify error messeges
    #     user_login = self.client.login(username = None, password = None)
    #     response = self.client.post(reverse("login:index"))
    #     self.assertEqual(response.status_code, 200)
    #     exp_data = {
    #         'error_message': "Please fill in all input fields"
    #     }
    #     self.assertEqual(exp_data, response.json())
    #
    # def test_invalid_login_invalid_username(self):
    #     # submit empty form
    #     # use assertFormError() to verify error messeges
    #     user_login = self.client.login(username = "hello", password = None)
    #     response = self.client.post(reverse("login:index"))
    #     self.assertEqual(response.status_code, 200)
    #     exp_data = {
    #         'error_message': "Please fill in all input fields"
    #     }
    #     self.assertEqual(exp_data, response.json())


