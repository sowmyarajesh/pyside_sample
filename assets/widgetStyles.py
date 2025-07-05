
def highlight_image_label(color="rgb(200,200,200)"):
    _style ="""
    QLabel {
        background-color:"""+color+""";
        }
    """
    return _style