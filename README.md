# Cascadeur Bridge for Blender

Cascadeur Bridge is a Blender addon designed to help you integrate Cascadeur into your workflow with Blender.

For a visual introduction watch the youtube video:

[![Watch the video](https://img.youtube.com/vi/0muo9EPIPSE/default.jpg)](https://youtu.be/0muo9EPIPSE)

## Features

![Cascadeur Bridge UI](/doc/addon_side_panel.png)

- Start Cascadeur from Blender
- Export scene from Blender to Cascadeur
- Import whole scene from Cascadeur
- Import animation to selected armature
- Batch import all opened scenes and actions from Cascadeur
- Configure Cascadeur FBX export settings
- Configure Blender FBX import/export settings

## Installation

To install Cascadeur Bridge, follow these steps:

1. Download the [latest release](https://github.com/arcsikex/cascadeur_bridge/releases/tag/0.7.0) from the **releases**
> If you are using Cascadeur version **2022.3.1 or older** use [Cascadeur Bridge 0.4.1](https://github.com/arcsikex/cascadeur_bridge/releases/tag/0.4.1)
2. Open Blender and go to **Edit > Preferences**
4. Click on the Add-ons tab, then click the Install button at the top of the window
5. Select the downloaded zip
6. Click the **Install Add-on** button, then enable the addon by clicking the checkbox next to its name
7. **Set the Cascadeur executable path**
8. Click the **Install Requirements** button (If you get an error try to restart Blender as an Admin)

![Preferences view of the addon](/doc/addon_pereferences.png)

## Usage

The addon can be accessed from the N panel of the 3D Viewport in Blender.
- In the add-on preferences, you have the option to set the display name of the N panel. This feature is particularly useful if you want to merge the user interface with a different add-on.
- **Export to Cascadeur** will export the Blender scene and import it to Cascadeur.
- **Import Action**: To import an action into the selected object, first, make sure to select an **Armature that exactly matches the one in Cascadeur**.
 This operator will import the Cascadeur scene as an fbx file, apply the imported action to the selected armature, and then delete the imported objects.
- **Import Scene** will simply import the current Cascadeur scene as an fbx file.
- **Batch Import** Similar to "Import Scene" and "Import Action", but this option allows you to import scenes or actions from **all opened scenes in Cascadeur**.
- **Cascadeur Export Settings and Blender Import/Export Settings:** The default settings are optimized for typical use, but you might need different settings based on your specific requirements. Adjust the usual Blender FBX export/import settings and the Cascadeur FBX export settings here. Once you find the settings that work for you, remember to click the Save Settings button.



## Remove the addon

To remove the addon 
- from **Blender** go to **Edit > Preferences > Add-ons** and click on the Remove button of the add-on.
- from **Cascadeur** 
    - go to your commands folder (*CASCADEUR PATH\resources\scripts\python\commands*) and delete the ***externals*** folder. 

## Future plans:
- Bind textures automatically in Cascaduer
- Set up camera in Cascadeur (to match with Blender)
- Export action from Blender

If you have more idea/request or you found a bug please report it in the **Issues**.

---
