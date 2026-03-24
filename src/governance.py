from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class Proposal:
    def __init__(self, id: str, title: str, description: str, creator: str,
                 execution_code: str, voting_period_days: int = 7):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.execution_code = execution_code
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(days=voting_period_days)
        self.votes_for: List[str] = []
        self.votes_against: List[str] = []
        self.executed = False
        self.execution_result: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creator': self.creator,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'votes_for': self.votes_for,
            'votes_against': self.votes_against,
            'executed': self.executed,
            'execution_result': self.execution_result
        }

class GovernanceEngine:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.required_quorum = 0.5
        self.required_majority = 0.6

    def create_proposal(self, id: str, title: str, description: str,
                       creator: str, execution_code: str) -> Proposal:
        if id in self.proposals:
            raise ValueError(f'Proposal with ID {id} already exists')
            
        proposal = Proposal(id, title, description, creator, execution_code)
        self.proposals[id] = proposal
        return proposal

    def cast_vote(self, proposal_id: str, voter: str, vote: bool) -> None:
        if proposal_id not in self.proposals:
            raise ValueError(f'Proposal {proposal_id} not found')

        proposal = self.proposals[proposal_id]
        
        if datetime.now() > proposal.expires_at:
            raise ValueError('Voting period has ended')

        # Remove any existing votes by this voter
        if voter in proposal.votes_for:
            proposal.votes_for.remove(voter)
        if voter in proposal.votes_against:
            proposal.votes_against.remove(voter)

        # Add new vote
        if vote:
            proposal.votes_for.append(voter)
        else:
            proposal.votes_against.append(voter)

    def execute_proposal(self, proposal_id: str) -> str:
        if proposal_id not in self.proposals:
            raise ValueError(f'Proposal {proposal_id} not found')

        proposal = self.proposals[proposal_id]
        
        if proposal.executed:
            raise ValueError('Proposal already executed')

        if datetime.now() < proposal.expires_at:
            raise ValueError('Voting period not ended yet')

        total_votes = len(proposal.votes_for) + len(proposal.votes_against)
        if total_votes == 0:
            raise ValueError('No votes cast')

        # Check quorum
        total_eligible_voters = self._get_total_eligible_voters()
        if total_votes / total_eligible_voters < self.required_quorum:
            raise ValueError('Quorum not reached')

        # Check majority
        if len(proposal.votes_for) / total_votes < self.required_majority:
            raise ValueError('Required majority not reached')

        try:
            # Execute the proposal code
            result = eval(proposal.execution_code)
            proposal.executed = True
            proposal.execution_result = str(result)
            return proposal.execution_result
        except Exception as e:
            proposal.execution_result = f'Execution failed: {str(e)}'
            raise

    def _get_total_eligible_voters(self) -> int:
        # TODO: Implement actual eligible voter calculation
        return 100

    def get_proposal_status(self, proposal_id: str) -> Dict:
        if proposal_id not in self.proposals:
            raise ValueError(f'Proposal {proposal_id} not found')
        return self.proposals[proposal_id].to_dict()

    def list_active_proposals(self) -> List[Dict]:
        now = datetime.now()
        return [p.to_dict() for p in self.proposals.values()
                if not p.executed and p.expires_at > now]