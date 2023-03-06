from .models import *


class DataMixin:
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 4
