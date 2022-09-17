from django import forms

class EOQform(forms.Form):
    demand_per_anum = forms.IntegerField(min_value=1)
    ordering_cost_per_order = forms.FloatField()
    holding_cost = forms.FloatField()

class MaximumStockLevelForm(forms.Form):
    reorder_level = forms.IntegerField(min_value=1)
    reorder_quantity = forms.IntegerField(help_text='also known as (EOQ)')
    minimum_usage_rate = forms.IntegerField()
    minimum_lead_time = forms.IntegerField(help_text='In days')

class ReorderLevelForm(forms.Form):
    maximum_lead_time = forms.IntegerField(min_value=1, help_text='In days')
    maximum_usage_rate = forms.IntegerField(min_value=1)


class MinimumStockLevelForm(forms.Form):
    reorder_level = forms.IntegerField(min_value=1)
    average_usage_rate = forms.IntegerField(min_value=1)
    average_lead_time = forms.IntegerField(min_value=1, help_text='In days')