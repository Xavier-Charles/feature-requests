import os
import unittest
from unittest.mock import patch

import requests
from requests.models import User, Clients, Requests
from requests import app, db


class TestCase(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls)
    #     self.user1 = app.models.User(username='Test User',email='admin@britecore.com')
    #     self.client1 = app.models.Client(name='Piggybank',email='34, Akintola street Yaba')

    # @classmethod
    # def tearDownClass(cls):
    #     self.user1 = app.models.User(username='Test User',email='admin@britecore.com')
    #     self.client1 = app.models.Client(name='Piggybank',email='34, Akintola street Yaba')  

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        print('setup')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  'test.db'
        self.app = app.test_client()

        user1 = User(id=5, username='Mr Test',email='john@britecore.com',\
                password=b'$2b$12$MvZL2ljTdpcd/BV141Uvq.u3HnT1/fOOczQTaJhUpmGt6TmfNqMy2')
        db.create_all()
        db.session.add(user1)
        db.session.commit()


    def tearDown(self):
        print('tear down')
        db.session.remove()
        db.drop_all()

    #  def mocktest(self):
    #      with patch(value.get) as mocked_get:
    #         mocked_get.return_value.ok = True
    #         mocked_get.return_value.text = 'Success'
    #         schedule = self

    #         mocked_get.assert_called_with(url)



    def test_app(self):
        ''' Ensure the app was properly setup '''
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Use this Email to test it out', response.data) #check that the page loads

    def test_redirects(self):
        '''Ensure redirects work'''
        response = self.app.get('/clients', follow_redirects=True)
        self.assertIn(b'Use this Email to test it out', response.data) #check that the page loads

    def test_login(self):
        response = self.app.post('/',data=dict(email=\
        'john@britecore.com', password='password'), follow_redirects=True)

        self.assertIn(b'You are logged in as Mr Test!', response.data)

    def  test_add_client(self):
        response = self.app.post('/', data=dict(email=\
        'john@britecore.com', password='password'), follow_redirects=True)

        response = self.app.post('/clients', data=dict(name=\
        'Paystack', location='3a Ladoke Akintola Rd, Ikeja GRA, Ikeja'), follow_redirects=True)
        self.assertIn(b'Paystack has been added!', response.data)


    def  test_update_client(self):
        response = self.app.post('/', data=dict(email=\
        'john@britecore.com', password='password'), follow_redirects=True)

        response = self.app.post('/clients', data=dict(name=\
        'Paystack', location='3a Ladoke Akintola Rd, Ikeja GRA, Ikeja'), follow_redirects=True)
        self.assertIn(b'Paystack has been added!', response.data)

        response = self.app.post('/update/client/1', data=dict(name=\
        'Paystack.ng'), follow_redirects=True)
        self.assertIn(b'Update this Client', response.data)

        response = self.app.post('/update/client/1', data=dict(name=\
        'Paystack.ng', location='3a Ladoke Akintola Rd, Ikeja GRA, Ikeja'), follow_redirects=True)
        self.assertIn(b'Paystack.ng has been updated!', response.data)


    def  test_add_request(self):
        response = self.app.post('/', data=dict(email=\
        'john@britecore.com', password='password'), follow_redirects=True)

        response = self.app.post('/clients', data=dict(name=\
        'Paystack', location='3a Ladoke Akintola Rd, Ikeja GRA, Ikeja'), follow_redirects=True)
        self.assertIn(b'Paystack has been added!', response.data)       

        response = self.app.post('/clients/requests/1',\
        data=dict(
                title='Test Request',
                description='I know this would work',
                client_priority='A_level',
                target_date='2018-12-1',
                files= None,
                product_area='Policies'
                ), follow_redirects=True)
        self.assertIn(b'Your request has been added', response.data)

    def  test_update_request(self):
        response = self.app.post('/', data=dict(email=\
        'john@britecore.com', password='password'), follow_redirects=True)

        response = self.app.post('/clients', data=dict(name=\
        'Paystack', location='3a Ladoke Akintola Rd, Ikeja GRA, Ikeja'), follow_redirects=True)
        self.assertIn(b'Paystack has been added!', response.data)       

        # response = self.app.post('/update/request/1',\
        # data=dict(
        #         title='Test Request has been Updated',
        #         description='I know this would still work',
        #         client_priority='B_level',
        #         target_date='2018-12-2',
        #         files= None,
        #         product_area='Claims'
        #         ), follow_redirects=True)
        # self.assertIn(b'Your request has been updated!', response.data) ought to return 404

        response = self.app.post('/clients/requests/1',\
        data=dict(
                title='Test Request',
                description='I know this would work',
                client_priority='A_level',
                target_date='2018-12-1',
                files= None,
                product_area='Policies'
                ), follow_redirects=True)
        self.assertIn(b'Your request has been added', response.data)

        response = self.app.post('update/request/1',\
        data=dict(
                title='Test Request has been Updated',
                description='I know this would still work',
                client_priority='B_level',
                target_date='2018-12-2',
                files= None,
                product_area='Claims'
                ), follow_redirects=True)
        self.assertIn(b'Your request has been updated!', response.data)

    
    def  test_delete_request(self):
        response = self.app.post('/', data=dict(email=\
        'john@britecore.com', password='password'), follow_redirects=True)

        response = self.app.post('/clients', data=dict(name=\
        'Paystack', location='3a Ladoke Akintola Rd, Ikeja GRA, Ikeja'), follow_redirects=True)
        self.assertIn(b'Paystack has been added!', response.data)       

        response = self.app.post('/clients/requests/1',\
        data=dict(
                title='Test Request',
                description='I know this would work',
                client_priority='A_level',
                target_date='2018-12-1',
                files= None,
                product_area='Policies'
                ), follow_redirects=True)
        self.assertIn(b'Your request has been added', response.data)

        response = self.app.post('delete/request/1', follow_redirects=True)
        self.assertIn(b'Your request has been deleted!', response.data)



if __name__ =='__main__':
    unittest.main()  


