import os
import subprocess

base_dir = os.path.abspath(".")
target_exe = os.path.join(base_dir, "dist", "CoreProtectGenerator.exe")
html_file = os.path.join(base_dir, "CoreProtectGenerator.html")

sed_content = f"""[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName={target_exe}
FriendlyName=CoreProtect Generator
AppLaunched=cmd.exe /c start CoreProtectGenerator.html
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
FILE0="CoreProtectGenerator.html"

[SourceFiles]
SourceFiles0={base_dir}\\

[SourceFiles0]
%FILE0%=
"""

with open("package.sed", "w", encoding="gbk") as f:
    f.write(sed_content)

os.makedirs("dist", exist_ok=True)
print("Running iexpress...")
result = subprocess.run(["iexpress", "/N", "package.sed"], capture_output=True, text=True)
print("IExpress output:", result.stdout)
print("IExpress error:", result.stderr)

if os.path.exists(target_exe):
    print("EXE created successfully at:", target_exe)
else:
    print("Failed to create EXE.")
