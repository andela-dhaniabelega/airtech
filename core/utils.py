from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.http import Http404


class ExtendedEncoder(DjangoJSONEncoder):
    """
    Convert Django Model to JSON
    """
    def default(self, o):

        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)


def get_single_object(idx, obj_type):
    """
    Return a QuerySet object
    :param idx: Object ID
    :param obj_type: The Queryset Class
    :return: Queryset object
    """
    try:
        return obj_type.objects.get(id=idx)
    except obj_type.DoesNotExist:
        raise Http404