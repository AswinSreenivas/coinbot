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

# Run
- `python faucet/main.py`



# TODO
- [ ] need function for checking if funding address has enough funds to send to given address
- [ ] send goerli test eth using transfer, not faucet