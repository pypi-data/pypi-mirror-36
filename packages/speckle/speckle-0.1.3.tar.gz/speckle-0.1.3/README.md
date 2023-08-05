# SpeckleBlender
Speckle for Blender Client

# Update - May 2, 2018
## Disclaimer
This code is very WIP and as such should be used with extreme caution, on non-sensitive projects.
There is much to be tightened up, optimized, organized, etc. but the basic functionality is there.
`SpeckleClient.py` could be adapted for generic Python usage.

## Installation

This works like a normal Blender add-on:
1. Download the 'speckle' folder
2. Place into 'BLENDER_DIRECTORY/VERSION#/scripts/addons_contrib'
3. Start Blender
4. Go to User Preferences (Ctrl + Alt + U)
5. Go to the Add-ons tab
6. Find and enable A Blend of Speckle in the Testing category
7. Click Save User Settings

## Usage

Usage is fairly simple, but for now is with a couple caveats:
1. There must be an already created profile in your SpeckleSettings folder (`AppData/Local/SpeckleSettings`) with an authentication token. Although it is possible to create a profile and login using the Python client, this is not yet exposed in Blender.
2. SpeckleBlender will take the first profile in this folder. This is hard-coded at the moment, but will change when the login system is properly implemented.
3. Currently, only Mesh objects are supported. Anything else will be ignored. Curve objects could be supported in the future.

**SpeckleBlender** adds some operators:
- **Speckle - Import Stream** : Choose from a stream in your profile and import all objects from that stream.
- **Speckle - Create Stream** : Create a Speckle stream.
- **Speckle - Delete Stream** : Delete a Speckle stream.
- **Speckle - Update Object** : Updates the selected object if it is enabled for Speckle usage.
- **Speckle - Update All** : Updates all objects that are enabled for Speckle usage.
- **Speckle - Upload Object** : Choose from a stream in your profile and upload active object to that stream. This enables the object for Speckle usage and sets its update direction to 'Send'.

**SpeckleBlender** adds some Object properties:
- **Enabled** : Enables the object for Speckle usage.
- **Send/Receive** : Sets the update direction on a per-object level. 'Send' will update the remote object with local data, 'Receive' will replace the local object with remote data.
- **Stream ID** : Possibly useless. Holds the Stream ID that this object is part of. Meaningless if the object is part of multiple streams.
- **Object ID** : The ID of the object on the server.

**SpeckleBlender** adds some Scene properties:
- **Scale** : Scale factor for incoming data. Outgoing data is scaled by `1 / Scale`.
- **Update all** : Triggers the `Speckle - Update All` operator. Currently non-functional.
- **Import stream** : Triggers the `Speckle - Import Stream` operator.

## Notes
SpeckleBlender is written and sort of maintained by [Tom Svilans](http://tomsvilans.com) ([Github](https://github.com/tsvilans)).