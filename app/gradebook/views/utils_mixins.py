from django.views.generic.base import ContextMixin


class SectionIDMixin(ContextMixin):
    """
    This is for other Classes to inherit so that they can all have the section id needed
    to link back to the previous section's page. I use this for the Create/Update/List forms.
    """
    def get_context_data(self, **kwargs):
        context = super(SectionIDMixin, self).get_context_data(**kwargs)
        section_pk = self.kwargs['sec']
        context['current_section_pk'] = section_pk
        return context