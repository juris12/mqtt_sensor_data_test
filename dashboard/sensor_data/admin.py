from django.contrib import admin
from django import forms
from .models import Building, SensorCategory, Sensor, DataField, SensorReading, Measurement

class DataFieldForm(forms.ModelForm):
    class Meta:
        model = DataField
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        field_type = cleaned_data.get('field_type')
        sensor_category = cleaned_data.get('sensor_category')
        
        # Ensure field names are lowercase with underscores
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].lower().replace(' ', '_')
        
        return cleaned_data

class DataFieldInline(admin.TabularInline):
    model = DataField
    form = DataFieldForm
    extra = 1
    fields = ('name', 'field_type', 'unit')
    ordering = ('name',)

@admin.register(SensorCategory)
class SensorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sensor_type', 'data_field_count')
    list_filter = ('sensor_type',)
    search_fields = ('name',)
    inlines = [DataFieldInline]
    
    def data_field_count(self, obj):
        return obj.data_fields.count()
    data_field_count.short_description = 'Fields'

class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 1  # Changed from 0 to 1 to show at least one empty form
    fields = ('field', 'get_value_display', 'float_value', 'int_value', 'str_value', 'bool_value')
    readonly_fields = ('get_value_display',)
    
    def get_value_display(self, obj):
        return obj.get_value()
    get_value_display.short_description = 'Current Value'

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "field" and hasattr(self, 'parent_obj') and self.parent_obj:
            kwargs["queryset"] = DataField.objects.filter(
                sensor_category=self.parent_obj.sensor.sensor_category
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'timestamp', 'measurement_count')
    list_filter = ('sensor__sensor_category', 'timestamp')
    search_fields = ('sensor__name',)
    date_hierarchy = 'timestamp'
    inlines = [MeasurementInline]
    
    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)
    
    def measurement_count(self, obj):
        return obj.measurements.count()
    measurement_count.short_description = 'Measurements'

class SensorReadingInline(admin.StackedInline):
    model = SensorReading
    extra = 0
    fields = ['timestamp']
    readonly_fields = ('timestamp',)
    show_change_link = True

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'sensor_category', 'building', 'last_reading')
    list_filter = ('sensor_category', 'manufacturer', 'building')
    search_fields = ('name', 'serial_number', 'manufacturer')
    inlines = [SensorReadingInline]
    
    def last_reading(self, obj):
        last = obj.readings.order_by('-timestamp').first()
        return last.timestamp if last else None
    last_reading.short_description = 'Last Reading'
    last_reading.admin_order_field = 'readings__timestamp'

@admin.register(DataField)
class DataFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'unit', 'sensor_category')
    list_filter = ('field_type', 'sensor_category__sensor_type')
    search_fields = ('name', 'sensor_category__name')
    ordering = ('sensor_category', 'name')
    form = DataFieldForm

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('reading', 'field', 'value_display')
    list_filter = ('field__sensor_category', 'field')
    search_fields = ('reading__sensor__name', 'field__name')
    readonly_fields = ('reading', 'field')
    
    def value_display(self, obj):
        return obj.get_value()
    value_display.short_description = 'Value'

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'sensor_count')
    list_filter = ('user',)
    search_fields = ('name',)
    
    def sensor_count(self, obj):
        return obj.sensor_set.count()
    sensor_count.short_description = 'Sensors'