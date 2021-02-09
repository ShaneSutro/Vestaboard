# Vestaboard

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7d172f1a1ede4c91bb379aa0837a3683)](https://app.codacy.com/gh/SonicRift/Vestaboard?utm_source=github.com&utm_medium=referral&utm_content=SonicRift/Vestaboard&utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.com/SonicRift/Vestaboard.svg?branch=master)](https://travis-ci.com/SonicRift/Vestaboard)
[![PyPI version](https://badge.fury.io/py/Vestaboard.svg)](https://badge.fury.io/py/Vestaboard)
![PyPI - Downloads](https://img.shields.io/pypi/dm/vestaboard)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vestaboard)
***

## GitHub Stats

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/SonicRift/Vestaboard)
![GitHub contributors](https://img.shields.io/github/contributors/SonicRift/Vestaboard)

This is a lightweight and unassuming wrapper for the Vestaboard API.

By [Shane Sutro][] and [contributors](https://github.com/SonicRift/Vestaboard/graphs/contributors)
***
### Official API
You can view more information about Vestaboard's API [here](https://docs.vestaboard.com/).

### Concepts
According to Vestaboard's documentation, software that utilizes the API is considered an `installable`, and as such must be connected to a Vestaboard via an `installation`.

Each Board subscribes to an `installable` via an `installation` and as such is able to recieve a `message`. While I won't get into detail on how these correlate, know that you must first create an `installable` via [Vestaboard's API](https://web.vestaboard.com). You'll need to create an account and register your `installable` to your board.

Once created, you will need to store your API Key and API Secret - you'll need this to communicate with your board. During this process, you will be prompted to select which board you'd like to install this `installable` onto - this is what creates the Subscription ID behind the scenes. Read more below.
***

### Using this package

#### Installation

-   Download and install into your project file
-   Via `pip`:

```pip install vestaboard```

#### Usage

This package will simplify the process of connecting your code to Vestaboard's API.
By default, the module will store your API Key, API Secret, and Subscriber ID in a .txt file in the root folder of the project.
If you do _not_ want to store this, pass `saveCredentials=False` into the creation of an `Installable`. Alternatively, you may skip creating an `Installable` alltogether if you already know your Subscription ID (which you can get from Vestaboards official portal if you'd like to skip this step).

If you do **_not_** know your Subscription ID call `Installable()` with your API Key and API Secret to find and store it:
```python
import vestaboard
#This will print your subscription ID, and store all keys in 'credentials.txt'
installable = vestaboard.Installable('your_api_key', 'your_api_secret')

#Pass in the Installable() instance to a new instance of Board()
vboard = vestaboard.Board(installable)
vboard.post('And just like that, we were off.')
```
![Board with plain text example](../media/basictext.png?raw=true)

If you already have your Subscription ID or you do not want to store it, you can call `Board()` directly and pass your API Key, API Secret and Subscription ID directly. Note that if you choose to not store these credentials, you will need to provide them each time you call a method on a `Board`.
If you do choose to store them, they will be stored in a file called `credentials.txt` in the root directory of your project; remember to add `credentials.txt` to your `.gitignore` to avoid commiting your keys to GitHub. Alternatively, you may create a `config.py` file in your code and store the information there; again, add `config.py` to your `.gitignore`. Never upload API keys or API Secrets to a repository.

#### config.py
```python
api_key='DrBXYxUN40z2dpIogNjO'
api_secret='2Qc8cClVov2TI9eeudVP'
subscription_id='5PmlVd5MnjtMIBYcBUXI'
```
#### vestaboard.py
```python
from vestaboard import Board
import config

vboard = Board(apiKey=config.api_key, apiSecret=config.api_secret, subscriptionId=config.subscription_id)

vboard.post('Love is all you need')
```

***
## Currently Supported
Currently this module supports the following:
-   Creating an Installable object by passing in an API Key and API Secret
    -   This will find and store the Subscription ID for you

-   Creating an instance of Board, either by passing in an  Installable or by passing in an API Key, API Secret _and_ Subscription ID

The board currently has 1 method available, the `.post()` method, which takes in a string and sends it to the board:

```python
import vestaboard

installable = vestaboard.Installable('your_api_key', 'your_api_secret')
vboard = vestaboard.Board(installable)

vboard.post('Everything you can imagine is real.')
```

The `.post()` method supports all letters and symbols that Vestaboard supports, including all letters, numbers, and symbols.
In addition, you may pass in a character code in curly brackets to represent a single character or a color tile. You can view a reference of character and color codes on [Vestaboard's official website by clicking here.](https://docs.vestaboard.com/characters)
Vestaboard's API currently strips leading and trailing spaces from lines - *this includes the `{0}` character (the black tile)*. To precisely place characters, use the `.raw()` method (coming soon).

```python
import vestaboard

installable = vestaboard.Installable('your_api_key', 'your_api_secret')
vboard = vestaboard.Board(installable)

vboard.post('Triage Status\n\n{63}High -3{0}{0}items\n {65}Med -18 items\n{66}Low -88 items')
```
![Board with color tiles example](../media/vbcolors.png?raw=true)

## Upcoming Support
-   Formatting
    -   Want to right justify, left justify, or center? Coming soon!

-   Color codes
    -   Add in color chips alongside letters, numbers, and symbols to create unique combinations

-   Raw Mode
    -   Vestaboard supports a "list of lists" to send a message. This will allow you to precisely place characters exactly where you want them. Upcoming support to pass in a 6 x 22 array to place characters, complete with conversion from letters, numbers, and symbols into the corresponding character.

-   Templates
    -   Choose from a list of templates to send to your board, including calendars, Q&A, trivia, and more

***
## Repository Info
### Needs
-   Additional formatting for 6 x 22 list of lists for sending custom messages
-   Unit and other tests inside the `/test` folder
-   Suggestions or ideas for improvement are always welcome!

Interested in contributing to this project? Send a PR with changes and I'd be happy to review! If you're having trouble with this library, be sure to [open an issue][] so that I can look into the problem. Any details that can be provided alongside the problem would be greatly appreciated.
Thanks!

#### [Shane Sutro][]

You belong here :heart:

[open an issue]: https://github.com/SonicRift/Vestaboard/issues
[shane sutro]: https://github.com/SonicRift