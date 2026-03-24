from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

class ProposalStatus(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active' 
    PASSED = 'passed'
    REJECTED = 'rejected'
    EXECUTED = 'executed'

@dataclass
class Vote:
    voter: str
    weight: float
    timestamp: datetime
    support: bool

@dataclass 
class Proposal:
    id: str
    title: str
    description: str
    proposer: str
    status: ProposalStatus
    created_at: datetime
    start_time: datetime
    end_time: datetime
    votes: List[Vote]
    min_quorum: float
    execution_threshold: float

class GovernanceEngine:
    def __init__(self):
        self._proposals: Dict[str, Proposal] = {}
        self._voting_weights: Dict[str, float] = {}
    
    def create_proposal(self, id: str, title: str, description: str, 
                       proposer: str, start_time: datetime, end_time: datetime,
                       min_quorum: float = 0.4, execution_threshold: float = 0.6) -> Proposal:
        if id in self._proposals:
            raise ValueError(f'Proposal with ID {id} already exists')
            
        proposal = Proposal(
            id=id,
            title=title,
            description=description,
            proposer=proposer,
            status=ProposalStatus.DRAFT,
            created_at=datetime.now(),
            start_time=start_time,
            end_time=end_time,
            votes=[],
            min_quorum=min_quorum,
            execution_threshold=execution_threshold
        )
        self._proposals[id] = proposal
        return proposal

    def activate_proposal(self, proposal_id: str) -> None:
        proposal = self._get_proposal(proposal_id)
        if proposal.status != ProposalStatus.DRAFT:
            raise ValueError('Can only activate proposals in DRAFT status')
        proposal.status = ProposalStatus.ACTIVE

    def cast_vote(self, proposal_id: str, voter: str, support: bool) -> None:
        proposal = self._get_proposal(proposal_id)
        
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError('Can only vote on ACTIVE proposals')
            
        if datetime.now() < proposal.start_time:
            raise ValueError('Voting period has not started')
            
        if datetime.now() > proposal.end_time:
            raise ValueError('Voting period has ended')

        # Remove any existing vote from this voter
        proposal.votes = [v for v in proposal.votes if v.voter != voter]
        
        weight = self._voting_weights.get(voter, 1.0)
        vote = Vote(voter=voter, weight=weight, timestamp=datetime.now(), support=support)
        proposal.votes.append(vote)
        
        self._check_proposal_state(proposal)

    def set_voting_weight(self, voter: str, weight: float) -> None:
        if weight < 0:
            raise ValueError('Voting weight cannot be negative')
        self._voting_weights[voter] = weight

    def get_proposal_result(self, proposal_id: str) -> dict:
        proposal = self._get_proposal(proposal_id)
        
        total_weight = sum(self._voting_weights.get(v.voter, 1.0) for v in proposal.votes)
        support_weight = sum(v.weight for v in proposal.votes if v.support)
        
        quorum_reached = total_weight >= proposal.min_quorum
        execution_threshold_met = (support_weight / total_weight) >= proposal.execution_threshold if total_weight > 0 else False
        
        return {
            'total_votes': len(proposal.votes),
            'total_weight': total_weight,
            'support_weight': support_weight,
            'quorum_reached': quorum_reached,
            'execution_threshold_met': execution_threshold_met
        }

    def _get_proposal(self, proposal_id: str) -> Proposal:
        if proposal_id not in self._proposals:
            raise ValueError(f'Proposal {proposal_id} not found')
        return self._proposals[proposal_id]

    def _check_proposal_state(self, proposal: Proposal) -> None:
        if proposal.status != ProposalStatus.ACTIVE:
            return
            
        if datetime.now() <= proposal.end_time:
            return
            
        result = self.get_proposal_result(proposal.id)
        
        if not result['quorum_reached']:
            proposal.status = ProposalStatus.REJECTED
        elif result['execution_threshold_met']:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.REJECTED