import maya.cmds as cmds

def set_curve_color(transform_name, index=None, rgb=None):
    shapes = cmds.listRelatives(transform_name, shapes=True, fullPath=True) or []
    if not shapes:
        raise RuntimeError(f"No shape found for '{transform_name}'")
    shape = shapes[0]
    cmds.setAttr(shape + '.overrideEnabled', 1)
    if rgb is not None:
        r,g,b = rgb
        cmds.setAttr(shape + '.overrideRGBColors', 1)
        cmds.setAttr(shape + '.overrideColorRGB', r, g, b, type='double3')
    elif index is not None:
        cmds.setAttr(shape + '.overrideRGBColors', 0)
        cmds.setAttr(shape + '.overrideColor', int(index))
    else:
        raise ValueError("Provide either an index (0-31) or rgb=(r,g,b)")

set_curve_color('head_ctrl', index=13)
set_curve_color('head_ctrl', rgb=(1.0, 0.2, 0.2))