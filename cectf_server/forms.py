from flask_security.forms import LoginForm, ConfirmRegisterForm, StringField, Required, HiddenField
from flask import session, request
from .database import user_datastore
from .models import Challenge, Solve


class ExtendedLoginForm(LoginForm):

    username = StringField('Username', [Required()])

    def validate(self):
        self.user = user_datastore.find_user(username=self.username.data)
        self.email.data = self.user.email
        return super().validate()


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    username = StringField('Username', [Required()])
    roles = HiddenField('roles')
    solves = HiddenField('solves')

    def validate(self):
        self.roles.data = ['contestant']
        self.solves.data = [Solve(
            hinted=False,
            solved=False,
            challenge=challenge)
            for challenge in Challenge.query.all()]
        print('FORMO', self.solves.data)
        return super().validate()


'''
    def to_dict(self):
        _dict = super().to_dict()
        _dict['username'] = self.username.data
        return _dict
'''