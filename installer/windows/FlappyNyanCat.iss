[Setup]
AppName=Flappy Nyan Cat PRO
AppVersion=1.0.0
DefaultDirName={autopf}\FlappyNyanCat
DefaultGroupName=Flappy Nyan Cat PRO
OutputDir=dist
OutputBaseFilename=FlappyNyanCat-Setup-Windows
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\FlappyNyanCat\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Flappy Nyan Cat PRO"; Filename: "{app}\FlappyNyanCat.exe"
Name: "{autodesktop}\Flappy Nyan Cat PRO"; Filename: "{app}\FlappyNyanCat.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:";

[Run]
Filename: "{app}\FlappyNyanCat.exe"; Description: "Launch Flappy Nyan Cat PRO"; Flags: nowait postinstall skipifsilent
