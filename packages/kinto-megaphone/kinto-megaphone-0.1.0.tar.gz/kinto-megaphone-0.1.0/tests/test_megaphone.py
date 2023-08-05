import mock
import pytest

from kinto_megaphone import megaphone


@mock.patch('kinto_megaphone.megaphone.requests')
def test_megaphone_send_version_does_put(requests):
    m = megaphone.Megaphone('http://example.com/', 'mytoken')
    m.send_version('bid', 'chanid', 'myversion')
    assert requests.put.call_count == 1
    requests.put.assert_called_with('http://example.com/v1/broadcasts/bid/chanid',
                                    auth=megaphone.BearerAuth('mytoken'),
                                    data='myversion')


@mock.patch('kinto_megaphone.megaphone.requests')
def test_megaphone_send_put_failure_raises(requests):
    m = megaphone.Megaphone('http://example.com/', 'mytoken')
    resp = requests.put.return_value = mock.Mock()
    e = resp.raise_for_status.side_effect = AssertionError('hi')
    with pytest.raises(AssertionError) as excinfo:
        m.send_version('bid', 'chanid', 'myversion')
    assert excinfo.value == e


def test_bearer_auth_adds_auth_header():
    r = mock.MagicMock()
    r.headers = {}
    new_r = megaphone.BearerAuth("my-api-key")(r)
    assert new_r == r
    assert new_r.headers["Authorization"] == "Bearer my-api-key"
