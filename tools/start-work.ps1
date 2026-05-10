$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\Projects\forest-harvest-system"
$ObsidianRoot = "C:\ObsidianVaults\ForestHarvestSystem"

Set-Location $ProjectRoot

Write-Host ""
Write-Host "=== Forest Harvest System 開工檢查 ==="
Write-Host ""

Write-Host "=== 1. Obsidian readme.md ==="
if (Test-Path "$ObsidianRoot\readme.md") {
    Get-Content "$ObsidianRoot\readme.md"
} else {
    Write-Host "找不到 Obsidian readme.md"
}

Write-Host ""
Write-Host "=== 2. 最近 work-log ==="
if (Test-Path "$ObsidianRoot\worklog\work-log.md") {
    Get-Content "$ObsidianRoot\worklog\work-log.md"
} else {
    Write-Host "找不到 Obsidian work-log.md"
}

Write-Host ""
Write-Host "=== 3. TODO ==="
if (Test-Path "docs\worklog\todo.md") {
    Get-Content "docs\worklog\todo.md"
} else {
    Write-Host "找不到 docs\worklog\todo.md"
}

Write-Host ""
Write-Host "=== 4. Git status ==="
git status

Write-Host ""
Write-Host "=== 5. 最近 Git commits ==="
git log --oneline -10

Write-Host ""
Write-Host "=== 6. Docker containers ==="
docker ps

Write-Host ""
Write-Host "=== 7. PostgreSQL 核心資料表筆數 ==="
try {
    docker exec -i forest_postgis psql -U forest_user -d forest_db -c "SELECT 'species' AS table_name, COUNT(*) FROM species UNION ALL SELECT 'volume_models', COUNT(*) FROM volume_models UNION ALL SELECT 'height_models', COUNT(*) FROM height_models UNION ALL SELECT 'plots', COUNT(*) FROM plots UNION ALL SELECT 'trees', COUNT(*) FROM trees;"
} catch {
    Write-Host "資料庫檢查失敗："
    Write-Host $_.Exception.Message
}

Write-Host ""
Write-Host "=== 開工檢查完成 ==="
