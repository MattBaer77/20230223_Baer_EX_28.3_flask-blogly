
def add_default_user_image(user):
    if not user.img_url or user.img_url == '/default.png':
        user.img_url = "{{url_for('static', filename='default.png')}}"

def replace_user_values_empty_with_null(user):
    if user.first_name == '' or user.first_name == 'None':
        user.first_name = None
    if user.last_name == '' or user.last_name == 'None':
        user.last_name = None
    if user.img_url == '' or user.img_url == 'None':
        user.img_url = None
