from cectf_server import challenges

from helpers import setup_test


def _get_headers(client):
    return {}  # {'Authorization': 'JWT ' + _get_token(client)}


@setup_test('/api/ctf/challenges', user_id=1)
def test_get_challenges(app, client):
    response = challenges.get_challenges()
    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'title': 'The First Challenge',
            'category': 'crypto',
            'body': 'Just think really hard!',
            'hinted': False,
            'solved': False
        },
        {
            'id': 2,
            'title': 'The Second Challenge',
            'category': 'reversing',
            'body': 'Just think really harder!',
            'hinted': False,
            'solved': False
        }
    ]


@setup_test('/api/ctf/challenges/1', user_id=1)
def test_get_challenge(app, client):
    response = challenges.submit_flag(1)
    assert response.status_code == 200
    assert response.json == {
        'id': 1,
        'title': 'The First Challenge',
        'category': 'crypto',
        'body': 'Just think really hard!',
        'hinted': False,
        'solved': False
    }


@setup_test('/api/challenges/1',
            method='POST',
            json={'flag': 'CTF{l0l}'},
            user_id=1)
def test_submit_correct_flag(app, client):
    response = challenges.submit_flag(1)
    assert response.status_code == 200
    assert response.json == {
        'status': challenges.CORRECT,
        'challenge': {
            'id': 1,
            'title': 'The First Challenge',
            'category': 'crypto',
            'body': 'Just think really hard!',
            'hinted': False,
            'solved': True,
            'solution': 'CTF{l0l}'
        }
    }


@setup_test('/api/challenges/1',
            method='POST',
            json={'flag': 'CTF{l0l_n0p3}'},
            user_id=1)
def test_submit_incorrect_flag(app, client):
    response = challenges.submit_flag(1)
    assert response.status_code == 200
    assert response.json == {'status': challenges.INCORRECT}


@setup_test('/api/challenges/1',
            method='POST',
            json={'flag': 'CTF{l0l}'},
            user_id=1)
def test_submit_twice(app, client):
    challenges.submit_flag(1)
    response = challenges.submit_flag(1)
    assert response.status_code == 200
    assert response.json == {'status': challenges.ALREADY_SOLVED}
