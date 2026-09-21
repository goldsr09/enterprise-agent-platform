from app.agent import investigate

test_cases = [
    {
        "name": "valid Android metrics",
        "question": (
            "Compare Android revenue and sessions between "
            "2026-09-15 and 2026-09-16."
        ),
        "required": [
            "95,000",
            "43,000",
            "720,000",
            "350,000",
        ],
    },
    {
        "name": "missing BlackBerry data",
        "question": (
            "Compare BlackBerry revenue and sessions between "
            "2026-09-15 and 2026-09-16. "
            "If no data exists, say so and do not invent values."
        ),
        "required": ["no data"],
    },
    {
        "name": "grounded runbook guidance",
        "question": (
            "Android traffic dropped sharply. Find operational "
            "guidance. Include the runbook source and chunk numbers. "
            "Do not claim the guidance proves the cause."
        ),
        "required": [
            "runbooks/data_ingestion.md",
            "chunk",
        ],
    },
]

passed = 0

for case in test_cases:
    result = investigate(case["question"])

    if isinstance(result, dict):
        answer = result["answer"]
    else:
        answer = result

    normalized_answer = answer.lower()

    missing = [
        expected_text
        for expected_text in case["required"]
        if expected_text.lower() not in normalized_answer
    ]

    # Accept multiple ways of expressing the causation caveat.
    if case["name"] == "grounded runbook guidance":
        acceptable_caveats = [
            "do not prove",
            "does not prove",
            "do not establish",
            "does not establish",
            "cannot establish",
        ]

        if not any(
            phrase in normalized_answer
            for phrase in acceptable_caveats
        ):
            missing.append(
                "a statement that the evidence does not prove the cause"
            )

    if missing:
        outcome = "FAIL"
    else:
        outcome = "PASS"
        passed += 1

    print(f"\n{outcome}: {case['name']}")
    print(answer)

    if missing:
        print("Missing required text:", missing)

total = len(test_cases)

print(f"\nAgent score: {passed}/{total}")
print(f"Agent pass rate: {passed / total:.0%}")