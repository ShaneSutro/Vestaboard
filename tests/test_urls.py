import vestaboard.vbUrls as vbUrls

def test_post_url_matches():
    assert vbUrls.post == 'https://platform.vestaboard.com/subscriptions/{}/message'

def test_subscription_url_matches():
    assert vbUrls.subscription == 'https://platform.vestaboard.com/subscriptions'
