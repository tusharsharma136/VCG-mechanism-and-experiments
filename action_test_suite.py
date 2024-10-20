import json
from dataclasses import asdict
from vcg_auction import VCGAuction, SecondPriceAuction, Bid, SpaceType
from typing import List, Dict, Tuple
import random


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SpaceType):
            return obj.value
        return super().default(obj)


class AuctionTestSuite:
    def __init__(self):
        self.test_results = []
    
    def run_single_test(self, bids: List[Bid], test_name: str) -> Dict:
        
        vcg = VCGAuction(bids)
        spa = SecondPriceAuction(bids)
        
        # VCG Results
        vcg_allocation, vcg_value = vcg.find_optimal_allocation()
        vcg_payments = vcg.compute_vcg_payments()
        vcg_revenue = sum(vcg_payments.values())
        
        # Second Price Auction Results
        spa_winner, spa_payment = spa.run_auction()
        
        result = {
            'test_name': test_name,
            'bids': [self.serialize_bid(bid) for bid in bids],
            'vcg_results': {
                'allocation': vcg_allocation,
                'payments': vcg_payments,
                'total_revenue': vcg_revenue
            },
            'spa_results': {
                'winner': spa_winner,
                'payment': spa_payment
            },
            'revenue_ratio': spa_payment / vcg_revenue if vcg_revenue > 0 else float('inf')
        }
        
        self.test_results.append(result)
        return result


    def serialize_bid(self, bid: Bid) -> Dict:
        return {
            'bidder_id': bid.bidder_id,
            'value': bid.value,
            'space_type': bid.space_type.value
        }


    def test_sybil_attack(self) -> Dict:
        #Test case demonstrating Sybil attack vulnerability.
        # Original scenario: truthful bidding
        original_bids = [
            Bid("A1", 100, SpaceType.BOTH),
            Bid("B1", 80, SpaceType.TOP),
            Bid("C1", 70, SpaceType.SIDEBAR)
        ]
        
        # Sybil attack scenario: A1 splits into two identities
        sybil_bids = [
            Bid("A1", 60, SpaceType.TOP),
            Bid("A2", 50, SpaceType.SIDEBAR),  # Second identity
            Bid("B1", 80, SpaceType.TOP),
            Bid("C1", 70, SpaceType.SIDEBAR)
        ]
        
        return {
            'original': self.run_single_test(original_bids, "Sybil Attack - Original"),
            'sybil': self.run_single_test(sybil_bids, "Sybil Attack - Split Identity")
        }


    def test_revenue_comparison(self) -> List[Dict]:
       #Test cases for comparing VCG and second-price auction revenues.
        test_cases = [
            # Case 1: Both slots highly valued
            {
                'name': "High Value Both Slots",
                'bids': [
                    Bid("A1", 200, SpaceType.BOTH),
                    Bid("B1", 180, SpaceType.BOTH),
                    Bid("C1", 100, SpaceType.TOP),
                    Bid("D1", 90, SpaceType.SIDEBAR)
                ]
            },
            # Case 2: Split allocation optimal
            {
                'name': "Split Allocation Optimal",
                'bids': [
                    Bid("A1", 120, SpaceType.TOP),
                    Bid("B1", 110, SpaceType.SIDEBAR),
                    Bid("C1", 150, SpaceType.BOTH),
                    Bid("D1", 140, SpaceType.BOTH)
                ]
            },
            # Case 3: Mixed preferences
            {
                'name': "Mixed Preferences",
                'bids': [
                    Bid("A1", 90, SpaceType.TOP),
                    Bid("B1", 85, SpaceType.SIDEBAR),
                    Bid("C1", 160, SpaceType.BOTH),
                    Bid("D1", 80, SpaceType.TOP),
                    Bid("E1", 75, SpaceType.SIDEBAR)
                ]
            }
        ]
        
        results = []
        for case in test_cases:
            results.append(self.run_single_test(case['bids'], case['name']))
        return results


    def test_truthful_bidding(self) -> Dict:
        #Test case demonstrating truthful bidding is optimal in second-price auction.
        true_value = 150
        test_bids = [
            # True value bidding
            [
                Bid("A1", true_value, SpaceType.BOTH),
                Bid("B1", 100, SpaceType.BOTH),
                Bid("C1", 80, SpaceType.TOP)
            ],
            # Overbidding
            [
                Bid("A1", true_value * 1.2, SpaceType.BOTH),
                Bid("B1", 100, SpaceType.BOTH),
                Bid("C1", 80, SpaceType.TOP)
            ],
            # Underbidding
            [
                Bid("A1", true_value * 0.8, SpaceType.BOTH),
                Bid("B1", 100, SpaceType.BOTH),
                Bid("C1", 80, SpaceType.TOP)
            ]
        ]
        
        results = {
            'true_value': true_value,
            'truthful': self.run_single_test(test_bids[0], "Truthful Bidding"),
            'overbid': self.run_single_test(test_bids[1], "Overbidding"),
            'underbid': self.run_single_test(test_bids[2], "Underbidding")
        }
        return results


    def run_all_tests(self) -> Dict:
        #Run all test cases and generate comprehensive report.
        return {
            'sybil_attack': self.test_sybil_attack(),
            'revenue_comparison': self.test_revenue_comparison(),
            'truthful_bidding': self.test_truthful_bidding()
        }


def save_results(results: Dict, filename: str):
    #Save test results to a JSON file.
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, cls=EnhancedJSONEncoder)


def analyze_results(results: Dict):
    #Analyze and print key findings from the test results.
    print("\nKey Findings:")
    
    # Analyze Sybil attack
    sybil = results['sybil_attack']
    print("\n1. Sybil Attack Analysis:")
    print(f"Original VCG Revenue: {sybil['original']['vcg_results']['total_revenue']}")
    print(f"Sybil Attack VCG Revenue: {sybil['sybil']['vcg_results']['total_revenue']}")
    
    # Analyze revenue ratios
    revenue_tests = results['revenue_comparison']
    ratios = [test['revenue_ratio'] for test in revenue_tests]
    print("\n2. Revenue Comparison:")
    print(f"Minimum SPA/VCG Revenue Ratio: {min(ratios):.2f}")
    print(f"Average SPA/VCG Revenue Ratio: {sum(ratios)/len(ratios):.2f}")
    
    # Analyze truthful bidding
    truthful = results['truthful_bidding']
    print("\n3. Truthful Bidding Analysis:")
    print(f"True Value: {truthful['true_value']}")
    print(f"Truthful Bid Payment: {truthful['truthful']['spa_results']['payment']}")
    print(f"Overbid Payment: {truthful['overbid']['spa_results']['payment']}")
    print(f"Underbid Payment: {truthful['underbid']['spa_results']['payment']}")


if __name__ == "__main__":
    # Run all tests
    test_suite = AuctionTestSuite()
    results = test_suite.run_all_tests()
    
    # Save results
    save_results(results, "auction_test_results.json")
    
    # Analyze results
    analyze_results(results)



