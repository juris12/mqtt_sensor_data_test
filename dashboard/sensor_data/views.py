from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Building, Sensor, IndividualSensor
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