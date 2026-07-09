# get-session-context.ps1
# Lists recently modified project files sorted by last write time (newest first).
# Output is consumed by the end-session skill to infer what was worked on this session.
# Excludes meta/tooling directories that are not meaningful session work signals.

param(
    [int]$HoursBack = 8,
    [string]$Root = "."
)

$cutoff = (Get-Date).AddHours(-$HoursBack)

# Directories to exclude — tooling/meta dirs, not project work signals
$excludedDirs = @('.venv', 'node_modules', '.git', '.bob', '.agent_docs', '.opencode', '__pycache__', 'dist', '.databricks')

$rootResolved = (Resolve-Path $Root).Path.TrimEnd('\')

Get-ChildItem -Path $Root -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $file = $_
        $recent = $file.LastWriteTime -ge $cutoff
        # Check if the file's path contains any excluded directory segment
        $excluded = $excludedDirs | Where-Object {
            $seg = $_
            $file.FullName -like "*\$seg\*" -or $file.FullName -like "*\$seg"
        }
        $recent -and (-not $excluded)
    } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 40 |
    ForEach-Object {
        $rel = $_.FullName.Replace($rootResolved + '\', '')
        "$($_.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))  $rel"
    }
