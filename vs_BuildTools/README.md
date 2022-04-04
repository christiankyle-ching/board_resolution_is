# Offline Visual Studio Installation

[See this guide for the full documentation](https://docs.microsoft.com/en-us/visualstudio/install/create-an-offline-installation-of-visual-studio?view=vs-2022)

## Create an Offline Installer

To create an offline installer, use this on a `cmd (Admin)`:

```bat
vs_BuildTools.exe --layout C:\localVSlayout ^
--add Microsoft.VisualStudio.Component.Roslyn.Compiler ^
--add Microsoft.Component.MSBuild ^
--add Microsoft.VisualStudio.Component.CoreBuildTools ^
--add Microsoft.VisualStudio.Workload.MSBuildTools ^
--add Microsoft.VisualStudio.Component.Windows10SDK ^
--add Microsoft.VisualStudio.Component.VC.CoreBuildTools ^
--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest ^
--add Microsoft.VisualStudio.Component.VC.CMake.Project ^
--add Microsoft.VisualStudio.Component.Windows10SDK.20348 ^
--lang en-US
```

You will generate a folder in `C:\localVSlayout`. **Zip this folder and transfer to other PC**.

## Install on other PC

Assuming you already have the `localVSlayout.zip`, extract it first. You can then install this layout by running this command on a `cmd (Admin)`. Make sure to `cd` first to where the extracted folder is located.

```bat
.\localVSlayout\vs_BuildTools.exe --noweb ^
--add Microsoft.VisualStudio.Component.Roslyn.Compiler ^
--add Microsoft.Component.MSBuild ^
--add Microsoft.VisualStudio.Component.CoreBuildTools ^
--add Microsoft.VisualStudio.Workload.MSBuildTools ^
--add Microsoft.VisualStudio.Component.Windows10SDK ^
--add Microsoft.VisualStudio.Component.VC.CoreBuildTools ^
--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest ^
--add Microsoft.VisualStudio.Component.VC.CMake.Project ^
--add Microsoft.VisualStudio.Component.Windows10SDK.20348 ^
--lang en-US
```

## .bat Files

Instead of typing out the commands, you can just use the `*.bat` files.
