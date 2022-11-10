# trb-faucet
mention @trb-faucet on twitter with a network &amp; address, then receive test TRB tokens

*Currently only Polygon Mumbai and Goerli testnets are supported. Check constants.py for specific chain IDs.*

# Setup
- install python >= 3.7
- create a virtualenv `python3 -m venv env`
- activate the virtualenv `source env/bin/activate`
- install dependencies `pip install -r requirements.txt`
- create a twitter app and get the keys
- copy and rename `.env.example` to `.env` and fill in the keys

*The account you're using to fund faucet tweet requests must have testnet MATIC, testnet ETH (Goerli), and the special TRB on Goerli (not generated from Playground contract faucet function.*

Goerli TRB token address: `0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2`

# Run
- `python faucet/main.py`

# Next steps
- [ ] add tests
- [ ] deploy
- [ ] support more testnets
