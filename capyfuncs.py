import maya.cmds as mc
import matrix_freeze
import re
import pymel.core as pm

def isolate_first_selected(*args):
    selection = mc.ls(sl=True)
    first = selection[0]
    last = []
    for i in range(len(selection) - 1):
        last.append(selection[i + 1])

    return first, last


def isolate_last_selected(*args):
    selection = mc.ls(sl=True)
    last = selection[-1]
    first = []
    for i in range(len(selection) + 1):
        first.append(selection[i - 1])

    return first, last

def separate_parent_from_children():
    selection = mc.ls(sl=True)
    parent = selection[0]
    children = []
    for i in range(len(selection) - 1):
        children.append(selection[i + 1])

    return parent, children

def delete_keys(*args):
    selection = mc.ls(sl=True)
    for controller in selection:
        # mc.cutKey(controller, time=(1, 1000), cl=True)  # To reset position to first key
        mc.cutKey(controller, cl=True)
        pass

def get_playback_range(*args):
    start_frame = mc.playbackOptions(q=True, min=True)
    last_frame = mc.playbackOptions(q=True, max=True)
    return start_frame, last_frame


def go_to_first_frame(*args):
    first_frame = mc.playbackOptions(q=True, min=True)
    mc.currentTime(first_frame)


def locator_to_selection(*args):
    selection = mc.ls(sl=True)
    local_scale = 1
    for node in selection:
        locator = mc.spaceLocator(n="%s_loc" % node)[0]
        mc.matchTransform(locator, node, pos=True)
        mc.setAttr("%s.localScaleX" % locator, local_scale)
        mc.setAttr("%s.localScaleY" % locator, local_scale)
        mc.setAttr("%s.localScaleZ" % locator, local_scale)


def sort_last_in_hierarchy(*args):
    selection = mc.ls(sl=True)
    childless_nodes = []

    master = selection[0]
    children = mc.listRelatives(master, ad=True)
    for child in children:
        if mc.listRelatives(child, ad=True) is None:
            childless_nodes.append(child)

    return childless_nodes

def add_npo(group_name=""):
    init_sel = mc.ls(sl=True)

    for node in init_sel:
        parent = mc.listRelatives(node, ap=True, typ="transform")
        if parent is not None:
            mc.parent(w=True)
        else:
            pass

        if group_name == "":
            group_name = "%s_npo" % node

        group = mc.group(n=group_name, em=True)
        mc.matchTransform(group, node)
        mc.parent(node, group)

        if parent is not None:
            mc.parent(group, parent)
        else:
            pass

        mc.select(init_sel)
        matrix_freeze.run()
        mc.select(group)
        matrix_freeze.run()

    mc.select(init_sel)
    return group

def extract_faces(new_name=""):
    faces_to_extract_mesh = mc.ls(sl=True)
    mesh = re.split(".f", faces_to_extract_mesh[0], 1)[0]

    # Extract
    dupli = mc.duplicate(mesh)[0]

    faces_to_extract_dupli = []
    for face_range in faces_to_extract_mesh:
        faces_to_extract_dupli.append(face_range.replace(mesh, dupli))

    mc.select("%s.f[*]" % dupli)
    mc.select(faces_to_extract_dupli, d=True)
    mc.delete()

    # Rename
    if new_name == "":
        new_name = "%s_extract" % mesh
    dupli = mc.rename(dupli, new_name)

    mc.delete(dupli, ch=True)
    return dupli

def remove_constraints(*args):
    selection = mc.ls(sl=True)
    error_message = "No constraints found"
    constraints = []

    for node in selection:
        direct_children = mc.listRelatives(node, typ="transform")
        if direct_children is None:
            mc.error("%s : %s" % (node, error_message))
        else:
            for child in direct_children:
                if "Constraint" in child:
                    constraints.append(child)

    for each in constraints:
        mc.delete(each)

def reset_selected():
    tr_list = ['.tx','.ty','.tz','.rx','.ry','.rz']
    s_list = ['.sx','.sy','.sz']
    selection = pm.selected()

    # o is each object, x is each attribute
    for attr in [(o, x) for o in selection for x in tr_list]:
        try: pm.Attribute(attr[0] + attr[1]).set(0)
        except: pass
    for attr in [(o, x) for o in selection for x in s_list]:
        try: pm.Attribute(attr[0] + attr[1]).set(1)
        except: pass