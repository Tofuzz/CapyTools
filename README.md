# CapyTools
A compilation of maya python tools I built over last year to be more efficient :
  - CapyAnim, for animation
  - CapyRig, for rigging
  
![capytools_overview](https://user-images.githubusercontent.com/132166620/235325155-5473901f-f1a0-40c2-8b9e-3d9b24647f08.png)


All submenus can be collapsed, allowing you to display only the tools that you really need.
___

[Capyanim](#capyanim)

  - [Quick anim](#quick-anim)
    - [Quick spline](#quick-spline)
    - [Motion curves](#motion-curves)
    - [Offet machine](#offset-machine)
    - [Noise machine](#noise-machine)
    - [Reset](#reset)
  - [Easy constraints](#easy-constraints)
  
 [Capyrig](#capyrig)
 
  - [Quick rig](#quick-rig)
  - [Gym](#gym)
  - [Better wire](#better-wire)
  - [Easy constraints](#easy-constraints)

___


# Capyanim


### Quick anim

#### Quick spline
To keep the graph editor clean, by quickly deleting useless information.
  
  - 'Less curves' removes curves that do not contain animation.

  - 'Less keys' removes keys that do not modify the channel's values
      
#### Motion curves
Creates motion trails that doesn't stop maya from working properly. They are just Nurb curves with Locators marking each keyframes, which makes them very lightweight.
  - Step curve
  - Spline curve
  - Delete motion curves
      
#### Offset machine
Move selected keys with precision.
      
#### Noise machine
Offset the selected keys by a random value. 'Alternate' ensures that each key's offset has the opposite sign to the previous key.
      
#### Reset
Sometimes you need to start over.
    
### Easy constraints

![capyanim_easyconstraints](https://user-images.githubusercontent.com/132166620/235326161-12295061-5acf-42b4-9968-8b44e467229f.png)

This window doesn't actually add new functionnalities to Maya; it's purpose is to gather existing tools to the same place (I enjoy doing less clicks). As a result, most buttons are self-explanatory.

Notable stuff :
 - 'Bake transforms' appplies a match transform for each frame in the timerange.
 - Constraints are applied to all objects selected after the first, with the first object acting as the parent.
 - Match transforms are applied to all selected objects, with the last object selected acting as the target.
 - 'Remove' deletes all constraints applied to the selected object.
 
 
 
 # Capyrig
 
 
 ### Quick rig
 
 #### Misc
 
   - 'NPO' adds a neutral parent to the selected object (zero-out his transforms by giving them to a group and parenting it to it).
   
   - 'Super cluster' creates a cluster whose group can be moved without causing deformations.
   
 For both of these tools, the text field overrides the default name of the npo / cluster if it is not empty.
 
 #### Joints
 
  - 'Delete orients' sets the orients of the selected joint to 0.
  
  - ' Convert rotates' transfers the selected joint's rotation into its orients.
  
 #### Controls
 
  - 'Mirror' creates a symmetrized copy of the selected controller and its childrens, with inverted behavior. It aut-replaces "L" with "R" in the name, and vice-versa.
  
  - 'Color override' is a faster way to change the color of the color of a controller (with infinite choices compared to indexes).
      > I found the code for this one elsewhere, but did the UI
 
 
 ### Gym
 A quick way to setup controller/bone animation for skinning.
 
 'Value' is the angle between each key, whereas 'Frame skip' is the size of the inbetween.
 
 The reset tab makes it quick to delete the animation once finished.
 
 
 ### Better wire
 
 The default wire deformer is great to start a facial blendshape, but isn't very intuitive and needs a lot of setup.
 
 The goal of this tool is to make wire deformers a lot more efficient.
 
  - Select continuous edges from a mesh,
  
  - Click new wire to add a wire deformer (with a custom name if you want to).
    > The list of wire deformers existing in the scene will auto-update.

Other tools act on the wire currently displayed from the list:

  - 'Select control' selects the defroming curve
  
  - 'Select node' gives a quick access the deformers' settings
  
  - 'Droppoff' is linked to the dropoff slider in the node.
  
  - 'Weight' is the amount of deformation applied.
  
    > It is usefull to switch back to original pose, to ensure the deformation is correct.
    
  - 'Auto-update': If you create, modify, or delete wires without using the tool, the list won't auto-update, hence this button.
  
  - 'Delete current wire' deletes the current wire and removes it from the list.
  
 
 ### Easy constraints
 
 This window is exactly the same as the one from [CapyAnim](#easy-constraints); constraints are useful in rigging aswell.
