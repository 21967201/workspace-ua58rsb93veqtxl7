# Step 3: Check promotion candidates (pages with timeline entries)
$promotionCandidates = @()

Get-Content "D:\QClawX\data\workspace-ua58rsb93veqtxl7\all_pages.txt" | ForEach-Object {
    $slug = $_
    $content = & bun run "C:\Users\Administrator\gbrain\src\cli.ts" get $slug 2>&1
    if ($content -match '### \d{4}-\d{2}-\d{2}') {
        $promotionCandidates += $slug
        Write-Host "Candidate: $slug"
    }
}

$promotionCandidates | Out-File -FilePath "D:\QClawX\data\workspace-ua58rsb93veqtxl7\promotion_candidates.txt" -Encoding UTF8
Write-Host "Total promotion candidates: $($promotionCandidates.Count)"
