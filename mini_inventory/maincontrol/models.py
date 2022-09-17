from django.db import models


# Create your models here.

class Inventories(models.Model):
    METHODS = (
        ('LIFO', 'Last in first out (LIFO)'),
        ('FIFO', 'First in first out (FIFO)'),
        ('AVP', 'Simple average price method'),
    )
    name = models.CharField(max_length=80, help_text='Max length is 80')
    extra_notes = models.TextField(null=True, blank=True, help_text='Extra note about this stock')
    currently_managed = models.BooleanField(default=False)
    method_of_management = models.CharField(max_length=5, choices=METHODS, default='LIFO')

    def __str__(self):
        return self.name

class Transactions(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=15)
    inventory = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    
    #recievals
    quantity_recieved = models.PositiveIntegerField(blank=True, null=True)
    price_recieved = models.FloatField(blank=True, null=True)
    quantity_remaining = models.PositiveIntegerField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)

    #distributions
    quantity_sent_out = models.PositiveIntegerField(blank=True, null=True)
    price_sent_out = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    balance_quantity = models.PositiveIntegerField()
    balance_value = models.FloatField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return str(self.action)