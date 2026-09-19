from app.tools.runbook_tool import search_runbook


result = search_runbook.invoke({
    "query": "sessions"
})

print(result)