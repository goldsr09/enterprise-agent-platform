from app.agent import investigate

answer = investigate(
    "Compare Android revenue and sessions between "
    "2026-09-15 and 2026-09-16. "
    "Calculate the percentage decline for each. "
    "Then search the operational runbook using the query 'sessions' "
    "and list the recommended investigation steps. "
    "Do not claim that the runbook proves the cause."
)

print("\nFinal answer:")
print(answer)