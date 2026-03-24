import os
import json
from web3 import Web3

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

# Contract ABI and address
abi = json.load(open('abi.json'))
contract_address = '0x123456789abcdef0123456789abcdef01234567'
contract = w3.eth.contract(address=contract_address, abi=abi)

# Proposal struct
class Proposal:
    def __init__(self, id, title, description, author, start_block, end_block, vote_weight):
        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.start_block = start_block
        self.end_block = end_block
        self.vote_weight = vote_weight

# Create a new proposal
def create_proposal(title, description, author, start_block, end_block, vote_weight):
    tx = contract.functions.createProposal(
        title, description, author, start_block, end_block, vote_weight
    ).transact({'from': w3.eth.accounts[0]})
    return tx.wait(1)

# Vote on a proposal
def vote_on_proposal(proposal_id, vote_weight):
    tx = contract.functions.voteOnProposal(proposal_id, vote_weight).transact({'from': w3.eth.accounts[0]})
    return tx.wait(1)

# Finalize a proposal
def finalize_proposal(proposal_id):
    tx = contract.functions.finalizeProposal(proposal_id).transact({'from': w3.eth.accounts[0]})
    return tx.wait(1)
