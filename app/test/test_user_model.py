import unittest

import datetime

from app.main import db
from app.main.model.organization import Organization
from app.test.base import BaseTestCase


class TestOrganizationModel(BaseTestCase):

    def test_encode_auth_token(self):
        organization = Organization(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.now()
        )
        db.session.add(organization)
        db.session.commit()
        auth_token = Organization.encode_auth_token(organization.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        organization = Organization(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.now()
        )
        db.session.add(organization)
        db.session.commit()
        auth_token = Organization.encode_auth_token(organization.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(Organization.decode_auth_token(auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()

