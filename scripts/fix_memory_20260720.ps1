$path = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\MEMORY.md"
$content = Get-Content $path -Raw

# Remove stale "Promoted From Short-Term Memory" section
$splitMarker = "## Promoted From Short-Term Memory"
$parts = $content -split $splitMarker
if ($parts.Count -eq 2) {
    $content = $parts[0]
}

# Update consolidation header
$old1 = "*Last Consolidation: 2026-07-15 11:10 (Memory Dreaming Promotion)*"
$new1 = "*Last Consolidation: 2026-07-20 09:47 (Memory Dreaming Promotion)*"
$content = $content.Replace($old1, $new1)

$old2 = "*Next Consolidation: 2026-07-20 (weekly Dream Memory Consolidation)*"
$new2 = "*Next Consolidation: 2026-07-27 (weekly dream consolidation)*"
$content = $content.Replace($old2, $new2)

$old3 = "*Note: 12 cron tasks active; Added OpenSquilla(P0 #12) + paper trend(SSPM/Agora/SAGEAgent) + harness0(P2 watch)."
$new3 = "*Note: 12 cron tasks active; Added 07-20 monitoring (WAIC 2026), TencentDB Agent Memory P1-candidate, G-Memory P2. Dry spell >16 days. Cleaned stale 07-07 block."
$content = $content.Replace($old3, $new3)

# Insert 07-20 monitoring record after 07-15 section
$marker = "### Latest Monitoring Record (2026-07-15, 09:46 run)"
$idx = $content.IndexOf($marker)
if ($idx -ge 0) {
    $before = $content.Substring(0, $idx)
    $rest = $content.Substring($idx + $marker.Length)
    
    $nextH3 = $rest.IndexOf("`r`n### L")
    if ($nextH3 -ge 0) {
        $section = $rest.Substring(0, $nextH3)
        $after = $rest.Substring($nextH3)
        
        $newBlock = "`r`n`r`n"
        $newBlock += "### Latest Monitoring Record (2026-07-20, 09:46 run)"
        $newBlock += "`r`n- **Monitoring Coverage**: 2026-07-19->20; **0 P0, 0 P1** found (dry spell >16 days)"
        $newBlock += "`r`n- **P0**: 0; **P1(impact>8.5)**: 0"
        $newBlock += "`r`n- **WAIC 2026** (7/17-20) in progress, theme Token Cost-Efficiency Era"
        $newBlock += "`r`n- **P1-candidate(to verify)**: TencentDB Agent Memory (9k stars, vector DB 4-layer memory arch)"
        $newBlock += "`r`n- **P2**: G-Memory (GitHub bingreeky/GMemory, hierarchical multi-agent memory)"
        $newBlock += "`r`n- **Tracked P0**: headroom(stable), DECS/AbstractCoT(no new refs)"
        $newBlock += "`r`n- **Details**: See memory/2026-07-20-tech.md"
        
        $beforeSection = $marker + $section
        $content = $before + $beforeSection + $newBlock + $after
    }
}

$content = $content.TrimEnd()
Set-Content $path $content -Encoding UTF8
$len = $content.Length
Write-Host "Updated MEMORY.md. Length: $len chars"
