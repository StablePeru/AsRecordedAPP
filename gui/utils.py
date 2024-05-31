import os

def load_stylesheet(app, filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    css_path = os.path.join(script_dir, '..', 'resources', filename)
    with open(css_path, "r") as f:
        app.setStyleSheet(f.read())
