"""messages._utils tests."""

import builtins

import pytest

import messages._utils

from messages._utils import validate_input
from messages._utils import check_valid
from messages._utils import validate_email
from messages._utils import validate_twilio
from messages._utils import validate_slackwebhook
from messages._utils import validate_slackpost
from messages._utils import validate_telegrambot
from messages._utils import validus
from messages._exceptions import InvalidMessageInputError


##############################################################################
# FIXTURES
##############################################################################

class Email:
    """Basic Email class used for testing."""
    def __init__(self, from_, to , cc, bcc):
        self.from_, self.to, self.cc, self.bcc = from_, to, cc, bcc


class Twilio:
    """Basic Twilio class used for testing."""
    def __init__(self, from_, to , media_url):
        self.from_, self.to, self.media_url = from_, to, media_url


class SlackWebhook:
    """Basic SlackWebhook class used for testing."""
    def __init__(self, webhook_url, attachments):
       self.url = webhook_url
       self.attachments = attachments


class SlackPost:
    """Basic SlackPost class used for testing."""
    def __init__(self, token, channel):
       self.credentials = token
       self.channel = channel


class TelegramBot:
    """Basic TelegramBot class used for testing."""
    def __init__(self, bot_token, chat_id):
       self.bot_token = bot_token
       self.chat_id = chat_id


def func(item):
    """Test func for check_valid."""
    if item == 'BAD':
        return False
    return True


@pytest.fixture()
def get_email():
    """Return a valid Email object for testing."""
    return Email('me@here.com', 'you@there.com',
        ['him@there.com', 'her@there.com'], ['them@there.com'])


@pytest.fixture()
def get_twilio():
    """Return a valid Twilio object for testing."""
    return Twilio('+3215556666', '+3216665555', 'https://url.com')


@pytest.fixture()
def get_slackwebhook():
    """Return a valid SlackWebhook object for testing."""
    return SlackWebhook('https://webhookurl.com', 'https://url.com')


@pytest.fixture()
def get_slackpost():
    """Return a valid SlackWebhook object for testing."""
    return SlackPost('12345abcdef', 'general')


@pytest.fixture()
def get_tgram():
    """Return a valid SlackWebhook object for testing."""
    return TelegramBot('12345:ABCDEFG', '12356')


##############################################################################
# TEST: validate_input
##############################################################################

def test_val_input_NotSupported(get_email, mocker):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object that is
        not supported for input validation
    THEN assert nothing happens
    """
    class Nothing:
        def __init__(self, name):
            self.name = name

    n = Nothing('nothing')
    validate_input(n, 'name')


def test_val_input_Email(get_email, mocker):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object
    THEN assert the proper valid_* functions are called
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_email')
    e = get_email
    for key in e.__dict__.keys():
        validate_input(e, key)
    assert val_mock.call_count == 4


def test_val_input_Twilio(get_twilio, mocker):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object
    THEN assert the proper valid_* functions are called
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_twilio')
    e = get_twilio
    for key in e.__dict__.keys():
        validate_input(e, key)
    assert val_mock.call_count == 3


def test_val_input_SlackWebhook(get_slackwebhook, mocker):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object
    THEN assert the proper valid_* functions are called
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_slackwebhook')
    e = get_slackwebhook
    for key in e.__dict__.keys():
        validate_input(e, key)
    assert val_mock.call_count == 2


def test_val_input_SlackPost(get_slackpost):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object
    THEN assert no errors occur
    """
    e = get_slackpost
    for key in e.__dict__.keys():
        validate_input(e, key)


def test_val_input_SlackPost_raises(get_slackpost):
    """
    GIVEN a message object is instantiated with bad inputs
    WHEN validate_input() is called on a message object
    THEN assert InvalidMessageInputError is raised
    """
    e = get_slackpost
    e.credentials = 12345
    with pytest.raises(InvalidMessageInputError):
        for key in e.__dict__.keys():
            validate_input(e, key)


def test_val_input_TelegramBot(get_tgram, mocker):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object
    THEN assert the proper valid_* functions are called
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_telegrambot')
    e = get_tgram
    for key in e.__dict__.keys():
        validate_input(e, key)
    assert val_mock.call_count == 2


##############################################################################
# TEST: validate_*
##############################################################################

def test_val_email(get_email, mocker):
    """
    GIVEN an Email object
    WHEN validate_email is called
    THEN assert check_valid is called the requisite number of times
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    e = get_email
    e.not_checked = 'this attr should not get checked'
    for key in e.__dict__.keys():
        validate_email(e, key)
    assert check_mock.call_count == 4


def test_val_twilio(get_twilio, mocker):
    """
    GIVEN a Twilio object
    WHEN validate_twilio is called
    THEN assert check_valid is called the requisite number of times
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    e = get_twilio
    e.not_checked = 'this attr should not get checked'
    for key in e.__dict__.keys():
        validate_twilio(e, key)
    assert check_mock.call_count == 3


def test_val_slackwebhook(get_slackwebhook, mocker):
    """
    GIVEN a SlackWebhook object
    WHEN validate_slackwebhook is called
    THEN assert check_valid is called the requisite number of times
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    e = get_slackwebhook
    e.not_checked = 'this attr should not get checked'
    for key in e.__dict__.keys():
        validate_slackwebhook(e, key)
    assert check_mock.call_count == 2


def test_val_slackpost(get_slackpost, mocker):
    """
    GIVEN a SlackPost object
    WHEN validate_slackpost is called
    THEN assert check_valid is called the requisite number of times
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    e = get_slackpost
    e.not_checked = 'this attr should not get checked'
    for key in e.__dict__.keys():
        validate_slackpost(e, key)
    assert check_mock.call_count == 0


def test_val_telegrambot(get_tgram, mocker):
    """
    GIVEN a TelegramBot object
    WHEN validate_telegrambot is called
    THEN assert check_valid is called the requisite number of times
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    e = get_tgram
    e.not_checked = 'this attr should not get checked'
    for key in e.__dict__.keys():
        validate_telegrambot(e, key)
    assert check_mock.call_count == 1


##############################################################################
# TEST: check_valid
##############################################################################

def test_check_valid(get_email):
    """
    GIVEN a valid message object
    WHEN check_valid is called on requisite attributes
    THEN assert normal behavior and no exceptions raised
    """
    e = get_email
    for key in e.__dict__.keys():
        check_valid(e, key, func, 'email')


def test_check_valid_singleton_raisesExc(get_email):
    """
    GIVEN a message object with a single invalid input
    WHEN check_valid is called
    THEN assert InvalidMessageInputError is raised
    """
    e = get_email
    e.from_ = 'BAD'
    with pytest.raises(InvalidMessageInputError):
        for key in e.__dict__.keys():
            check_valid(e, key, func, 'email')


def test_check_valid_list_raisesExc(get_email):
    """
    GIVEN a message object with a list of invalid inputs
    WHEN check_valid is called
    THEN assert InvalidMessageInputError is raised
    """
    e = get_email
    e.to = ['BAD', 'BAD']
    with pytest.raises(InvalidMessageInputError):
        for key in e.__dict__.keys():
            check_valid(e, key, func, 'email')
