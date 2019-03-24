from django.contrib.auth.models import User
from django.test import RequestFactory,TestCase,Client
from ticket_creation.models import Ticket
from django.urls import reverse


class TicketCreationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        testticket = Ticket.objects.create(ticket_id="12345678910", title="Forgot my username",
                                      description="I am very bad at remembering",
                                       user="john")
        testticket.save()



    def create_ticket(self,ticket_id="12345678910", title="Forgot my username",
                                      description="I am very bad at remembering",
                                       user="john"):
        return Ticket.objects.create(ticket_id=ticket_id,title=title,description=description,user=user)

    def test_ticket_creation(self):
        t= self.create_ticket()
        self.assertTrue(isinstance(t,Ticket))
        self.assertEqual(t.title,"Forgot my username")



    def test_bad_tickets(self):
        response = self.client.post('/ticket_creation/100000')
        self.assertEqual(response.status_code,404)
