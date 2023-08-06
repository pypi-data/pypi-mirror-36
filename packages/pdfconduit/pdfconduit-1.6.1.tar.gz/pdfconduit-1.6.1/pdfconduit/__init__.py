__all__ = []


# Conduit installation
try:
    from pdf.conduit import Encrypt, Merge, Watermark, Label, WatermarkAdd
    CONDUIT_INSTALL = True
    __all__.extend(["Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd"])
except ImportError:
    CONDUIT_INSTALL = False


# Utils installation
try:
    from pdf.utils.info import Info
    UTILS_INSTALL = True
    __all__.extend(["Info"])
except ImportError:
    UTILS_INSTALL = False


# GUI installation
try:
    from pdf.gui.gui import GUI
    GUI_INSTALLED = True
    __all__.extend(["GUI"])
except ImportError:
    GUI_INSTALLED = False


# Modify installation
try:
    from pdf.modify import upscale, rotate, slicer
    MODIFY_INSTALLED = True
    __all__.extend(["slicer", "upscale", "rotate"])
except ImportError:
    MODIFY_INSTALLED = False


# Convert installation
try:
    from pdf.convert.flatten import Flatten
    MODIFY_INSTALLED = True
    __all__.extend(["Flatten"])
except ImportError:
    MODIFY_INSTALLED = False
