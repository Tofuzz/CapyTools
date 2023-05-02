import maya.cmds as mc
import pymel.core as pm
import re
import matrix_freeze
import capyfuncs

import importlib
importlib.reload(capyfuncs)
importlib.reload(matrix_freeze)

default_attributes = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
dark_grey = 3*[0.19]


def reset_orient_joint(*args):
    selection = mc.ls(sl=True)
    for joint in selection:
        joint_orients_attr = ["jointOrientX", "jointOrientY", "jointOrientZ"]
        for attribute in joint_orients_attr:
            mc.setAttr("%s.%s" % (joint, attribute), 0)


def rotates_to_orient(*args):
    selection = mc.ls(sl=True)
    for joint in selection:
        rot_attr = ["rotateX", "rotateY", "rotateZ"]
        orient_attr = ["jointOrientX", "jointOrientY", "jointOrientZ"]
        for i in range(len(rot_attr)):
            mc.select(joint)

            rot_value = mc.getAttr("%s.%s" % (joint, rot_attr[i]))
            orient_value = mc.getAttr("%s.%s" % (joint, orient_attr[i]))
            mc.setAttr("%s.%s" % (joint, rot_attr[i]), 0)
            mc.setAttr("%s.%s" % (joint, orient_attr[i]), orient_value + rot_value)


def override_color(target, color=(1, 1, 1)):
    rgb = ("R", "G", "B")

    mc.setAttr(target + ".overrideEnabled", 1)
    mc.setAttr(target + ".overrideRGBColors", 1)

    for channel, color in zip(rgb, color):
        mc.setAttr(target + ".overrideColor%s" % channel, color)


def get_enum_name(options_list):
    enum_name = options_list[0]
    for i in range(len(options_list)-1):
        enum_name = "%s:%s" % (enum_name, options_list[i+1])

    return enum_name


def add_parent_switch(target, parents, dv):
    mc.select(target)

    if not mc.objExists("%s_npo" % target):
        npo = capyfuncs.add_npo()

    if not mc.objExists("%s._______" % target):
        mc.addAttr(at="enum", sn="________", en="_________", k=True)

    parent_attr = "parent"
    enum_name = get_enum_name(parents)
    mc.addAttr(at="enum", sn=parent_attr, nn="Parent", k=True, en=enum_name)
    mc.setAttr("%s.%s" % (target, parent_attr), dv)

    constraint = mc.parentConstraint(parents, npo, mo=True)[0]

    for i in range(len(parents)):
        for y in range(len(parents)):
            constraint_attr = "%sW%s" % (parents[y], y)
            if y == i:
                mc.setDrivenKeyframe("%s.%s" % (constraint, constraint_attr), cd="%s.%s" % (target, parent_attr), dv=i, v=1)
            else:
                mc.setDrivenKeyframe("%s.%s" % (constraint, constraint_attr), cd="%s.%s" % (target, parent_attr),dv=i, v=0)


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


def separate_parent_from_children():
    selection = mc.ls(sl=True)
    parent = selection[0]
    children = []
    for i in range(len(selection) - 1):
        children.append(selection[i + 1])

    return parent, children


def gym(*args):
    selection = mc.ls(sl=True)
    angle = 60

    for controller in selection:
        mc.setKeyframe(controller, at="rotateY", t=0, v=0)
        mc.setKeyframe(controller, at="rotateY", t=3, v=-angle)
        mc.setKeyframe(controller, at="rotateY", t=6, v=angle)
        mc.setKeyframe(controller, at="rotateY", t=9, v=0)

        mc.setKeyframe(controller, at="rotateZ", t=9, v=0)
        mc.setKeyframe(controller, at="rotateZ", t=12, v=-angle)
        mc.setKeyframe(controller, at="rotateZ", t=15, v=angle)
        mc.setKeyframe(controller, at="rotateZ", t=18, v=0)


def delete_keys(*args):
    selection = mc.ls(sl=True)
    for controller in selection:
        mc.cutKey(controller, time=(1, 1000), cl=True)  # To reset position to first key
        mc.cutKey(controller, cl=True)


def go_to_first_frame(*args):
    mc.currentTime(0)


def orient_joints(*args):
    init_selection = mc.ls(sl=True)

    mc.select(init_selection[0])
    mc.joint(edit=True, oj="xyz", sao="yup", ch=True, zso=True)
    end_joints = capyfuncs.sort_last_in_hierarchy()
    mc.select(end_joints)
    mc.joint(edit=True, oj="none")

    mc.select(init_selection)


class CapyRig:
    def __init__(self):
        window_name = "CapyRig"
        if mc.window(window_name, exists=True):
            mc.deleteUI(window_name, window=True)

        self.window = mc.window(window_name, iconName='CapyRig')
        mc.tabLayout()

        # Misc
        mc.columnLayout("Quick Rig", adj=True, rs=10)
        mc.separator(style="none", h=2)


        mc.frameLayout(l="Misc", cll=1, bgc=dark_grey)

        form = mc.formLayout()

        rl1 = mc.rowLayout(nc=2, adj=1)
        self.npo_field = mc.textField()
        mc.button(w=80, l="NPO", command=self.add_npo)
        mc.setParent('..')

        rl2 = mc.rowLayout(nc=2, adj=1)
        self.txt_super_cluster = mc.textField()
        mc.button(w=80, l="Super cluster", command=self.super_cluster)
        mc.setParent('..')

        mc.formLayout(form, e=1,
                      attachForm=[
                          (rl1, "top", 5),
                          (rl1, "left", 5),
                          (rl2, "left", 5),
                      ],
                      attachControl=[
                          (rl2, "top", 5, rl1),
                      ],
                      attachPosition=[
                          (rl1, 'right', 5, 100),
                          (rl2, 'right', 5, 100),
                      ]
                      )

        mc.setParent('..')

        mc.setParent('..')


        mc.separator()
        mc.frameLayout(l="Joints", cll=1, bgc=dark_grey)

        form = mc.formLayout()
        b1 = mc.button(l="Delete orients", command=reset_orient_joint)
        b2 = mc.button(l="Convert rotates", command=rotates_to_orient)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (b1, "top", 5),
                          (b1, "left", 5),
                          (b2, "top", 5),
                          (b2, "right", 5),
                      ],
                      attachControl=[
                          (b2, "left", 5, b1),
                      ],
                      attachPosition=[
                          (b1, 'right', 5, 50),
                      ]
                      )
        mc.setParent('..')

        mc.setParent('..')


        mc.separator()
        mc.frameLayout(l="Controls", cll=1, bgc=dark_grey)

        form = mc.formLayout()


        b1 = mc.button(l="Mirror", command=self.mirror_controls)

        rl1 = mc.rowLayout(nc=2, ad2=1)
        self.color_picker = mc.colorSliderGrp()
        mc.button(l="Color override", command=self.override_color)
        mc.setParent('..')

        mc.formLayout(form, e=1,
                      attachForm=[
                          (b1, "top", 5),
                          (b1, "left", 5),
                          (rl1, "left", 5),
                      ],
                      attachControl=[
                          (rl1, "top", 5, b1),
                      ],
                      attachPosition=[
                          (b1, 'right', 5, 100),
                          (rl1, 'right', 5, 100),
                      ]
                      )
        mc.setParent('..')

        mc.setParent('..')


        mc.setParent('..')

        # GYM
        mc.columnLayout("Gym", adj=True, rs=10)
        mc.separator(h=2, style="none")

        mc.columnLayout(adj=True, rs=5)
        mc.rowLayout(nc=2)
        self.gym_box_t = mc.checkBox(l="Translate", v=0)
        self.gym_box_r = mc.checkBox(l="Rotate", v=1)
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.text(l="Value :")
        self.gym_value = mc.textField(tx=60, w=30)
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.text(l="Frame skip :")
        self.gym_skip = mc.textField(tx=10, w=30)
        mc.setParent('..')
        mc.rowLayout(nc=3)
        self.gym_box_x = mc.checkBox(l="X   ", v=1)
        self.gym_box_y = mc.checkBox(l="Y   ", v=1)
        self.gym_box_z = mc.checkBox(l="Z   ", v=1)
        mc.setParent('..')
        mc.setParent('..')
        mc.button(l="Gym", command=self.gym)

        mc.separator()
        mc.frameLayout(l="Reset", cll=1, cl=True, bgc=dark_grey)
        self.box_reset_keys = mc.checkBox(l="Delete all keys  ", v=1)
        self.box_reset_transforms = mc.checkBox(l="Reset transforms  ", v=1)
        self.box_reset_first_frame = mc.checkBox(l="First frame  ", v=1)
        mc.button(l="Reset", command=self.reset)
        mc.setParent('..')
        mc.setParent('..')


        # BETTER WIRE
        mc.columnLayout("Better wire", adj=True, rs=5)
        mc.separator(style="none", h=15)

        self.wires_list = mc.optionMenu(l="Wires")
        self.update_wire_list(self.wires_list, "_wire_grp")

        mc.rowLayout(nc=2, adj=1)
        self.group_name = mc.textField()
        mc.button(w=80, l="New wire", command=self.create_new_wire)
        mc.setParent('..')

        mc.separator(h=10)
        form = mc.formLayout()
        b1 = mc.button(l="Select control", command=self.select_wire_control)
        b2 = mc.button(l="Select node", command=self.select_wire_node)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (b1, "top", 5),
                          (b1, "left", 5),
                          (b2, "top", 5),
                          (b2, "right", 5),
                      ],
                      attachControl=[
                          (b2, "left", 5, b1),
                      ],
                      attachPosition=[
                          (b1, 'right', 5, 50),
                      ]
                      )
        mc.setParent('..')

        mc.separator(h=10)
        mc.rowLayout(nc=2, adj=True)
        self.slider_dropoff = mc.floatSliderGrp(
            cw=[1, 50], field=True, v=1, min=0, max=10, fmx=100, dc=self.update_wire_dropoff)
        mc.button(l="Dropoff", w=80, command=self.update_wire_dropoff)
        mc.setParent('..')

        mc.rowLayout(nc=2, adj=True)
        self.slider_bs_weight = mc.floatSliderGrp(
            cw=[1, 50], field=True, v=1, min=0, max=1, dc=self.update_wire_bs_weight)
        mc.button(l="Weight", w=80, command=self.delete_wire)
        mc.setParent('..')

        mc.separator(h=10)
        mc.button(l="Update list", w=80, command=pm.Callback(self.update_wire_list, self.wires_list, "_wire_grp"))
        mc.button(l="Delete current wire", w=80, command=self.delete_wire)

        mc.setParent('..')

        mc.setParent('..')


        # EASY CONSTRAINTS
        mc.columnLayout("Easy constraints", adj=True, rs=10)
        mc.separator(style="none", h=2)

        mc.frameLayout(l="Quick Locator", cll=1, cl=True, bgc=dark_grey)
        form = mc.formLayout()
        self.loc_scale_slider = mc.intSliderGrp(
            f=True, min=1, max=10, fieldMaxValue=100, v=5)
        b1 = mc.button(l="Locator to selection", command=capyfuncs.locator_to_selection)
        s2 = self.loc_scale_slider
        b2 = mc.button(l="Set scale", w=80, command=self.set_locator_scale)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (b1, "top", 5),
                          (b1, "left", 5),
                          (b2, "right", 5),
                      ],
                      attachControl=[
                          (b2, "top", 5, b1),
                          (s2, "top", 5, b1),

                          (s2, "right", 5, b2),
                      ],
                      attachPosition=[
                          (b1, 'right', 5, 100),
                          (s2, 'left', 5, 0),
                      ]
                      )
        mc.setParent('..')
        mc.setParent('..')


        mc.separator()
        mc.frameLayout(l="Match transforms", cll=1, bgc=dark_grey)
        mc.rowLayout(nc=4)
        self.box_match_all = mc.checkBox(l="All     ", v=1,
                                         ofc=self.enable_match_boxes,
                                         onc=self.disable_match_boxes)
        self.box_match_t = mc.checkBox(l="T  ", v=1, ed=False)
        self.box_match_r = mc.checkBox(l="R  ", v=1, ed=False)
        self.box_match_s = mc.checkBox(l="S  ", v=0, ed=False)
        mc.setParent('..')
        mc.button(l="Match transforms", command=self.match_transform)
        mc.button(l="Bake transforms", command=self.bake_transforms)
        mc.setParent('..')

        mc.separator()
        mc.frameLayout(l="Constraints", cll=1, bgc=dark_grey)
        self.box_constraints_mo = mc.checkBox(l="Maintain offset", v=1)
        form = mc.formLayout()
        b1 = mc.button(l="Parent", w=80, command=self.parent_constraint)
        b2 = mc.button(l="Point", w=80, command=self.point_constraint)
        b3 = mc.button(l="Orient", w=80, command=self.orient_constraint)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (b1, "top", 5),
                          (b1, "left", 5),
                          (b2, "left", 5),
                          (b3, "right", 5),
                      ],
                      attachControl=[
                          (b2, "top", 5, b1),
                          (b3, "top", 5, b1),
                          (b3, "left", 5, b2),
                      ],
                      attachPosition=[
                          (b1, 'right', 5, 100),
                          (b2, 'right', 5, 50),
                          (b3, "right", 5, 100),
                      ]
                      )
        mc.setParent('..')
        mc.separator()
        mc.button(l="Delete from object", w=80, command=capyfuncs.remove_constraints)
        mc.setParent('..')
        mc.setParent('..')

        mc.setParent('..')

        mc.showWindow(window_name)

    def add_npo(self, *args):
        init_sel = mc.ls(sl=True)
        group_name = mc.textField(self.npo_field, q=True, tx=True)

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

            # mc.select(init_sel)
            # matrix_freeze.run()
            mc.select(group)
            # matrix_freeze.run()

    def override_color(self, *args):
        color = mc.colorSliderGrp(self.color_picker, q=True, rgb=True)
        color = (color[0], color[1], color[2])

        selection = mc.ls(sl=True)
        for target in selection:
            override_color(target, color)

    def mirror_controls(self, *args):
        target = mc.ls(sl=True)[0]

        old = "L"
        new = "R"
        if "R" in target:
            old = "R"
            new = "L"

        dupli = mc.duplicate(target, n=target.replace(old, new), rc=True)[0]
        parent = mc.listRelatives(dupli, ap=True, type="transform") or []
        children = mc.listRelatives(dupli, ad=True, typ="transform") or []
        for child in children:
            mc.rename(child, child.replace(old, new)[:-1])

        group = mc.group(em=True)
        mc.parent(dupli, group)
        mc.setAttr("%s.sx" % group, -1)
        mc.parent(dupli, parent)
        mc.delete(group)

    def gym(self, *args):
        selection = mc.ls(sl=True)
        value = int(mc.textField(self.gym_value, q=True, tx=True))
        time = mc.currentTime(q=True)
        skip = int(mc.textField(self.gym_skip, q=True, tx=True))

        transforms = []
        axes = []
        attributes = []

        if mc.checkBox(self.gym_box_t, q=True, v=1):
            transforms.append("translate")
        if mc.checkBox(self.gym_box_r, q=True, v=1):
            transforms.append("rotate")

        if mc.checkBox(self.gym_box_x, q=True, v=1):
            axes.append("X")
        if mc.checkBox(self.gym_box_y, q=True, v=1):
            axes.append("Y")
        if mc.checkBox(self.gym_box_z, q=True, v=1):
            axes.append("Z")

        for transform in transforms:
            for axis in axes:
                attributes.append(transform + axis)

        for controller in selection:
            for attribute in attributes:
                mc.setKeyframe(controller, at=attribute, t=time, v=0)
                time += skip
                mc.setKeyframe(controller, at=attribute, t=time, v=value)
                time += skip
                mc.setKeyframe(controller, at=attribute, t=time, v=-value)
                time += skip
                mc.setKeyframe(controller, at=attribute, t=time, v=0)

    def reset(self, *args):
        c1_on = mc.checkBox(self.box_reset_keys, q=True, v=True)
        c2_on = mc.checkBox(self.box_reset_transforms, q=True, v=True)
        c3_on = mc.checkBox(self.box_reset_first_frame, q=True, v=True)

        if c1_on:
            capyfuncs.delete_keys()
        if c2_on:
            capyfuncs.reset_selected()
        if c3_on:
            capyfuncs.go_to_first_frame()

    def super_cluster(self, *args):
        input_name = mc.textField(self.txt_super_cluster, q=True, tx=True)
        selection = mc.ls(sl=True)
        obj = re.split(".vtx", selection[0], 1)[0]
        if input_name == "":
            input_name = "%s_superCluster" % obj
        cluster = mc.cluster(n=input_name)

        handle = cluster[1]
        cluster = cluster[0]
        mc.connectAttr("%s.parentInverseMatrix[0]" % handle, "%s.bindPreMatrix" % cluster, f=True)

        group = mc.group(n="%s_grp" % cluster, em=True)
        mc.matchTransform(group, handle)
        mc.makeIdentity(group, apply=True, t=1, r=1, s=1, n=0)      #  == Freeze transforms
        mc.parent(handle, group)

    def set_locator_scale(self, *args):
        scale = mc.intSliderGrp(self.loc_scale_slider, q=True, v=True)
        locators = mc.ls(sl=True)
        for locator in locators:
            for axis in ["X", "Y", "Z"]:
                mc.setAttr("%s.localScale%s" % (locator, axis), scale)

    def match_transform(self, *args):
        sources, target = capyfuncs.isolate_last_selected()
        all_ = mc.checkBox(self.box_match_all, q=True, v=True)
        t = mc.checkBox(self.box_match_t, q=True, v=True)
        r = mc.checkBox(self.box_match_r, q=True, v=True)
        s = mc.checkBox(self.box_match_s, q=True, v=True)

        if all_:
            t = r = s = True

        for each in sources:
            mc.matchTransform(each, target, pos=t, rot=r, scl=s)

    def bake_transforms(self, *args):
        init_frame = mc.currentTime(q=True)
        start_frame, last_frame = capyfuncs.get_playback_range()

        frame = start_frame
        while frame < last_frame:
            mc.currentTime(frame)
            self.match_transform()
            frame += 1
        mc.currentTime(init_frame)

    def enable_match_boxes(self, *args):
        boxes = [self.box_match_t, self.box_match_r, self.box_match_s]
        for box in boxes:
            mc.checkBox(box, e=True, ed=True)

    def disable_match_boxes(self, *args):
        boxes = [self.box_match_t, self.box_match_r, self.box_match_s]
        for box in boxes:
            mc.checkBox(box, e=True, ed=False)

    def parent_constraint(self, *args):
        mo = mc.checkBox(self.box_constraints_mo, q=True, v=True)
        parent, children = capyfuncs.separate_parent_from_children()
        for each in children:
            mc.parentConstraint(parent, each, mo=mo)

    def point_constraint(self, *args):
        mo = mc.checkBox(self.box_constraints_mo, q=True, v=True)
        parent, children = capyfuncs.separate_parent_from_children()
        for each in children:
            mc.pointConstraint(parent, each, mo=mo)

    def orient_constraint(self, *args):
        mo = mc.checkBox(self.box_constraints_mo, q=True, v=True)
        parent, children = capyfuncs.separate_parent_from_children()
        for each in children:
            mc.orientConstraint(parent, each, mo=mo)

    def update_wire_list(self, optionmenu, string, *args):
        menu = mc.optionMenu(optionmenu, q=True, ils=True)
        if menu is None:
            menu = []

        scene = mc.ls("**%s" % string, typ="transform")
        if scene is None:
            scene = []

        print(menu)
        print(scene)

        for each in menu:
            if each not in scene:
                print("delete :", each)
                mc.deleteUI(each)

        for each in scene:
            if each not in menu:
                print("add :", each)
                mc.menuItem(each, parent=optionmenu)

    def create_new_wire(self, *args):
        selection = mc.ls(sl=True)
        text_input = mc.textField(self.group_name, q=True, tx=True)
        group = "%s_wire_grp" % text_input
        if text_input == "":
            group = "new_wire_grp"
        mc.group(n=group, em=True)
        self.update_wire_list(self.wires_list, "_wire_grp")
        mc.optionMenu(self.wires_list, e=True, v=group)

        mc.select(selection)
        mesh = re.split("\.", selection[0], 1)[0]
        curve = mc.polyToCurve(n=group.replace("_wire_grp", "_wire"), form=2, degree=3, conformToSmoothMeshPreview=1)[0]

        parent = mc.listRelatives(mesh, ap=True, typ="transform")
        mc.parent(group, parent)

        cvs_amount = mc.getAttr("%s.spans" % curve)
        mc.delete("%s.cv[1]" % curve)
        mc.delete("%s.cv[%s]" % (curve, cvs_amount))

        dupl = mc.duplicate(curve)[0]
        mc.delete(curve)
        curve = mc.rename(dupl, curve)


        mc.parent(curve, group)
        # mc.select(group)
        mc.wire(mesh, n=group.replace("grp", "def"), w=curve)[0]
        def_node = "%s_def" % self.get_current_wire()
        mc.setAttr("%s.rotation" % def_node, 0)

        control = mc.duplicate(curve, n=curve.replace("_wire", "_wire_ctrl"))
        bs = mc.blendShape(control, curve, n="%s_bs" % self.get_current_wire())[0]
        mc.setAttr("%s.%s" % (bs, control[0]), 1)

        mc.hide(curve)

    def delete_wire(self, *args):
        group = "%s_grp" % self.get_current_wire()
        mc.delete(group)
        self.update_wire_list(self.wires_list, "_wire_grp")

    def get_current_wire(self):
        current = mc.optionMenu(self.wires_list, q=True, v=True).replace("_grp", "")
        return current

    def select_wire_node(self, *args):
        mc.select("%s_def" % self.get_current_wire())

    def select_wire_control(self, *args):
        control = "%s_ctrl" % self.get_current_wire()
        mc.select(control)

    def update_wire_dropoff(self, *args):
        dropoff = mc.floatSliderGrp(self.slider_dropoff, q=True, v=True)
        def_node = "%s_def" % self.get_current_wire()
        mc.setAttr("%s.dropoffDistance[0]" % def_node, dropoff)

    def update_wire_bs_weight(self, *args):
        bs = "%s_bs" % self.get_current_wire()
        control = "%s_ctrl" % self.get_current_wire()
        weight = mc.floatSliderGrp(self.slider_bs_weight, q=True, v=True)

        mc.setAttr("%s.envelope" % bs, weight)



def launch():
    capyrig = CapyRig()
