$buf = [System.IO.File]::ReadAllBytes("D:\QClaw\v0.2.35.624\resources\app.asar")
$headerSize = [BitConverter]::ToUInt32($buf, 4)
$head = New-Object byte[] $headerSize
[Array]::Copy($buf, 8, $head, 0, $headerSize)
# Skip UTF-8 BOM if present
$start = 0
if ($head[0] -eq 0xEF -and $head[1] -eq 0xBB -and $head[2] -eq 0xBF) { $start = 3 }
$utf8 = [System.Text.Encoding]::UTF8.GetString($head[$start..($head.Length-1)])
if (-not $utf8.StartsWith("{")) { $utf8 = $utf8.Substring($utf8.IndexOf("{")) }
$h = $utf8 | ConvertFrom-Json
Write-Host "Parsed OK. Top keys: $($h.files.PSObject.Properties.Name.Count)"

# Recursively find hermes_cli_main
function Find-Key($obj, $path) {
    foreach ($p in $obj.PSObject.Properties) {
        $name = $p.Name
        $val = $p.Value
        if ($name -like "*hermes_cli_main*") {
            Write-Host "FOUND: $path/$name"
        }
        if ($val -and $val.PSObject.Properties.Name -contains "files") {
            Find-Key $val.files "$path/$name"
        }
    }
}
Find-Key $h.files ""
Write-Host "Search done"
