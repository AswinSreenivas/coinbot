# trb-faucet
mention @trb-faucet on twitter with a network &amp; address, then receive test TRB tokens

*Currently only Polygon Mumbai and Goerli testnets are supported. Check constants.py for specific chain IDs.*

# Setup
- install python >= 3.7
- create a virtualenv `python3 -m venv env`
- activate the virtualenv `source env/bin/activate`
- install dependencies `pip install -r requirements.txt`
- create an account on [twilio](https://www.twilio.com/docs/sms/quickstart/python)
- create a twitter app and get the keys
- copy and rename `.env.example` to `.env` and fill in the twitter app keys
- in your `.env` file, list phone numbers you want alerts sent to (`ALERT_RECIPIENTS`).
- from [twilio](https://www.twilio.com/docs/sms/quickstart/python), specify the phone number that will send messages (`TWILIO_FROM`), your `TWILIO_ACCOUNT_SID`, and access key (`TWILIO_AUTH_TOKEN`)

*The account you're using to fund faucet tweet requests must have testnet MATIC, testnet ETH (Goerli), and the special TRB on Goerli (not generated from Playground contract faucet function.*

Goerli TRB token address: `0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2`

# Run
- `python faucet/main.py`

# Next steps
- [ ] add tests
- [ ] deploy
- [ ] support more testnets
