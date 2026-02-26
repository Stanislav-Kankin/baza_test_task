# Проверка API из PowerShell

В PowerShell `curl` — это алиас на `Invoke-WebRequest`, поэтому `-X` не работает.
Используй один из вариантов:

## Вариант A: curl.exe (настоящий curl)
```powershell
curl.exe -X POST "http://localhost:8090/requests/?client_name=Иван&phone=123&address=ул.Тест&problem_text=Не работает"
curl.exe -X POST "http://localhost:8090/requests/1/assign/2"
curl.exe -X POST "http://localhost:8090/requests/1/take/2"
curl.exe -X POST "http://localhost:8090/requests/1/complete/2"
```

## Вариант B: Invoke-RestMethod
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8090/requests/1/assign/2"
```
