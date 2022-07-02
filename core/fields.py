# from django.db.models import fields


# class PercentageField(fields.FloatField):
#     widget = fields.TextInput(attrs={"class": "percentInput"})

#     def to_python(self, value):
#         val = super(PercentageField, self).to_python(value)
#         if is_number(val):
#             return val/100
#         return val

#     def prepare_value(self, value):
#         val = super(PercentageField, self).prepare_value(value)
#         if is_number(val) and not isinstance(val, str):
#             return str((float(val)*100))
#         return val