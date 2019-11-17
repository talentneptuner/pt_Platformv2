import xadmin

from .models import Labelresult

class LabelResultAdmin(object):
    list_display = ['mid', 'img_name', 'task', 'label', 'tagger']
    list_filter = ['task', 'label', 'tagger', 'label__parent', 'time']
    readonly_fields = ['mid', 'img_name', 'txt', 'label', 'tagger', 'time']

    def queryset(self):
        qs = super(LabelResultAdmin, self).queryset()
        user = self.request.user
        if user.is_superuser == 1:
            return qs
        qs = qs.filter(task__creator=user)
        return qs

xadmin.site.register(Labelresult, LabelResultAdmin)
