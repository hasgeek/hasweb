from flask.ext.wtf import Form, FileField


class ProfileImageForm(Form):
    """Form to upload profile images"""

    image_file = FileField(u'Profile Picture')
