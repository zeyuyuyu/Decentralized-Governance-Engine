import math

class GovernanceEngine:
    def __init__(self, token_supply, minimum_quorum):
        self.token_supply = token_supply
        self.minimum_quorum = minimum_quorum
        self.proposals = []
        self.voters = {}

    def register_voter(self, address, token_balance):
        self.voters[address] = token_balance

    def create_proposal(self, proposal_details):
        self.proposals.append(proposal_details)

    def vote(self, voter_address, proposal_index, vote_weight):
        if voter_address not in self.voters:
            raise ValueError("Voter not registered")
        if vote_weight > self.voters[voter_address]:
            raise ValueError("Insufficient voting power")
        self.proposals[proposal_index]['votes'] += vote_weight
        self.voters[voter_address] -= vote_weight

    def finalize_proposal(self, proposal_index):
        proposal = self.proposals[proposal_index]
        total_votes = sum(p['votes'] for p in self.proposals)
        if total_votes >= self.minimum_quorum and proposal['votes'] > total_votes / 2:
            proposal['status'] = 'passed'
        else:
            proposal['status'] = 'failed'
        return proposal['status']
