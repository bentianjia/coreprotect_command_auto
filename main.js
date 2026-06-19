const { app, BrowserWindow } = require('electron')
const path = require('path')

function createWindow () {
  const win = new BrowserWindow({
    width: 950,
    height: 850,
    autoHideMenuBar: true,
    show: false, // 优化体验：加载完再显示
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('CoreProtectGenerator.html')
  
  win.once('ready-to-show', () => {
    win.show()
  })
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
