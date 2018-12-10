import os
import json
# first need to install the module using `pip install -e .`
from charitybase import CharityBase

DUMMY_API_KEY = 'dummy_api_key'


def test_list(requests_mock):
    with open(os.path.join(os.path.dirname(__file__), 'mocks/list.json')) as a:
        mock_data = json.load(a)
    requests_mock.get(
        'https://charitybase.uk/api/v4.0.0/charities/?fields=income.latest.total&search=homeless&incomeRange=[100000,+1000000]&sort=income.latest.total:desc&limit=10&skip=0&apiKey={}'.format(
            DUMMY_API_KEY),
        json=mock_data
    )
    charityBase = CharityBase(DUMMY_API_KEY)
    res = charityBase.charity.list({
        'fields': ['income.latest.total'],
        'search': 'homeless',
        'incomeRange': [100000, 1000000],
        'sort': 'income.latest.total:desc',
        'limit': 10,
        'skip': 0,
    })

    assert requests_mock.called
    assert len(res.charities)==10
    assert res.count is None


def test_count(requests_mock):
    with open(os.path.join(os.path.dirname(__file__), 'mocks/count.json')) as a:
        mock_data = json.load(a)
    requests_mock.get(
        'https://charitybase.uk/api/v4.0.0/count-charities/?search=homeless&incomeRange=%5B100000%2C+1000000%5D&apiKey={}'.format(
            DUMMY_API_KEY),
        json=mock_data
    )
    charityBase = CharityBase(DUMMY_API_KEY)
    res = charityBase.charity.count({
        'search': 'homeless',
        'incomeRange': [100000, 1000000],
    })

    assert requests_mock.called
    assert res.count == 1566
    assert len(res.charities) == 0
