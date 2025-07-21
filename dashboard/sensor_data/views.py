from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Building, Sensor, IndividualSensor, DataField, Measurement
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Case, When, IntegerField

@login_required
def building_list(request):
    query = request.GET.get('q')
    limit = int(request.GET.get('limit') or 60)

    if query:
        buildings = Building.objects.filter(name__icontains=query)[:limit]
    else:
        buildings = Building.objects.all()[:limit]

    return render(request, 'sensor_data/building_list.html', {
        'buildings': buildings,
        'num_rows': buildings.count()
    })

@login_required
def sensor_data_list(request, id):
    building = get_object_or_404(Building, id=id)
    sensors = IndividualSensor.objects.filter(building=building).prefetch_related(
        'readings__measurements__field'
    )
    
    sensor_data = []
    for ind_sensor in sensors:
        latest_reading = ind_sensor.readings.order_by('-timestamp').first()
        if latest_reading:
            if ind_sensor.sensor.sensor_category.sensor_type in ['ENVIRONMENT', 'METER']:
                # Get first measurement with value
                measurement = latest_reading.measurements.first()
                if measurement:
                    value_display = f"{measurement.field.name}: {measurement.get_value()}"
                else:
                    value_display = "No data"
            else:
                value_display = "N/A"
        else:
            value_display = "No readings"
        
        sensor_data.append({
            'sensor': ind_sensor,
            'value': value_display
        })
    
    return render(request, 'sensor_data/sensors_list.html', {
        'sensor_data': sensor_data,
        'building': building,
        'num_rows': len(sensor_data)
    })

@login_required
def building_names(request):
    search_text = request.GET.get('search_text', '')
    suggestions = Building.objects.annotate(
        starts_with=Case(
            When(name__istartswith=search_text, then=1),
            default=0,
            output_field=IntegerField(),
        )
    ).filter(name__icontains=search_text).order_by('-starts_with', 'name').values('name')[:10]
    suggestion_list = [entry['name'] for entry in suggestions]
    return JsonResponse(suggestion_list, safe=False)




@login_required
def sensor_detail(request, id):
    sensor = get_object_or_404(IndividualSensor, id=id)

    latest_reading = sensor.readings.order_by('-timestamp').first()
    measurements = []

    if latest_reading:
        for measurement in latest_reading.measurements.select_related('field'):
            measurements.append({
                'field_id': measurement.field.id,
                'field_name': measurement.field.name,
                'field_unit': measurement.field.unit,
                'value': measurement.get_value()
            })

    return render(request, 'sensor_data/sensor_detail.html', {
        'sensor': sensor,
        'building': sensor.building,
        'measurements': measurements,
        'timestamp': latest_reading.timestamp if latest_reading else None,
    })


@login_required
def sensor_field_detail(request, sensor_id, field_id):
    sensor = get_object_or_404(IndividualSensor, id=sensor_id)
    field = get_object_or_404(DataField, id=field_id)

    measurements = (Measurement.objects
        .filter(reading__individual_sensor=sensor, field=field)
        .select_related('reading')
        .order_by('-reading__timestamp')
    )[:10]

    records = [{
        'timestamp': m.reading.timestamp,
        'value': m.get_value()
    } for m in measurements]

    return render(request, 'sensor_data/sensor_field_detail.html', {
        'sensor': sensor,
        'field': field,
        'records': records,
    })
