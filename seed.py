from accounts.models import CustomUser
from properties.models import Property
from clients.models import Client
from contracts.models import Contract
from visits.models import Visit
from django.utils import timezone
from datetime import timedelta
import random

# * Delete existing data
Visit.objects.all().delete()
Contract.objects.all().delete()
Property.objects.all().delete()
Client.objects.all().delete()
CustomUser.objects.exclude(is_superuser=True).delete()

# * Users
admin = CustomUser.objects.create_user(email="admin@demo.com", password="admin123", role="admin", first_name="Admin", last_name="User")
agents = [
    CustomUser.objects.create_user(email=f"agent{i}@demo.com", password="agent123", role="agent", first_name=f"Agent{i}", last_name="User")
    for i in range(1, 4)
]
viewers = [
    CustomUser.objects.create_user(email=f"viewer{i}@demo.com", password="viewer123", role="viewer", first_name=f"Viewer{i}", last_name="User")
    for i in range(1, 3)
]

#  * Properties
property_statuses = ['available', 'sold', 'rented', 'reserved']
properties = []
for i in range(1, 11):
    owner = random.choice(agents)
    status = random.choice(property_statuses)
    prop = Property.objects.create(
        title=f"Property {i}",
        description=f"Description for property {i}",
        price=random.randint(50000, 500000),
        status=status,
        address=f"Street {i}, City",
        latitude=40.0 + i,
        longitude=-3.0 - i,
        owner=owner,
    )
    properties.append(prop)

# * Clients
clients = []
for i in range(1, 11):
    agent = random.choice(agents)
    client = Client.objects.create(
        name=f"Client {i}",
        email=f"client{i}@demo.com",
        phone=f"60000000{i}",
        notes=f"Notes for client {i}",
        agent=agent,
    )
    clients.append(client)

# * Contracts
contract_types = ['rental', 'sale']
contract_statuses = ['draft', 'signed', 'cancelled']
for i in range(1, 11):
    agent = random.choice(agents)
    # * Only select properties and clients for the current agent
    agent_properties = [p for p in properties if p.owner == agent and p.status == 'available']
    agent_clients = [c for c in clients if c.agent == agent]
    if not agent_properties or not agent_clients:
        continue  # * Skip if no properties or clients for this agent
    prop = random.choice(agent_properties)
    client = random.choice(agent_clients)
    ctype = random.choice(contract_types)
    status = random.choice(contract_statuses)
    start_date = timezone.now().date() + timedelta(days=random.randint(0, 10))
    end_date = start_date + timedelta(days=random.randint(30, 365)) if ctype == 'rental' else None
    contract = Contract.objects.create(
        property=prop,
        client=client,
        agent=agent,
        type=ctype,
        price=random.randint(60000, 400000),
        start_date=start_date,
        end_date=end_date,
        document="contracts/sample.pdf",
        status=status,
    )
    # * Update property status if contract is signed
    if status == 'signed':
        if ctype == 'rental':
            prop.status = 'rented'
        elif ctype == 'sale':
            prop.status = 'sold'
        prop.save()

# * Visits
visit_statuses = ['scheduled', 'completed', 'canceled']
for i in range(1, 21):
    agent = random.choice(agents)
    agent_properties = [p for p in properties if p.owner == agent]
    agent_clients = [c for c in clients if c.agent == agent]
    if not agent_properties or not agent_clients:
        continue
    prop = random.choice(agent_properties)
    client = random.choice(agent_clients)
    status = random.choice(visit_statuses)
    date = timezone.now() + timedelta(days=random.randint(1, 30))
    Visit.objects.create(
        property=prop,
        client=client,
        agent=agent,
        date=date,
        status=status,
        notes=f"Visit {i} notes"
    )

print("Seed data created successfully!")