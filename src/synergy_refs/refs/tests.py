import pytest

from django.test import TestCase

from refs.entities import User, UserGraph, RefLevel
from refs.graph_loader import UserGraphLoader


@pytest.fixture
def service():
    return UserGraphLoader()


def test_payments_case_1(service: UserGraphLoader):
    user1 = User(pk="1", ref_level=RefLevel.V2)
    user2 = User(pk="2", ref_level=RefLevel.V1)
    user3 = User(pk="3", ref_level=RefLevel.V1)
    user_graph = UserGraph(root=user1)

    user1.refs.append(user2)
    user2.refs.append(user3)

    service._evaluate_payments(user_graph)

    assert user1.balance == 120 + 40 + 10
    assert user2.balance == 120 + 30 - 40
    assert user3.balance == 120 - 30 - 10


def test_payments_case_2(service: UserGraphLoader):
    user1 = User(pk="1", ref_level=RefLevel.V6)
    user2 = User(pk="2", ref_level=RefLevel.V5)
    user3 = User(pk="3", ref_level=RefLevel.V4)
    user4 = User(pk="4", ref_level=RefLevel.V3)
    user5 = User(pk="5", ref_level=RefLevel.V2)
    user6 = User(pk="6", ref_level=RefLevel.V1)
    user_graph = UserGraph(root=user1)

    user1.refs.append(user2)
    user2.refs.append(user3)
    user3.refs.append(user4)
    user4.refs.append(user5)
    user5.refs.append(user6)

    service._evaluate_payments(user_graph)

    assert user1.balance == 120 + 70 + 5 * 4
    assert user2.balance == 120 + 65 + 5 * 3 - 70
    assert user3.balance == 120 + 60 + 10 * 2 - 65 - 5
    assert user4.balance == 120 + 50 + 10 * 1 - 60 - 5 - 5
    assert user5.balance == 120 + 40 - 50 - 5 - 5 - 10
    assert user6.balance == 120 - 40 - 5 - 5 - 10 - 10


def test_payments_case_3(service: UserGraphLoader):
    user1 = User(pk="1", ref_level=RefLevel.V2)
    user2 = User(pk="2", ref_level=RefLevel.V2)
    user3 = User(pk="3", ref_level=RefLevel.V1)
    user4 = User(pk="4", ref_level=RefLevel.V1)
    user_graph = UserGraph(root=user1)

    user1.refs.append(user2)
    user2.refs.append(user3)
    user3.refs.append(user4)

    service._evaluate_payments(user_graph)

    assert user1.balance == 120 + 40
    assert user2.balance == 120 + 40 + 10 - 40
    assert user3.balance == 120 + 30 - 40
    assert user4.balance == 120 - 30 - 10


def test_payments_case_4(service: UserGraphLoader):
    user1 = User(pk="1", ref_level=RefLevel.V6)
    user2 = User(pk="2", ref_level=RefLevel.V2)
    user3 = User(pk="3", ref_level=RefLevel.V5)
    user4 = User(pk="4", ref_level=RefLevel.V2)
    user5 = User(pk="5", ref_level=RefLevel.V4)
    user6 = User(pk="6", ref_level=RefLevel.V2)
    user7 = User(pk="7", ref_level=RefLevel.V3)
    user8 = User(pk="8", ref_level=RefLevel.V2)
    user9 = User(pk="9", ref_level=RefLevel.V1)
    user10 = User(pk="10", ref_level=RefLevel.V1)
    user_graph = UserGraph(root=user1)

    user1.refs.append(user2)
    user2.refs.append(user3)
    user3.refs.append(user4)
    user4.refs.append(user5)
    user5.refs.append(user6)
    user6.refs.append(user7)
    user7.refs.append(user8)
    user8.refs.append(user9)
    user9.refs.append(user10)

    service._evaluate_payments(user_graph)

    assert user10.balance == 120 - 40 - 10 - 20 - 25 - 30
    assert user10.balance == -5
