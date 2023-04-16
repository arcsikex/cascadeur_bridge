# Cascadeur Bridge for Blender

Cascadeur Bridge is a Blender addon designed to help you integrate Cascadeur into your workflow with Blender.

## Features
- Import whole scene from Cascadeur
- Import animation to selected armature

## Installation

To install Cascadeur Bridge, follow these steps:

1. Download the latest release from the **releases**.
2. Extract the files
3. Open Blender and go to Edit > Preferences
4. Click on the Add-ons tab, then click the Install button at the top of the window.
5. Navigate to the downloaded Cascadeur Bridge file and select the ***cascadeur_bridge.zip file***.
6. Click the Install Add-on button, then enable the addon by clicking the checkbox next to its name.
### For Cascadeur's side:
1. Copy the *external* folder to **CASCADEUR FOLDER/resources/scripts/commands**
2. Copy the *_socket.pyd* and *select.pyd* files *CASCADEUR FOLDER/python/DLLs* (Hopefully it will be included in the future)

## Usage

You can find the addon on the side panel of the 3D Viewport with the name CSC Bridge.
- Select an Armature to **Import Action** to the selected object. **This armature should be exactly the same in both software!**
This operator imports the Cascadeur scene as fbx, apply the imported action to the selected armature and delete the imported objects.
- **Import Scene** will simply import the current Cascadeur scene as an fbx.

## Future plans:
- Make fbx import/export options section
- Cascadeur scripts installation from Blender
- Blender > Cascadeur exporter
- Import actions from all opened scene
- Set up camera in Cascadeur (to match with Blender)

If you have more idea/request or you found a bug please report it in the **Issues**.


---
