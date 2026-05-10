param(
    [string]$Summary = "本次收工由 close-work.ps1 自動產生。",
    [string]$Next = "Backend Phase 6：NFI trees / 子紀錄匯入策略",
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\Projects\forest-harvest-system"
$ObsidianRoot = "C:\ObsidianVaults\ForestHarvestSystem"
$FirebaseProjectId = "forestry-rs-monitor"
$GitHubRepo = "https://github.com/cct7366488-collab/forest-harvest-system"

Set-Location $ProjectRoot

$today = Get-Date -Format "yyyy-MM-dd"
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Ensure-Dir($path) {
    New-Item -ItemType Directory -Force $path | Out-Null
}

function Write-Lines($path, $lines) {
    Set-Content -Encoding UTF8 -Path $path -Value $lines
}

function Copy-IfExists($source, $target) {
    if (Test-Path $source) {
        Copy-Item $source $target -Force
    }
}

Ensure-Dir "docs\worklog"
Ensure-Dir "firebase\project_status"
Ensure-Dir "firebase\work_logs"
Ensure-Dir "$ObsidianRoot\worklog"
Ensure-Dir "$ObsidianRoot\database"
Ensure-Dir "$ObsidianRoot\database\nfi"
Ensure-Dir "$ObsidianRoot\teaching"

$gitBranch = git rev-parse --abbrev-ref HEAD
$gitCommit = git rev-parse --short HEAD
$recentCommits = git log --oneline -10
$gitStatusBefore = git status --short

$dbCounts = @("資料庫未檢查。")
try {
    $containerNames = docker ps --format "{{.Names}}"
    if ($containerNames -contains "forest_postgis") {
        $dbCounts = docker exec -i forest_postgis psql -U forest_user -d forest_db -c "SELECT 'species' AS table_name, COUNT(*) FROM species UNION ALL SELECT 'volume_models', COUNT(*) FROM volume_models UNION ALL SELECT 'height_models', COUNT(*) FROM height_models UNION ALL SELECT 'plots', COUNT(*) FROM plots UNION ALL SELECT 'trees', COUNT(*) FROM trees;"
    } else {
        $dbCounts = @("forest_postgis container 未執行。")
    }
} catch {
    $dbCounts = @("資料庫檢查失敗：" + $_.Exception.Message)
}

$logLines = @(
"# Forest Harvest System 收工紀錄 - $today",
"",
"## 一、本次收工摘要",
"",
$Summary,
"",
"## 二、專案位置",
"",
"- 本機：$ProjectRoot",
"- GitHub：$GitHubRepo",
"- Firebase Project ID：$FirebaseProjectId",
"- Obsidian Vault：$ObsidianRoot",
"",
"## 三、Git 狀態",
"",
"- Branch：$gitBranch",
"- Commit：$gitCommit",
"",
"### 收工前 Git status --short",
"```text"
)

if ($gitStatusBefore.Count -eq 0) {
    $logLines += "working tree clean"
} else {
    $logLines += $gitStatusBefore
}

$logLines += @(
"```",
"",
"### 最近 Git commits",
"```text"
)

$logLines += $recentCommits

$logLines += @(
"```",
"",
"## 四、資料庫狀態摘要",
"",
"```text"
)

$logLines += $dbCounts

$logLines += @(
"```",
"",
"## 五、下次開工建議",
"",
$Next,
"",
"## 六、收工時間",
"",
$now
)

Write-Lines "docs\worklog\$today.md" $logLines
Write-Lines "docs\worklog\work-log.md" $logLines
Write-Lines "$ObsidianRoot\worklog\$today.md" $logLines
Write-Lines "$ObsidianRoot\worklog\work-log.md" $logLines

$todoLines = @(
"# Forest Harvest System TODO",
"",
"## 下一階段",
"",
"- [ ] $Next",
"- [ ] 判斷 NFI4 中哪些欄位屬於 trees 樣木層級",
"- [ ] 建立 NFI4 → trees 欄位對應表",
"- [ ] 建立 trees 匯入腳本",
"- [ ] 測試匯入少量樣木資料",
"- [ ] 驗證 trees.plot_id 與 plots.id 關聯",
"- [ ] 匯入 species 樹種代碼資料",
"- [ ] 匯入 volume_models 立木材積式資料",
"- [ ] 匯入 height_models 樹高曲線式資料",
"- [ ] 建立材積估算 API",
"- [ ] 建立樹高估算 API",
"- [ ] 建立前端地圖介面"
)

Write-Lines "docs\worklog\todo.md" $todoLines
Write-Lines "$ObsidianRoot\worklog\todo.md" $todoLines

$readmeLines = @(
"# Forest Harvest System 開發筆記本",
"",
"## 專案定位",
"",
"Forest Harvest System 是森林收穫、森林監測、GIS 空間資料、全國森林資源調查資料與後續碳匯 MRV 分析的整合型平台。",
"",
"## 本機專案位置",
"",
$ProjectRoot,
"",
"## GitHub Repository",
"",
$GitHubRepo,
"",
"## Firebase Project ID",
"",
$FirebaseProjectId,
"",
"## Obsidian Vault",
"",
$ObsidianRoot,
"",
"## 最近收工摘要",
"",
$Summary,
"",
"## 目前 Git 狀態",
"",
"- Branch：$gitBranch",
"- Commit：$gitCommit",
"",
"## 下次開工優先事項",
"",
"1. 執行 tools\start-work.ps1。",
"2. 讀取本 readme.md。",
"3. 確認本機、GitHub、Obsidian、Firebase 狀態。",
"4. 接續：$Next",
"",
"## 最近收工時間",
"",
$now
)

Write-Lines "$ObsidianRoot\readme.md" $readmeLines

Copy-IfExists "docs\setup-guide.md" "$ObsidianRoot\teaching\setup-guide.md"

if (Test-Path "docs\data") {
    Copy-Item "docs\data\*.md" "$ObsidianRoot\database\nfi\" -Force -ErrorAction SilentlyContinue
}

if (Test-Path "docs\database\schema-design.md") {
    Copy-Item "docs\database\schema-design.md" "$ObsidianRoot\database\schema-design.md" -Force
}

$status = [ordered]@{
    project_name = "Forest Harvest System"
    firebase_project_id = $FirebaseProjectId
    github_repository = $GitHubRepo
    obsidian_vault = $ObsidianRoot
    local_project_path = $ProjectRoot
    git_branch = $gitBranch
    git_commit = $gitCommit
    summary = $Summary
    next_phase = $Next
    updated_at = $now
}

$status | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 "firebase\project_status\current-status.json"

$worklogJson = [ordered]@{
    date = $today
    summary = $Summary
    next_phase = $Next
    git_branch = $gitBranch
    git_commit = $gitCommit
    updated_at = $now
}

$worklogJson | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 "firebase\work_logs\$today.json"

git add -A

$pending = git status --porcelain

if ($pending.Count -gt 0) {
    git commit -m "Closing log $today"
    if (-not $NoPush) {
        git push
    }
} else {
    Write-Host "沒有需要 commit 的變更。"
}

Write-Host ""
Write-Host "=== 收工檢查：Git status ==="
git status

Write-Host ""
Write-Host "=== 收工檢查：本機 worklog ==="
dir docs\worklog

Write-Host ""
Write-Host "=== 收工檢查：Obsidian ==="
dir $ObsidianRoot
dir "$ObsidianRoot\worklog"

Write-Host ""
Write-Host "=== 收工檢查：Firebase status files ==="
dir firebase\project_status
dir firebase\work_logs

Write-Host ""
Write-Host "=== 收工完成 ==="
