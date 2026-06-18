const fs = require('fs');
const path = require('path');

const wwwDir = path.join(__dirname, '..', 'www');
if (!fs.existsSync(wwwDir)) {
    fs.mkdirSync(wwwDir);
}

// Copy the main HTML file to www/index.html so Capacitor can use it as the entry point
fs.copyFileSync(
    path.join(__dirname, '..', 'CoreProtectGenerator.html'),
    path.join(wwwDir, 'index.html')
);

console.log('Web assets successfully copied to www/ for Android build.');
