# PowerShell script to add AGPL header to all Python files
# Usage: .\add_agpl_headers.ps1

$AGPL_HEADER = @"
# This file is part of text-to-audiobook
#
# text-to-audiobook is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# text-to-audiobook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"@

function Add-AGPLHeader {
    param(
        [string]$FilePath,
        [string]$Header
    )

    $content = Get-Content -Path $FilePath -Raw

    # Check if header already exists
    if ($content -match "GNU Affero General Public License") {
        Write-Host "⏭️  Skipping $FilePath (header already present)" -ForegroundColor Yellow
        return
    }

    # Preserve shebang line if present
    $lines = $content -split "`n"
    $shebang = ""
    $startIndex = 0

    if ($lines[0] -match "^#!") {
        $shebang = $lines[0]
        $startIndex = 1
    }

    # Add header
    $newContent = @()
    if ($shebang) {
        $newContent += $shebang
    }
    $newContent += $Header
    $newContent += ""
    $newContent += ($lines[$startIndex..($lines.Count - 1)] -join "`n")

    Set-Content -Path $FilePath -Value ($newContent -join "`n") -Encoding UTF8
    Write-Host "✅ Added header to: $FilePath" -ForegroundColor Green
}

# Find all Python files (only project files, exclude venv and build dirs)
$pythonFiles = @()
$excludeDirs = @(".venv", "venv", ".git", ".github", "build", "dist", "__pycache__", ".pytest_cache", "*.egg-info")

Get-ChildItem -Path "." -Filter "*.py" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    $path = $_.FullName
    $skip = $false

    # Check if file is in excluded directories
    foreach ($excludeDir in $excludeDirs) {
        if ($path -match [regex]::Escape("\$excludeDir\")) {
            $skip = $true
            break
        }
    }

    if (-not $skip) {
        $pythonFiles += $_
    }
}

if ($pythonFiles.Count -eq 0) {
    Write-Host "⚠️  No Python files found!" -ForegroundColor Red
    exit 1
}

Write-Host "🔄 Processing $($pythonFiles.Count) Python files..." -ForegroundColor Cyan
Write-Host ""

foreach ($file in $pythonFiles) {
    Add-AGPLHeader -FilePath $file.FullName -Header $AGPL_HEADER
}

Write-Host ""
Write-Host "✨ Done! Added AGPL headers to all Python files." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Update LICENSE file to AGPL v3"
Write-Host "2. Review LICENSES.md for third-party dependencies"
Write-Host "3. Commit changes: git add -A && git commit -m 'Add AGPL headers and license documentation'"
