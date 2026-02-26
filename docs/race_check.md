# Проверка гонки take (два параллельных запроса)

В PowerShell используй настоящий curl:

1) Убедись, что заявка #ID в статусе assigned и назначена на мастера 2.

2) Запусти в двух терминалах одновременно:

```powershell
curl.exe -X POST "http://localhost:8090/requests/ID/take/2"
```

Ожидаемое поведение:
- один запрос вернёт 200 (status=in_progress)
- второй вернёт 409 Conflict
