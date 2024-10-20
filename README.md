# VCG and Second-Price Auction Comparison

This project implements a comparison between Vickrey-Clarke-Groves (VCG) auctions and Second-Price auctions, providing insights into their revenue and allocation mechanisms. The implementation supports different bidding strategies and tests for auction vulnerabilities, such as Sybil attacks.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Features

- Implementations of VCG and Second-Price auctions.
- Bidding strategies using dataclasses for structured data.
- Capability to run multiple test cases, including:
  - Sybil attack simulations
  - Revenue comparisons between auction types
  - Truthful bidding scenarios
- Custom JSON encoder for handling enums in results.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tusharsharma136/VCG-mechanism-and-experiments.git
   ```

2. Install the required packages. If you're using Python 3, you can create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your input data in JSON format. Here is an example:

   ```json
   {
       "bids": [
           {"bidder_id": "A1", "value": 100, "space_type": "b"},
           {"bidder_id": "B1", "value": 60, "space_type": "t"},
           {"bidder_id": "C1", "value": 50, "space_type": "s"},
           {"bidder_id": "D1", "value": 80, "space_type": "b"}
       ]
   }
   ```

2. Run the auction experiment:

   ```python
   from vcg_auction import run_experiment

   results = run_experiment("path/to/your/input_file.json")
   print("Experiment Results:")
   print(results)
   ```

3. To analyze results, you can call:

   ```python
   from vcg_auction import analyze_results

   analyze_results(results)
   ```

## Testing

To run the test suite for the auction implementation, you can execute:

```python
from auction_test_suite import AuctionTestSuite

test_suite = AuctionTestSuite()
results = test_suite.run_all_tests()
print("All test results:")
print(results)
```

## Results

The results of the auction experiments will provide insights into the allocations, payments, and revenue generated by both auction types. The analysis will highlight key findings from the tests, such as the impact of Sybil attacks and revenue ratios between auction methods.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request. 

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your branch and open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
