Write-Host "Running pre-publish checks..." -ForegroundColor Cyan

$errors = @()

if (!(Test-Path "README.md")) {
    $errors += "README.md is missing."
} else {
    $readme = Get-Content "README.md" -Raw
    if ($readme -match "USERNAME/REPO") {
        $errors += "README still contains placeholder 'USERNAME/REPO'."
    }
    if ($readme -match "your-demo-link" -or $readme -match "your-video-link") {
        $errors += "README still contains demo placeholder links."
    }
}

$requiredScreens = @(
    "docs/screenshots/login.png",
    "docs/screenshots/admin-dashboard.png",
    "docs/screenshots/teacher-dashboard.png",
    "docs/screenshots/student-dashboard.png",
    "docs/screenshots/grades.png"
)

foreach ($screen in $requiredScreens) {
    if (!(Test-Path $screen)) {
        $errors += "Missing screenshot: $screen"
    }
}

if (Test-Path "db.sqlite3") {
    Write-Host "Info: db.sqlite3 exists locally (ok if not committed)." -ForegroundColor Yellow
}

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "Pre-publish check FAILED:" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host "- $_" -ForegroundColor Red }
    exit 1
}

Write-Host ""
Write-Host "Pre-publish check PASSED." -ForegroundColor Green
exit 0
