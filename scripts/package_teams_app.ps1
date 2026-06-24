$ErrorActionPreference = "Stop"

$source = "teams\lcd_bot"
$outputDir = "dist"
$output = Join-Path $outputDir "lcd-teams-bot.zip"
$stage = Join-Path $outputDir "lcd-teams-bot-package"

python .\scripts\validate_teams_package.py $source

New-Item -ItemType Directory -Force $outputDir | Out-Null
if (Test-Path $output) {
    Remove-Item $output
}
if (Test-Path $stage) {
    Remove-Item -Recurse -Force $stage
}

New-Item -ItemType Directory -Force $stage | Out-Null
Copy-Item (Join-Path $source "manifest.json") (Join-Path $stage "manifest.json")
Copy-Item (Join-Path $source "color.png") (Join-Path $stage "color.png")
Copy-Item (Join-Path $source "outline.png") (Join-Path $stage "outline.png")

Compress-Archive -Path "$stage\*" -DestinationPath $output
python .\scripts\validate_teams_package.py $output
Write-Host "Created $output"
