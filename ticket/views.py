import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket
from .form import CreateTicketForm, UpdateTicketForm


# view ticket details
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    context = {'ticket': ticket}
    return render(request, 'ticket/ticket_details.html', context)


"""For customers"""""


# create a ticket
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request, 'Your ticket has been successfully saved. An engineer will be assigned soon.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong, please check form inputs')
            return redirect('create-tickets')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)


# updating the ticket
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your ticket info has been been updated and all the changes are saved.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong, please check form inputs')
            # return redirect('create-tickets')

    else:
        form = UpdateTicketForm(instance=ticket)
        context = {'form': form}
        return render(request, 'ticket/update_ticket.html', context)


# viewing all created tickets
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    context = {'tickets': tickets}
    return render(request, 'tickets/all_tickets.html', context)


"""For engineers"""


# view ticket queue
def ticket_queue(request):
    tickets = Ticket.objects.filter(tikcet_status='Pending')
    context = {'tickets': tickets}
    return render(request, 'tickets/tickets_queue.html', context)


# accept a ticket from the queue
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted. Please resolve as soon as possible')
    return redirect('ticket-queue')


# close a ticket
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.closed_date = datetime.datetime.now()
    ticket.is_resolved = True
    ticket.save()
    messages.info(request, 'Ticket has been resolved. Thank you brilliant support engineer')
    return redirect('ticket-queue')


# tickets engineer is working on
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {'tickets': tickets}
    return render(request, 'tickets/workspace.html', context)


# all closed/resolved tickets
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {'tickets': tickets}
    return render(request, 'tickets/all_closed_tickets.html', context)
