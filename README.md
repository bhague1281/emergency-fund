# Emergency Fund

Uses [mintapi](https://github.com/mrooney/mintapi), a screen-scraping API for Mint.com, to calculate an emergency fund runway. I.E.: The number of months your emergency fund will last.

## Installation

1.) Ensure you have Python 3 and run the following to install dependencies:

```bash
pip install -r requirements.txt
```

2.) Install `chromedriver`, which will allow mintapi to find your Mint session cookies.

```
brew install chromedriver # or sudo apt-get install chromium-chromedriver on Ubuntu/Debian
```

3.) Set your Mint email and password as environment variables in a file called `.env`.

```bash
MINT_EMAIL=your@emailadress.com
MINT_PASSWORD=yourpassword
```

The script will load this file and the environment variables automatically.

## Usage

Run the following command to run the script:

```
python src/get_emergency_fund.py
```

The script will first log you into Mint. Mintapi tends to fail, when logging in frequently, so if the API is unable to log you in, wait a few minutes and try again.

The script will then ask you to select an account to "source" your emergency fund balance. It will also ask you to input your monthly expenses. The script outputs your currently monthly Mint budget to help aid you in determining your monthly expenses.

Once the script runs once, it'll save your account and expense info in a JSON file for later usage. If you want to change your account/expenses, delete or alter the JSON file.

## Future Fixes and Additions

* Support for multiple "source" accounts.
* Support for changing account/expense info from the command line
* Initiating an account refresh
