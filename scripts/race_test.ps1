\
    param(
        [Parameter(Mandatory=$true)][int]$RequestId,
        [Parameter(Mandatory=$true)][int]$MasterId = 2,
        [string]$BaseUrl = "http://localhost:8090"
    )

    # Запускает два параллельных take-запроса.
    # Ожидаемо: один 200, второй 409.

    $url = "$BaseUrl/requests/$RequestId/take/$MasterId"

    Write-Host "Race test URL: $url"

    $job1 = Start-Job -ScriptBlock { param($u) curl.exe -s -o NUL -w "%{http_code}" -X POST $u } -ArgumentList $url
    $job2 = Start-Job -ScriptBlock { param($u) curl.exe -s -o NUL -w "%{http_code}" -X POST $u } -ArgumentList $url

    Wait-Job $job1, $job2 | Out-Null

    $r1 = Receive-Job $job1
    $r2 = Receive-Job $job2

    Remove-Job $job1, $job2 | Out-Null

    Write-Host "Result #1: $r1"
    Write-Host "Result #2: $r2"
