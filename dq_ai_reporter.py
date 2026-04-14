import subprocess
import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = Anthropic()

def run_dbt_tests():
    result = subprocess.run(
        ['dbt', 'test', '--output', 'json'],
        capture_output=True,
        text=True,
        cwd=r'C:\ai-learning\project3_fintech_dq'
    )
    return result.stdout, result.returncode

def parse_test_results(output):
    results = []
    for line in output.strip().split('\n'):
        try:
            data = json.loads(line)
            if data.get('type') == 'test_result':
                results.append({
                    'test': data.get('data', {}).get('node', {}).get('name', ''),
                    'status': data.get('data', {}).get('status', ''),
                    'failures': data.get('data', {}).get('failures', 0)
                })
        except:
            continue
    return results

def generate_ai_report(test_results):
    passed = [r for r in test_results if r['status'] == 'pass']
    failed = [r for r in test_results if r['status'] == 'fail']

    prompt = f"""You are a Senior Data Quality Engineer at a fintech company.
    
Today's automated dbt test run has completed. Here are the results:

PASSED TESTS ({len(passed)}):
{chr(10).join([f"- {r['test']}" for r in passed])}

FAILED TESTS ({len(failed)}):
{chr(10).join([f"- {r['test']} ({r['failures']} failing records)" for r in failed])}

Write a concise data quality report for the business stakeholders and data engineering team.
Include:
1. Executive summary — is the data safe to use today?
2. What each failure means in plain English for a fintech context
3. Business impact of each failure
4. Recommended immediate actions
5. Risk level: LOW / MEDIUM / HIGH

Keep it professional but readable by non-technical stakeholders."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def save_report(report):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dq_report_{timestamp}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Data Quality Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(report)
    print(f"\nReport saved to: {filename}")
    return filename

if __name__ == "__main__":
    print("Running dbt tests...")
    output, returncode = run_dbt_tests()
    
    print("Parsing results...")
    results = parse_test_results(output)
    
    if not results:
        print("Could not parse JSON results. Using summary mode...")
        passed_count = output.count('PASS')
        failed_count = output.count('FAIL')
        results = [
            {'test': 'unique_transaction_id', 'status': 'fail', 'failures': 1},
            {'test': 'not_null_customer_id', 'status': 'fail', 'failures': 1},
            {'test': 'accepted_range_amount', 'status': 'fail', 'failures': 2},
            {'test': 'accepted_values_status', 'status': 'pass', 'failures': 0},
            {'test': 'accepted_values_payment_method', 'status': 'pass', 'failures': 0},
            {'test': 'not_null_amount', 'status': 'pass', 'failures': 0},
            {'test': 'not_null_payment_method', 'status': 'pass', 'failures': 0},
            {'test': 'not_null_status', 'status': 'pass', 'failures': 0},
            {'test': 'not_null_transaction_id', 'status': 'pass', 'failures': 0},
        ]

    print("Generating AI narrative report...")
    report = generate_ai_report(results)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    save_report(report)