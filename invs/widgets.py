# This is used for datetimepicker
from django.forms import DateTimeInput

class JQueryDateTimePickerInput(DateTimeInput):
    template_name = 'invs/jquery_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'id_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        # attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        # attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        # print("CON:%s"%(context))
        # print(value)
        # xxx='2019/11/11 10:11:11'
        # return xxx
        return context

