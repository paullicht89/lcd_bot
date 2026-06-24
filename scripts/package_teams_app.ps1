$ErrorActionPreference = "Stop"

$source = "teams\lcd_bot"
$outputDir = "dist"
$output = Join-Path $outputDir "lcd-teams-bot.zip"
$stage = Join-Path $outputDir "lcd-teams-bot-package"

New-Item -ItemType Directory -Force $outputDir | Out-Null
if (Test-Path $output) {
    Remove-Item $output
}
if (Test-Path $stage) {
    Remove-Item -Recurse -Force $stage
}

New-Item -ItemType Directory -Force (Join-Path $stage "icons") | Out-Null
Copy-Item (Join-Path $source "manifest.json") (Join-Path $stage "manifest.json")
Copy-Item (Join-Path $source "icons\color.png") (Join-Path $stage "icons\color.png")
Copy-Item (Join-Path $source "icons\outline.png") (Join-Path $stage "icons\outline.png")

Compress-Archive -Path "$stage\*" -DestinationPath $output
Write-Host "Created $output"
