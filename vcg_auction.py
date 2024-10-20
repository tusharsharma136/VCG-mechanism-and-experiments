import dataclasses
from typing import List, Tuple, Dict
from enum import Enum
import json

class SpaceType(Enum):
    TOP = 't'
    SIDEBAR = 's'
    BOTH = 'b'

@dataclasses.dataclass
class Bid:
    bidder_id: str
    value: float
    space_type: SpaceType

class VCGAuction:
    def __init__(self, bids: List[Bid]):
        self.bids = bids
        self.sorted_bids = self._sort_bids()
        
    def _sort_bids(self) -> Dict[SpaceType, List[Tuple[str, float]]]:
        #Sort bids by value for each space type.
        sorted_bids = {
            SpaceType.TOP: [],
            SpaceType.SIDEBAR: [],
            SpaceType.BOTH: []
        }
        
        for bid in self.bids:
            sorted_bids[bid.space_type].append((bid.bidder_id, bid.value))
            
        for space_type in sorted_bids:
            sorted_bids[space_type].sort(key=lambda x: x[1], reverse=True)
            
        return sorted_bids

    def find_optimal_allocation(self) -> Tuple[dict, float]:
        #Find the allocation that maximizes social welfare.
        best_value = 0
        best_allocation = {}

        # Try allocating to a single BOTH bidder
        if self.sorted_bids[SpaceType.BOTH]:
            best_value = self.sorted_bids[SpaceType.BOTH][0][1]
            best_allocation = {
                'top': self.sorted_bids[SpaceType.BOTH][0][0],
                'sidebar': self.sorted_bids[SpaceType.BOTH][0][0]
            }

        # Try allocating separately to TOP and SIDEBAR bidders
        top_value = self.sorted_bids[SpaceType.TOP][0][1] if self.sorted_bids[SpaceType.TOP] else 0
        sidebar_value = self.sorted_bids[SpaceType.SIDEBAR][0][1] if self.sorted_bids[SpaceType.SIDEBAR] else 0
        combined_value = top_value + sidebar_value

        if combined_value > best_value:
            best_value = combined_value
            best_allocation = {
                'top': self.sorted_bids[SpaceType.TOP][0][0] if self.sorted_bids[SpaceType.TOP] else None,
                'sidebar': self.sorted_bids[SpaceType.SIDEBAR][0][0] if self.sorted_bids[SpaceType.SIDEBAR] else 0
            }

        return best_allocation, best_value

    def compute_vcg_payments(self) -> Dict[str, float]:
        #Compute VCG payments for each winning bidder.
        allocation, total_value = self.find_optimal_allocation()
        payments = {}

        # For each winner, compute their VCG payment
        for space, winner_id in allocation.items():
            if winner_id is None:
                continue

            # Find the winning bid for this bidder
            winning_bid = next(bid for bid in self.bids if bid.bidder_id == winner_id)

            # Create a new auction without this bidder
            remaining_bids = [bid for bid in self.bids if bid.bidder_id != winner_id]
            alternative_auction = VCGAuction(remaining_bids)
            _, alternative_value = alternative_auction.find_optimal_allocation()

            # VCG payment is the difference in social welfare without this bidder
            payments[winner_id] = alternative_value - (total_value - winning_bid.value)

        return payments

class SecondPriceAuction:
    def __init__(self, bids: List[Bid]):
        self.bids = bids

    def run_auction(self) -> Tuple[str, float]:
        #Run a second-price auction for both slots together.
        # Sort bids by value, ignoring space_type
        sorted_bids = sorted(self.bids, key=lambda x: x.value, reverse=True)
        
        if len(sorted_bids) < 2:
            return sorted_bids[0].bidder_id, 0 if len(sorted_bids) == 1 else None
            
        winner = sorted_bids[0].bidder_id
        payment = sorted_bids[1].value
        
        return winner, payment

def run_experiment(input_file: str):
    #Run experiments comparing VCG and second-price auctions.
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    bids = [Bid(b['bidder_id'], b['value'], SpaceType(b['space_type'])) for b in data['bids']]
    
    # Run VCG auction
    vcg = VCGAuction(bids)
    vcg_allocation, vcg_value = vcg.find_optimal_allocation()
    vcg_payments = vcg.compute_vcg_payments()
    vcg_revenue = sum(vcg_payments.values())
    
    # Run second-price auction
    spa = SecondPriceAuction(bids)
    spa_winner, spa_payment = spa.run_auction()
    
    return {
        'vcg_allocation': vcg_allocation,
        'vcg_payments': vcg_payments,
        'vcg_revenue': vcg_revenue,
        'spa_winner': spa_winner,
        'spa_payment': spa_payment
    }

# Example usage
if __name__ == "__main__":
    # Example input data
    example_data = {
        "bids": [
            {"bidder_id": "A1", "value": 100, "space_type": "b"},
            {"bidder_id": "B1", "value": 60, "space_type": "t"},
            {"bidder_id": "C1", "value": 50, "space_type": "s"},
            {"bidder_id": "D1", "value": 80, "space_type": "b"}
        ]
    }
    
    with open("example_input.json", "w") as f:
        json.dump(example_data, f, indent=2)
    
    results = run_experiment("example_input.json")
    print("Experiment Results:")
    print(json.dumps(results, indent=2))