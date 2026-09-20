from app.tools.rag_tool import search_runbook_semantically
test_cases = [
    {
        "query": "Android traffic suddenly dropped",
        "expected_chunk": 3
    },
    {
        "query": "Can the session metrics prove what caused the incident?",
        "expected_chunk": 4
    },
    {
        "query": "Could authentication failures explain missing events?",
        "expected_chunk": 3
    }
]

passed = 0

for case in test_cases:
    results = search_runbook_semantically.invoke({
        "query":case["query"]
    })

    retrieved_chunks = [
        result["chunk"]
        for result in results
    ]
    success = case["expected_chunk"] in retrieved_chunks

    if success:
        passed += 1
        outcome = "PASS"
    else:
        outcome = "FAIL"

    print(f"\n{outcome}: {case['query']}")
    print("Expected chunk:", case["expected_chunk"])
    print("Retrieved chunks:", retrieved_chunks)
total = len(test_cases)

print(f"\nScore: {passed}/{total}")
print(f"Pass rate: {passed / total:.0%}")