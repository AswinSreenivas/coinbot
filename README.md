# trb-faucet
mention @trb-faucet on twitter with a network &amp; address, then receive test TRB tokens

# Setup
- install python >= 3.7
- create a virtualenv `python3 -m venv env`
- activate the virtualenv `source env/bin/activate`
- install dependencies `pip install -r requirements.txt`
- create a twitter app and get the keys
- copy and rename `.env.example` to `.env` and fill in the keys

# Run
- `python faucet/main.py`