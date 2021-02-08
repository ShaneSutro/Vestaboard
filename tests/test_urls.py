import vestaboard
import vestaboard.vbUrls as vbUrls

def test_post():
    assert vbUrls.post == 'https://platform.vestaboard.com/subscriptions/{}/message'

def test_subscription():
    assert vbUrls.subscription == 'https://platform.vestaboard.com/subscriptions'