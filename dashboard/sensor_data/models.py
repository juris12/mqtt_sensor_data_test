from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SensorCategory(models.Model):
    SENSOR_TYPES = [
        ('ENVIRONMENT', 'Environmental Sensor'),
        ('METER', 'Consumption Meter'),
        ('EQUIPMENT', 'Climate Equipment / PLC'),
    ]
    name = models.CharField(max_length=255)  # 'temperature', 'power_consumption'
    sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPES)  # 'ENVIRONMENT', 'METER'
    
    def __str__(self):
        return f"{self.name} ({self.get_sensor_type_display()})"

class Sensor(models.Model):
    name = models.CharField(max_length=255)
    sensor_category = models.ForeignKey(SensorCategory, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturer = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.serial_number}" if self.serial_number else self.name

class DataField(models.Model):
    DATA_TYPES = [
        ('FLOAT', 'Float'),
        ('INT', 'Integer'),
        ('STR', 'String'),
        ('BOOL', 'Boolean'),
    ]
    
    name = models.CharField(max_length=100)  # 'temperature', 'power_consumption'
    field_type = models.CharField(max_length=10, choices=DATA_TYPES)
    unit = models.CharField(max_length=20, blank=True)
    sensor_category = models.ForeignKey(SensorCategory, on_delete=models.CASCADE, related_name='data_fields')
    
    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()}) - {self.sensor_category.name}"

class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField()
    def __str__(self):
        return f"{self.sensor.name} @ {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', 'timestamp']),
        ]

class Measurement(models.Model):
    reading = models.ForeignKey(SensorReading, on_delete=models.CASCADE, related_name='measurements')
    field = models.ForeignKey(DataField, on_delete=models.CASCADE)
    
    float_value = models.FloatField(null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)
    str_value = models.CharField(max_length=255, null=True, blank=True)
    bool_value = models.BooleanField(null=True, blank=True)
    
    class Meta:
        unique_together = ('reading', 'field')
        verbose_name = 'Sensor Measurement'
        verbose_name_plural = 'Sensor Measurements'
    
    def __str__(self):
        return f"{self.reading.sensor.name} - {self.field.name} = {self.get_value()}"
    
    def get_value(self):
        """Returns the appropriate value based on field type"""
        if self.field.field_type == 'FLOAT':
            return self.float_value
        elif self.field.field_type == 'INT':
            return self.int_value
        elif self.field.field_type == 'STR':
            return self.str_value
        elif self.field.field_type == 'BOOL':
            return self.bool_value
        return None
    
    def set_value(self, value):
        """Sets the appropriate value based on field type"""
        if self.field.field_type == 'FLOAT':
            self.float_value = value
        elif self.field.field_type == 'INT':
            self.int_value = value
        elif self.field.field_type == 'STR':
            self.str_value = str(value)
        elif self.field.field_type == 'BOOL':
            self.bool_value = bool(value)