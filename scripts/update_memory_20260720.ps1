$path = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\MEMORY.md"
$content = Get-Content $path -Raw

# Remove the stale "Promoted From Short-Term Memory" section (lines with HTML comments and garbled Chinese)
$split = $content -split "`r`n## Promoted From Short-Term Memory \(2026-07-07\)"
if ($split.Count -eq 2) {
    $content = $split[0]
}

# Update consolidation header
$old = "*Last Consolidation: 2026-07-15 11:10 (Memory Dreaming Promotion)*"
$new = "*Last Consolidation: 2026-07-20 09:47 (Memory Dreaming Promotion)*"
$content = $content.Replace($old, $new)

$old = "*Next Consolidation: 2026-07-20 (weekly Dream Memory Consolidation)*"
$new = "*Next Consolidation: 2026-07-27 (weekly dream consolidation)*"
$content = $content.Replace($old, $new)

$old = "*Note: 12 cron tasks active; Added OpenSquilla(P0 #12) + paper trend(SSPM/Agora/SAGEAgent) + harness0(P2 watch). All entries"
$new = "*Note: 12 cron tasks active; Added 07-20 monitoring (WAIC 2026), TencentDB Agent Memory P1-candidate, G-Memory P2. Dry spell >16 days. Cleaned stale 07-07 block. All entries"
$content = $content.Replace($old, $new)

# Insert 07-20 monitoring record after 07-15 section
$marker = "### Latest Monitoring Record (2026-07-15, 09:46 run)"
$idx = $content.IndexOf($marker)
if ($idx -gt 0) {
    $start = $idx
    $rest = $content.Substring($idx)
    # Find next "###" after the marker
    $nextIdx = $rest.IndexOf("`r`n### ", [Math]::Max(1, $marker.Length))
    if ($nextIdx -gt 0) {
        $sectionEnd = $idx + $nextIdx
        $before = $content.Substring(0, $sectionEnd)
        $after = $content.Substring($sectionEnd)
        
        $newBlock = "`r`n`r`n### Latest Monitoring Record (2026-07-20, 09:46 run)" + "`r`n"
        $newBlock += "- **Monitoring Coverage**: 2026-07-19->20; **0 P0, 0 P1** found (dry spell >16 days)" + "`r`n"
        $newBlock += "- **P0**: 0; **P1(impact>8.5)**: 0" + "`r`n"
        $newBlock += "- **WAIC 2026** (7/17-20) in progress, theme `"Token Cost-Efficiency Era`" (industry trend, not algorithmic breakthrough)" + "`r`n"
        $newBlock += "- **P1-candidate(to verify)**: TencentDB Agent Memory (9k stars, Tencent vector DB 4-layer memory arch, complements Markdown)" + "`r`n"
        $newBlock += "- **P2**: G-Memory (GitHub bingreeky/GMemory, hierarchical multi-agent memory)" + "`r`n"
        $newBlock += "- **Tracked P0**: headroom(stable), DECS/AbstractCoT(no new refs)" + "`r`n"
        $newBlock += "- **Details**: See `memory/2026-07-20-tech.md`"
        
        $content = $before + $newBlock + $after
    }
}

# Trim trailing whitespace
$content = $content.TrimEnd()

Set-Content $path $content -Encoding UTF8
Write-Output "MEMORY.md updated. Length: $($content.Length) chars"
