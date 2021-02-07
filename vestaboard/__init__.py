import requests
import vestaboard.formatter
import vestaboard.characters
import vestaboard.vbUrls

class Board:
  def __init__(self, Installable=False, apiKey=False, apiSecret=False, subscriptionId=False):
    if not Installable:  #check for cred file
      if (not apiKey or not apiSecret or not subscriptionId):
        try:
          creds = self.get_creds()
          if (len(creds) == 3):
            self.apiKey = creds[0]
            self.apiSecret = creds[1]
            self.subscriptionId = creds[2]
          elif (len(creds) < 3 or len(creds) > 3):
            raise ValueError('Credentials have been saved, but one or more are missing. Create a new Installable and pass in saveCredentials=True, or pass in all three parameters when initializing a new Board.')
        except FileNotFoundError:
          raise ValueError('You must create an installable first or save credentials by passing saveCredentials=True into Installable().')
      else:
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.subscriptionId = subscriptionId
    else:
      self.apiKey = Installable.apiKey
      self.apiSecret = Installable.apiSecret
      self.subscriptionId = Installable.subscriptionId

  def get_creds(self):
    with open('./credentials.txt', 'r') as cred:
      creds = cred.read().splitlines()
      return creds

  def post(self, text):
    headers = {
        "X-Vestaboard-Api-Key" : self.apiKey,
        "X-Vestaboard-Api-Secret" : self.apiSecret
    }
    finalText = formatter.standard(text)
    r = requests.post(vbUrls.post.format(self.subscriptionId), headers=headers, json=finalText)
    print(r.status_code)
    print(r.text)

class Installable:
  def __init__(self, apiKey=False, apiSecret=False, getSubscription=True, saveCredentials=True):
    self.apiKey = apiKey
    self.apiSecret = apiSecret
    self.saveCredentials = saveCredentials
    if saveCredentials:
      with open('./credentials.txt', 'w') as cred:
        cred.write(apiKey + '\n')
        cred.write(apiSecret + '\n')
        cred.close()
    if getSubscription:
      self.subscriptionId = self.get_subscriptions(saveCredentials)[0]['_id']

  def get_subscriptions(self, save=True):
    if not self.apiKey or not self.apiSecret:
      raise ValueError('There are no keys set. Call Installable(apiKey= apiSecret=) with your installable keys.')
    headers = {
      'X-Vestaboard-Api-Key': self.apiKey,
      'X-Vestaboard-Api-Secret': self.apiSecret
    }
    response = requests.get(vbUrls.subscription, headers=headers)
    if self.saveCredentials or save and response.status_code == 200:
      with open('./credentials.txt', 'a') as cred:
        cred.write(response.json()['subscriptions'][0]['_id'] + '\n')
        cred.close()

    print(response.json()['subscriptions'])
    return response.json()['subscriptions']

  def get_creds(self):
    with open('./credentials.txt', 'r') as cred:
      print(cred.read().splitlines())
