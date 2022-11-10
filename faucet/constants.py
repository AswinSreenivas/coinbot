
SUPPORTED_CHAINS = {
    80001: {
        "network_names": {"mumbai", "polygon testnet"},
        "native_token_symbol": "MATIC",
        },
    5: {
        "network_names": {"goerli", "goerli testnet", "eth testnet"},
        "native_token_symbol": "ETH",
        },
}

# Chains that do not use Playground faucet to distribute TRB
NO_FAUCET_TRB = {5}

# Goerli TRB token contract address
TRB_ADDRESS = "0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2"

# Goerli TRB token contract ABI
TRB_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"}
        ],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]
