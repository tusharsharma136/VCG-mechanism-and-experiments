from vcg_auction import VCGAuction, SecondPriceAuction, Bid, SpaceType
import json

def experiment_sybil_attack():
    #Demonstrate that VCG is not dominant strategy truthful with multiple identities.
    # Scenario 1: Truthful bidding
    truthful_bids = [
        Bid("A1", 100, SpaceType.BOTH),
        Bid("B1", 80, SpaceType.TOP),
        Bid("C1", 70, SpaceType.SIDEBAR)
    ]
    
    # Scenario 2: Agent A1 creates second identity
    sybil_bids = [
        Bid("A1", 60, SpaceType.TOP),
        Bid("A2", 50, SpaceType.SIDEBAR),  # Second identity
        Bid("B1", 80, SpaceType.TOP),
        Bid("C1", 70, SpaceType.SIDEBAR)
    ]
    
    vcg_truthful = VCGAuction(truthful_bids)
    vcg_sybil = VCGAuction(sybil_bids)
    
    truthful_results = {
        'allocation': vcg_truthful.find_optimal_allocation()[0],
        'payments': vcg_truthful.compute_vcg_payments()
    }
    
    sybil_results = {
        'allocation': vcg_sybil.find_optimal_allocation()[0],
        'payments': vcg_sybil.compute_vcg_payments()
    }
    
    return {
        'truthful': truthful_results,
        'sybil': sybil_results
    }

def experiment_revenue_comparison():
    #Compare VCG and second-price auction revenues.
    test_cases = [
        # Case 1: Simple scenario
        [
            Bid("A1", 100, SpaceType.BOTH),
            Bid("B1", 80, SpaceType.BOTH),
            Bid("C1", 60, SpaceType.TOP)
        ],
        # Case 2: Competitive scenario
        [
            Bid("A1", 90, SpaceType.TOP),
            Bid("B1", 85, SpaceType.SIDEBAR),
            Bid("C1", 150, SpaceType.BOTH),
            Bid("D1", 140, SpaceType.BOTH)
        ],
        # Case 3: Split allocation likely optimal
        [
            Bid("A1", 70, SpaceType.TOP),
            Bid("B1", 65, SpaceType.SIDEBAR),
            Bid("C1", 100, SpaceType.BOTH),
            Bid("D1", 60, SpaceType.TOP)
        ]
    ]
    
    results = []
    for case in test_cases:
        vcg = VCGAuction(case)
        spa = SecondPriceAuction(case)
        
        vcg_allocation, _ = vcg.find_optimal_allocation()
        vcg_payments = vcg.compute_vcg_payments()
        vcg_revenue = sum(vcg_payments.values())
        
        spa_winner, spa_payment = spa.run_auction()
        
        results.append({
            'vcg_revenue': vcg_revenue,
            'spa_revenue': spa_payment,
            'revenue_ratio': spa_payment / vcg_revenue if vcg_revenue > 0 else float('inf')
        })
    
    return results

if __name__ == "__main__":
    # Run Sybil attack experiment
    sybil_results = experiment_sybil_attack()
    print("\nSybil Attack Experiment Results:")
    print(json.dumps(sybil_results, indent=2))
    
    # Run revenue comparison experiment
    revenue_results = experiment_revenue_comparison()
    print("\nRevenue Comparison Experiment Results:")
    print(json.dumps(revenue_results, indent=2))