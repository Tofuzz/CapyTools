import maya.cmds as mc

import capyfuncs
import random

import importlib
importlib.reload(capyfuncs)

default_attributes = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]

dark_grey = 3*[0.19]


def get_keyframes_values(node, attribute):
    key_values = mc.keyframe("%s.%s" % (node, attribute), q=True, vc=True)
    return key_values


def get_keyframes_times(node, attributes):
    all_attributes_keyframes_times = mc.keyframe(node, q=True, at=attributes)
    if all_attributes_keyframes_times is not None:
        combined_keyframe_times = []
        for time in all_attributes_keyframes_times:
            if time not in combined_keyframe_times:
                combined_keyframe_times.append(time)
        combined_keyframe_times.sort()
    else:
        combined_keyframe_times = None
    return combined_keyframe_times


def remove_unused_curves(*args):
    selection = mc.ls(sl=True)

    for node in selection:
        keyable_attributes = mc.listAttr(node, k=True)

        for attribute in keyable_attributes:
            key_values = get_keyframes_values(node, attribute)
            attribute_is_used = False

            if key_values is not None:
                i = 0
                while i < len(key_values):
                    if attribute_is_used:
                        break
                    if i > 0:
                        previous_value = key_values[i-1]
                        current_value = key_values[i]
                        if previous_value != current_value:
                            attribute_is_used = True
                    i += 1
                if not attribute_is_used:
                    mc.cutKey("%s.%s" % (node, attribute))

    mc.select(selection)


def remove_useless_keys(*args):
    precision = 0.01

    selection = mc.ls(sl=True)
    for node in selection:
        anim_curves = mc.keyframe(node, q=True, n=True)

        if anim_curves is None:
            mc.error("No anim curves found")
        for anim_curve in anim_curves:
            frames_to_delete = []
            key_frames = mc.keyframe(anim_curve, q=True)
            key_values = mc.keyframe(anim_curve, q=True, vc=True)

            for i in range(len(key_frames)-2):  # Avoids first
                i += 1                              # and last frame

                same_value_than_previous_frame = -precision < key_values[i] - key_values[i-1] < precision
                same_value_than_next_frame = -precision < key_values[i] - key_values[i+1] < precision

                if same_value_than_previous_frame and same_value_than_next_frame:
                    frames_to_delete.append(key_frames[i])
            for frame in frames_to_delete:
                mc.cutKey(anim_curve, t=(frame, frame))


def show_step_motion_curve(*args):
    print("init: step_motion_trail")
    selection = mc.ls(sl=True)

    local_scale = 3

    for node in selection:
        curve_points_positions = []
        key_times = mc.keyframe(q=True, tc=True) or []
        key_times = list(dict.fromkeys(key_times))  # Removes double keys (and sorts)
        key_times.sort()

        for time in key_times:
            world_matrix = mc.getAttr("%s.worldMatrix" % node, t=time)
            translates = [world_matrix[-4], world_matrix[-3], world_matrix[-2]]
            curve_points_positions.append(tuple(translates))

        motion_curve = mc.curve(n="%s_motion_curve" % node, p=curve_points_positions, d=1)

        for position in curve_points_positions:
            locator = mc.spaceLocator(n="%s_motion_loc" % node, p=position)[0]
            for axis in ["X", "Y", "Z"]:
                mc.setAttr("%s.localScale%s" % (locator, axis), local_scale)
            mc.parent(locator, motion_curve)

    mc.select(selection)


def show_spline_motion_curve(*args):
    print("init: spline_motion_trail")
    selection = mc.ls(sl=True)
    translate_attributes = ["translateX", "translateY", "translateZ"]

    local_scale = 3

    start_frame = mc.playbackOptions(q=True, min=True)
    end_frame = mc.playbackOptions(q=True, max=True)

    all_frames = []
    count = start_frame
    while count <= end_frame:
        all_frames.append(count)
        count += 1

    for node in selection:
        curve_points_positions = []
        for time in all_frames:
            world_matrix = mc.getAttr("%s.worldMatrix" % node, t=time)
            translates = [world_matrix[-4], world_matrix[-3], world_matrix[-2]]
            curve_points_positions.append(tuple(translates))

        locators_position = []
        key_times = mc.keyframe(q=True, tc=True) or []

        # key_times = get_keyframes_times(node, translate_attributes)
        # if key_times is not None:
        for time in key_times:
            world_matrix = mc.getAttr("%s.worldMatrix" % node, t=time)
            translates = [world_matrix[-4], world_matrix[-3], world_matrix[-2]]
            locators_position.append(tuple(translates))

        motion_curve = mc.curve(n="%s_motion_curve" % node, p=curve_points_positions, d=1)

        for position in locators_position:
            locator = mc.spaceLocator(n="%s_motion_loc" % node, p=position)[0]
            for axis in ["X", "Y", "Z"]:
                mc.setAttr("%s.localScale%s" % (locator, axis), local_scale)
            mc.parent(locator, motion_curve)
        # else:
        #     mc.error("Could not access translate attributes")

    mc.select(selection)


def reset_transforms_to_default(*args):
    selection = mc.ls(sl=True)
    for node in selection:
        mc.select(node)
        keyable_attributes = mc.listAttr(k=True, l=False)
        for attribute in keyable_attributes:
            default_value = mc.attributeQuery(attribute, n=node, listDefault=True)[0]
            mc.setAttr("%s.%s" % (node, attribute), default_value)
    mc.select(selection)

def show_attributes():
    selection = mc.ls(sl=True)
    for node in selection:
        for attribute in default_attributes:
            mc.setAttr("%s.%s" %(node, attribute), k=True)

def unlock_attributes():
    selection = mc.ls(sl=True)
    for node in selection:
        for attribute in default_attributes:
            mc.setAttr("%s.%s" %(node, attribute), lock=False)


def restore_default_attributes(*args):
    show_attributes()
    unlock_attributes()


def delete_keys(*args):
    selection = mc.ls(sl=True)
    for controller in selection:
        mc.cutKey(controller, time=(1, 1000), cl=True)  # To reset position to first key
        mc.cutKey(controller, cl=True)


def remove_doubles(*args):
    selection = mc.ls(sl=True)
    mc.selectKey(uk=True)
    mc.cutKey(sl=True)
    mc.select(selection)


def delete_motion_curves(*args):
    selection = mc.ls(sl=True)

    mc.select(mc.ls("***motion_curve*", r=True))
    if not mc.ls(sl=True):
        mc.error("No motion curves were found")
        mc.select(selection)
        return
    mc.delete()
    mc.select(selection)



class CapyAnim:
    def __init__(self):
        window_name = "CapyAnim"
        if mc.window(window_name, exists=True):
            mc.deleteUI(window_name, window=True)

        self.window = mc.window(window_name, iconName='CapyAnim')
        mc.tabLayout()

        # QUICK ANIM
        mc.columnLayout("Quick anim", adj=True, rs=10)
        mc.separator(style="none", h=2)

        mc.frameLayout(l="Quick spline", cll=1, bgc = dark_grey)
        form = mc.formLayout()
        b1 = mc.button(l="Less curves", command=remove_unused_curves)
        b2 = mc.button(l="Less keys", command=remove_useless_keys)
        mc.formLayout(form, e=1,
                attachForm = [
                    (b1, "left", 5),
                    (b1, "top", 5),
                    (b2, "top", 5),
                ],
				attachControl = [
					(b2, "left", 5, b1),
					],
                attachPosition = [
                    (b1, 'right', 5, 50),
                    (b2, 'right', 5, 100),
                    ]
                )
        mc.setParent('..')
        mc.setParent('..')

        mc.separator()
        mc.frameLayout(l="Motion curves (non-editables)", cll=1, bgc = dark_grey)
        form = mc.formLayout()
        b1 = mc.button(l="Step curve", command=show_step_motion_curve)
        b2 = mc.button(l="Spline curve", command=show_spline_motion_curve)
        b3 = mc.button(l="Delete motion curves", command=delete_motion_curves)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (b1, "left", 5),
                          (b1, "top", 5),
                          (b2, "top", 5),
                          (b3, "left", 5),
                      ],
                      attachControl=[
                          (b2, "left", 5, b1),
                          (b3, "top", 5, b1)
                      ],
                      attachPosition=[
                          (b1, 'right', 5, 50),
                          (b2, 'right', 5, 100),
                          (b3, "right", 5, 100)
                      ]
                      )
        mc.setParent('..')
        mc.setParent('..')

        mc.separator()
        mc.frameLayout(l="Offset Machine", cll=1, cl=True, bgc = dark_grey)
        form = mc.formLayout()
        s1 = self.offset_slider_value = mc.floatSliderGrp(
            f=True, min=-10, max=10, fieldMinValue=-500, fieldMaxValue=500, v=0)
        b1 = mc.button(l="Offset value", w=80, command=self.offset_keys_values)
        s2 = self.offset_slider_time = mc.intSliderGrp(
            f=True, min=-10, max=10, fieldMinValue=-500, fieldMaxValue=500, v=0)
        b2 = mc.button(l="Offset time", w=80, command=self.offset_keys_times)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (s1, "top", 5),
                          (b1, "right", 5),
                          (b2, "right", 5)
                      ],
                      attachControl=[
                          (s1, "right", 5, b1),
                          (b2, "top", 5, b1),
                          (s2, "right", 5, b2),
                          (s2, "top", 5, s1)
                      ],
                      attachPosition=[
                          (s1, 'left', 5, 0),
                          (s2, 'left', 5, 0),
                      ]
                      )
        mc.setParent('..')
        mc.setParent('..')

        mc.separator()
        mc.frameLayout(l="Noise Machine", cll=1, cl=True, bgc=dark_grey)
        self.box_noise_alternate = mc.checkBox(l="Alternate", v=1)
        form = mc.formLayout()
        s1 = self.random_value_slider = mc.floatSliderGrp(
            f=True, min=0, max=10, fieldMaxValue=500, v=0)
        b1 = mc.button(l="Noise", w=80, command=self.add_noise_value)
        mc.formLayout(form, e=1,
                      attachForm=[
                          (s1, "top", 5),
                          (b1, "right", 5),
                      ],
                      attachControl=[
                          (s1, "right", 5, b1),
                      ],
                      attachPosition=[
                          (s1, 'left', 5, 0),
                      ]
                      )
        mc.setParent('..')
        mc.setParent('..')

        mc.separator()
        mc.frameLayout(l="Reset", cll=1, cl=True, bgc=dark_grey)
        self.box_reset_keys = mc.checkBox(l="Delete all keys  ", v=0)
        self.box_reset_transforms = mc.checkBox(l="Reset transforms  ", v=1)
        self.box_reset_first_frame = mc.checkBox(l="First frame  ", v=0)
        mc.button(l="Reset", command=self.reset)
        mc.setParent('..')

        mc.setParent('..')

        # EASY CONSTRAINTS
        mc.columnLayout("Easy constraints", adj=True, rs=10)
        mc.separator(style="none", h=2)

        mc.frameLayout(l="Quick Locator", cll=1, bgc=dark_grey)
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
        mc.button(l="Remove", w=80, command=capyfuncs.remove_constraints)
        mc.setParent('..')
        mc.setParent('..')

        mc.setParent('..')

        mc.showWindow(window_name)

    def add_noise_value(self, *args):
        alternate = mc.checkBox(self.box_noise_alternate, q=True, v=True)
        selection = mc.ls(sl=True)

        for node in selection:
            anim_curves = mc.keyframe(node, q=True, sl=True, n=True)
            if anim_curves is None:
                mc.error("No keys selected")
            for anim_curve in anim_curves:
                frames = mc.keyframe(anim_curve, q=True, sl=True)
                if frames is not None:
                    alternate_mult = 1
                    for frame in frames:
                        max_offset = mc.floatSliderGrp(self.random_value_slider, q=True, v=True)
                        offset = random.uniform(-1, 1)
                        offset *= max_offset
                        if alternate:
                            offset = abs(offset)
                            offset *= alternate_mult
                            alternate_mult *= -1
                        mc.keyframe("%s" % anim_curve, e=True, r=True, vc=offset, t=(frame, frame))



    def offset_keys_values(self, *args):
        value_amount = mc.floatSliderGrp(self.offset_slider_value, q=True, v=True)
        mc.keyframe(e=True, r=True, vc=value_amount)

    def offset_keys_times(self, *args):
        time_amount = mc.intSliderGrp(self.offset_slider_time, q=True, v=True)
        mc.keyframe(e=True, r=True, tc=time_amount)


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


def launch():
    CapyAnim()
