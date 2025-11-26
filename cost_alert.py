import json
import argparse

def parse_args():
    """Parse command-line arguments for customizing the tool's behavior, like file input or alert threshold."""
    parser = argparse.ArgumentParser(description='AWS Cost Alert Tool - Monitors costs and alerts on thresholds.')
    parser.add_argument('--file', type=str, default=None, help='JSON file path for cost data (default: use mock).')
    parser.add_argument('--threshold', type=float, default=500.0, help='Cost alert threshold (default: 500).')
    return parser.parse_args()

def load_data(file_path):
    """Load cost data either from a provided JSON file or fallback to built-in mock data for testing."""
    # Check if a file path is provided; if yes, load from file, else use mock
    if file_path:
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        mock_data = '''
        {
          "ResultsByTime": [
            {"TimePeriod": {"Start": "2025-11-09"}, "Total": {"UnblendedCost": {"Amount": "650.00"}}},
            {"TimePeriod": {"Start": "2025-11-10"}, "Total": {"UnblendedCost": {"Amount": "400.00"}}}
          ]
        }
        '''
        return json.loads(mock_data)

def check_costs(data, threshold):
    """Process the cost data to identify and collect alerts for any periods exceeding the threshold."""
    alerts = []
    for result in data.get('ResultsByTime', []):
        try:
            cost = float(result['Total']['UnblendedCost']['Amount'])
            date = result['TimePeriod']['Start']
            # If the cost is above the threshold, add an alert message to the list
            if cost > threshold:
                alerts.append(f"ALERT: High cost ${cost} on {date}")
        except KeyError as e:
            print(f"Error processing data: Missing key {e}")
        except ValueError as e:
            print(f"Error converting cost: {e}")
    return alerts

if __name__ == "__main__":
    args = parse_args()
    cost_data = load_data(args.file)  # Load data, renamed to avoid shadowing
    cost_alerts = check_costs(cost_data, args.threshold)  # Check costs, renamed to avoid shadowing
    # If there are alerts, print each one; otherwise, print a no-issue message
    if cost_alerts:
        for alert in cost_alerts:
            print(alert)
    else:
        print("No high costs detected.")
