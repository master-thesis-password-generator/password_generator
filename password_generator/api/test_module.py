import uuid

from flask import Blueprint, request, jsonify

from password_generator.database.database import db_session
from password_generator.database.model.test_data import TestData
from password_generator.scheduler import scheduler

test_module = Blueprint('test_module', __name__)


@test_module.route('/schedule', methods=['POST'])
def add_data_to_test_module():
    """
    Test scheduler.
    Schedules a test for an user.
    ---
    tags:
        - Schedule test
    parameters:
      - name: random_characters_password
        in: body
        type: string
        required: true
        description: Password built using random characters.
      - name: random_words_password
        in: body
        type: string
        required: true
        description: Password built using random words.
      - name: song_password
        in: body
        type: string
        required: true
        description: Password built using song's lyrics.
      - name: email
        in: body
        type: string
        required: true
        description: User email.
    responses:
      500:
        description: Internal Server Error.
      201:
        description: Test scheduled.
        schema:
          type: boolean
    """
    data = request.get_json()

    random_characters_password = data['random_characters_password']
    random_words_password = data['random_words_password']
    song_password = data['song_password']
    email = data['email']

    test_uuid = str(uuid.uuid4())
    __add_test_to_db(test_uuid, random_characters_password, random_words_password, song_password)
    __schedule_test_mails(test_uuid, email)

    return jsonify(True), 201


def __add_test_to_db(test_uuid: str, random_characters_password: str,
                     random_words_password: str, song_password: str):
    db_session.add(TestData(test_uuid, random_characters_password,
                            random_words_password, song_password))
    db_session.commit()


def __schedule_test_mails(test_uuid: str, email: str):
    scheduler.schedule_test(email, test_uuid)