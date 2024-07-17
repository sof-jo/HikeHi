from django.shortcuts import render
from .models import HikingTrail


def map_view(request):
    trails = HikingTrail.objects.all()
    context = {'trails': trails}
    return render(request, 'map.html', context)
