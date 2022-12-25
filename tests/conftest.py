import datetime

import pytest
from jose import jwt
from starlette.testclient import TestClient

import tech_test
from tech_test.core.config import get_redis


@pytest.fixture
def r():
    redis = get_redis().__next__()
    return redis


@pytest.fixture(scope="session")
def tc():
    test_client = TestClient(tech_test.webapp)
    yield test_client


@pytest.fixture
def jwt_data():
    data = dict(pl={
        "sub": "1234567890",
        "user_id": 1001,
        "email": "beydaghi.alireza@gmail.com",
        "phone_number": "09353594889",
        "kyc_level": 1,
        "iat": datetime.datetime.now(),
        "exp": int((datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp())
    },
        priv="""-----BEGIN EC PRIVATE KEY-----
MHcCAQEEICRNeOpxVw2nvAiQ/Alc1ErILm/VvS7iAcS5+ePLJD4joAoGCCqGSM49
AwEHoUQDQgAEcaBco5sZkAFkh/k8zPbybZTwdqE9sJP6Q5l7ofYBgbFuHOiarB4o
HuFLvmNxAq4nYelRXS0WM8H6qSVdPuFhzg==
-----END EC PRIVATE KEY-----""",
        pub_key="""-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEcaBco5sZkAFkh/k8zPbybZTwdqE9
sJP6Q5l7ofYBgbFuHOiarB4oHuFLvmNxAq4nYelRXS0WM8H6qSVdPuFhzg==
-----END PUBLIC KEY-----"""

    )
    data['token'] = jwt.encode(data['pl'], data['priv'], 'ES256')
    return data
