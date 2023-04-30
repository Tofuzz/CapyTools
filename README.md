# CapyTools
A compilation of maya python tools I built over last year to be more efficient :
  - CapyAnim, for animation
  - CapyRig, for rigging
  
![capytools_overview](https://user-images.githubusercontent.com/132166620/235354163-e75253ca-d692-477e-a5c4-c74c347b5d3a.png)


All submenus can be collapsed, allowing you to display only the tools that you really need.
___

[Capyanim](#capyanim)

  - [Quick anim](#1-quick-anim)
    - [Quick spline](#quick-spline)
    - [Motion curves](#motion-curves)
    - [Offet machine](#offset-machine)
    - [Noise machine](#noise-machine)
    - [Reset](#reset)
  - [Easy constraints](#2-easy-constraints)
  
 [Capyrig](#capyrig)
 
  - [Quick rig](#1-quick-rig)
  - [Gym](#2-gym)
  - [Better wire](#3-better-wire)
  - [Easy constraints](#4-easy-constraints)

___


# Capyanim


### 1. Quick anim

#### Quick spline
To keep the graph editor clean, by quickly deleting useless information.
  
![capyanim_lesscurves_lesskeys](https://github.com/Tofuzz/CapyHost/blob/main/capyanim_lesscurves_lesskeys.gif)

  - 'Less curves' removes curves that do not contain animation.
  - 'Less keys' removes inbetween keys that do not modify the channel's values
  

#### Motion curves
Creates motion trails that doesn't stop maya from working properly. They are just Nurb curves with Locators marking each keyframes, which makes them very lightweight.

![capyanim_motiontrails](https://user-images.githubusercontent.com/132166620/235355452-6dc1d05e-15c7-498d-9ece-0f1e1d38d2ba.png)

- Step curve

![capyanim_stepcurves](https://github.com/Tofuzz/CapyHost/blob/main/step_curve.gif)


- Spline curve

![capyanim_spline_curves](https://github.com/Tofuzz/CapyHost/blob/main/capyanim_splinecurves.gif)

      
#### Offset machine
Move selected keys with precision.

![capyanim_offsetmachine](https://user-images.githubusercontent.com/132166620/235355463-3d0efef3-0140-4b06-a44d-222d1925048b.png)
      
#### Noise machine
Offset the selected keys by a random value. 'Alternate' ensures that each key's offset has the opposite sign to the previous key.

![capyanim_noisemachine](https://user-images.githubusercontent.com/132166620/235363956-72f783ac-a2a1-4225-897c-c85216cc7594.gif)


#### Reset
Sometimes you need to start over.

![capyanim_reset](https://user-images.githubusercontent.com/132166620/235355501-fac7453c-9472-4251-a25b-7dee9dc522f4.png)
    
### 2. Easy constraints

![capyanim_easyconstraints](https://user-images.githubusercontent.com/132166620/235326161-12295061-5acf-42b4-9968-8b44e467229f.png)

This window doesn't actually add new functionnalities to Maya; it's purpose is to gather existing tools to the same place (I enjoy doing less clicks). As a result, most buttons are self-explanatory.

Notable stuff :
 - 'Bake transforms' appplies a match transform for each frame in the timerange.
 - Constraints are applied to all objects selected after the first, with the first object acting as the parent.
 - Match transforms are applied to all selected objects, with the last object selected acting as the target.
 - 'Remove' deletes all constraints applied to the selected object.
 
 
 
 # Capyrig
 
 
 ### 1. Quick rig
 
 #### Misc
 
 ![capyrig_misc](https://user-images.githubusercontent.com/132166620/235356299-cd5f9bee-b0a8-4303-9231-3d37980e2725.png)
 
   - 'NPO' adds a neutral parent to the selected object (zero-out his transforms by giving them to a group and parenting it to it).
   
   - 'Super cluster' creates a cluster whose group can be moved without causing deformations.
   
   ![capyrig_supercluster](https://github.com/Tofuzz/CapyHost/blob/main/supercluster.gif)


 For both of these tools, the text field overrides the default name of the npo / cluster if it is not empty.
 
 #### Joints
 
 ![capyrig_joints](https://user-images.githubusercontent.com/132166620/235356303-b69182c1-61c8-4fb2-b350-26d470259bf1.png)

  - 'Delete orients' sets the orients of the selected joint to 0.
  
  - ' Convert rotates' transfers the selected joint's rotation into its orients.
  
 #### Controls
 
 ![capyrig_controls](https://user-images.githubusercontent.com/132166620/235356317-0d311b56-fd1e-4d95-8cc5-9161d47be4ee.png)
 
  - 'Mirror' creates a symmetrized copy of the selected controller and its childrens, with inverted behavior. It auto-replaces "L" with "R" in the name, and vice-versa.
  
  ![capyrig_mirror](https://github.com/Tofuzz/CapyHost/blob/main/mirror.gif)
 
  - 'Color override' is a faster way to change the color of the color of a controller (with infinite choices compared to indexes).
      > I found the code for this one elsewhere, but did the UI
 
 
 ### 2. Gym
 A quick way to setup controller/bone animation for skinning.
  
 ![capyrig_gym](https://github.com/Tofuzz/CapyHost/blob/main/capyrig_gym.gif)
 
  - 'Value' is the angle between each key
  - 'Frame skip' is the size of the inbetween.
  - The 'Reset' tab makes it quick to delete the animation once finished.
 
 
 ### 3. Better wire
 
 The default wire deformer is great to start a facial blendshape, but isn't very intuitive and needs a lot of setup.
 
 The goal of this tool is to make wire deformers a lot more efficient.
  
  - Select continuous edges from a mesh,
  
  - Click new wire to add a wire deformer (with a custom name if you want to).
    > The list of wire deformers existing in the scene will auto-update.

![capyrig_betterwire](https://github.com/Tofuzz/CapyHost/blob/main/capyrig_wire.gif)

Other tools act on the wire currently displayed from the list:

  - 'Select control' selects the defroming curve
  
  - 'Select node' gives a quick access the deformers' settings
  
  - 'Droppoff' is linked to the dropoff slider in the node.
  
  - 'Weight' is the amount of deformation applied.
  
    > It canb be usefull to switch back to original pose, to ensure the deformation is correct.
    
  - 'Auto-update': If you create, modify, or delete wires without using the tool, the list won't auto-update, hence this button.
  
  - 'Delete current wire' deletes the current wire and removes it from the list.
  
 
 ### 4. Easy constraints
 
 This window is exactly the same as the one from [CapyAnim](#easy-constraints); constraints are useful in rigging aswell.
