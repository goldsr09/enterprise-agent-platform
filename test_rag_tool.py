from app.tools.rag_tool import search_runbook_semantically


results = search_runbook_semantically.invoke({
    "query": "What should I investigate when Android traffic drops?"
})

for result in results:
    print("\nSource:", result["source"])
    print(result["content"])