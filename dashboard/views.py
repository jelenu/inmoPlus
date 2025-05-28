from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from properties.models import Property
from clients.models import Client
from contracts.models import Contract
from visits.models import Visit
from django.utils import timezone
from django.db import models
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}

        if user.role == 'admin':
            properties = Property.objects.all()
            clients = Client.objects.all()
            contracts = Contract.objects.all()
            visits = Visit.objects.all()
        elif user.role == 'agent':
            properties = Property.objects.filter(owner=user)
            clients = Client.objects.filter(agent=user)
            contracts = Contract.objects.filter(agent=user)
            visits = Visit.objects.filter(agent=user)
        else:
            return Response({"detail": "Not authorized."}, status=403)

        properties_by_status = properties.values('status').order_by('status').annotate(count=models.Count('id'))
        properties_status_dict = {item['status']: item['count'] for item in properties_by_status}

        contracts_by_type = contracts.values('type').order_by('type').annotate(count=models.Count('id'))
        contracts_type_dict = {item['type']: item['count'] for item in contracts_by_type}

        now = timezone.now()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        visits_completed_this_month = visits.filter(
            status='completed',
            date__gte=first_day,
            date__lte=now
        ).count()

        if user.role == 'agent':
            visits_pending = visits.filter(status='scheduled').count()
            visits_completed = visits.filter(status='completed').count()
        else:
            visits_pending = visits.filter(status='scheduled').count()
            visits_completed = visits.filter(status='completed').count()

        data = {
            "total_properties": properties.count(),
            "properties_by_status": properties_status_dict,
            "total_clients": clients.count(),
            "total_contracts": contracts.count(),
            "contracts_by_type": contracts_type_dict,
            "visits_completed_this_month": visits_completed_this_month,
        }

        if user.role == 'agent':
            data.update({
                "my_properties": properties.count(),
                "my_clients": clients.count(),
                "my_contracts": contracts.count(),
                "my_visits_pending": visits_pending,
                "my_visits_completed": visits_completed,
            })

        return Response(data)
