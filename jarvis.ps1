$origLocation = Get-Location
Set-Location "D:\CLI"
& "D:\CLI\.venv\Scripts\python.exe" "D:\CLI\main.py" $args
Set-Location $origLocation
