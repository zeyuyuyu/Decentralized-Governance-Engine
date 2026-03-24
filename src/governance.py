import os
import json
from web3 import Web3

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-PROJECT-ID'))

# Set up contract ABI and address
with open('./abi/governance.json') as f:
    abi = json.load(f)
contract_address = '0x1234567890123456789012345678901234567890'
contract = w3.eth.contract(address=contract_address, abi=abi)

# Define proposal struct
class Proposal:
    def __init__(self, id, title, description, creator, start_block, end_block, votes_for, votes_against):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.start_block = start_block
        self.end_block = end_block
        self.votes_for = votes_for
        self.votes_against = votes_against

# Create new proposal
def create_proposal(title, description, creator):
    current_block = w3.eth.get_block_number()
    proposal_id = contract.functions.createProposal(title, description, creator, current_block, current_block + 10000).call()
    return Proposal(proposal_id, title, description, creator, current_block, current_block + 10000, 0, 0)

# Vote on proposal
def vote_on_proposal(proposal_id, voter, vote):
    tx = contract.functions.voteOnProposal(proposal_id, vote).transact({'from': voter})
    w3.eth.wait_for_transaction_receipt(tx)
    proposal = get_proposal(proposal_id)
    if vote:
        proposal.votes_for += 1
    else:
        proposal.votes_against += 1
    return proposal

# Get proposal details
def get_proposal(proposal_id):
    proposal_data = contract.functions.getProposal(proposal_id).call()
    return Proposal(proposal_id, *proposal_data)

# Example usage
proposal = create_proposal('Increase token supply', 'Increase the total token supply by 10%', '0x0123456789012345678901234567890123456789')
print(f'Proposal created: {proposal.title}')

vote_on_proposal(proposal.id, '0x9876543210987654321098765432109876543210', True)
vote_on_proposal(proposal.id, '0x0123456789012345678901234567890123456789', False)

updated_proposal = get_proposal(proposal.id)
print(f'Proposal details: {updated_proposal.votes_for} votes for, {updated_proposal.votes_against} votes against')