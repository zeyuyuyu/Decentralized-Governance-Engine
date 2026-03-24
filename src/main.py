import os
import json
from typing import List, Dict

class DecentralizedVoting:
    def __init__(self, num_voters: int, proposals: List[str]):
        self.num_voters = num_voters
        self.proposals = proposals
        self.votes: Dict[str, List[int]] = {proposal: [0] * num_voters for proposal in proposals}

    def cast_vote(self, voter_id: int, proposal_index: int):
        for proposal, vote_counts in self.votes.items():
            vote_counts[voter_id] = 0
        self.votes[self.proposals[proposal_index]][voter_id] = 1

    def get_results(self) -> Dict[str, int]:
        return {proposal: sum(vote_counts) for proposal, vote_counts in self.votes.items()}

if __name__ == "__main__":
    num_voters = 100
    proposals = ["Proposal A", "Proposal B", "Proposal C"]
    voting = DecentralizedVoting(num_voters, proposals)

    for voter_id in range(num_voters):
        voting.cast_vote(voter_id, voter_id % len(proposals))

    results = voting.get_results()
    print(json.dumps(results, indent=2))