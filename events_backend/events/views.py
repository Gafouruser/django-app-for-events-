from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event, Attendance
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EventForm


def list_events(request):
    events = Event.objects.all()
    return render(request, 'events/list_events.html', {'events': events})


def detail_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/detail_event.html', {'event': event})


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('events:list_events')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events:detail_event', args=(event_id,)))
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form, 'event': event})


def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        event.delete()
        return HttpResponseRedirect(reverse('events:list_events'))
    else:
        event = Event.objects.get(pk=event_id)
        return render(request, 'events/delete_event.html', {'event': event})


@login_required
def register_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        if event.available_seats > 0:
            if not request.user.attended_events.filter(pk=event_id).exists():
                Attendance.objects.create(event=event, attendee=request.user)
                event.available_seats -= 1
                event.save()
                messages.success(request, 'Vous avez été inscrit à l\'événement avec succès!')
                return redirect('events:detail_event', event_id=event_id)
            else:
                messages.error(request, 'Vous êtes déjà inscrit à cet événement.')
        else:
            messages.error(request, 'Désolé, l\'événement est complet.')
    return render(request, 'events/register_event.html', {'event': event})


@login_required
def user_events(request):
    users_events = Attendance.objects.filter(attendee=request.user).values_list('event', flat=True)
    events = Event.objects.filter(pk__in=users_events)
    return render(request, 'events/user_events.html', {'users_events': events})