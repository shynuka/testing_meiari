from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from meiari_v1.models import WorkGroup, MeiAriUser, WorkGroupTicket

User = get_user_model()

class WorkGroupModelTests(TestCase):
    def setUp(self):
        # Setup users and workgroup for testing
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.group = WorkGroup.objects.create(
            group_name='Test Group',
            is_active=True,
            created_at=timezone.now(),
            modified_at=timezone.now()
        )
        self.group.users.add(self.user)  # Add user to the WorkGroup

    def test_workgroup_creation(self):
        # Test valid creation
        self.assertEqual(self.group.group_name, 'Test Group')

        # Test invalid creation (e.g., missing fields)
        with self.assertRaises(ValueError):  # assuming it raises a ValueError on invalid creation
            WorkGroup.objects.create(group_name="", is_active=None, created_at=None)

    def test_workgroup_user_relationship(self):
        # Test user association with WorkGroup
        self.assertIn(self.user, self.group.users.all())
        self.assertEqual(self.group.users.count(), 1)  # Only 1 user should be added

    def test_workgroup_str(self):
        # Test the string representation of the WorkGroup
        self.assertEqual(str(self.group), "Test Group")

    def test_workgroup_created_at(self):
        # Test if the created_at timestamp is assigned correctly
        self.assertIsInstance(self.group.created_at, timezone.datetime)

    def test_workgroup_modified_at(self):
        # Test if the modified_at timestamp is assigned correctly
        self.assertIsInstance(self.group.modified_at, timezone.datetime)

    def test_workgroup_ticket_creation(self):
        # Test creation of a WorkGroupTicket linked to a WorkGroup
        ticket = WorkGroupTicket.objects.create(
            ticket_code='TCK001',
            ticket_title='Test Ticket',
            ticket_description='This is a test ticket.',
            ticket_status='Created',
            ticket_type='TaskAssign',
            ticket_priority='High',
            work_group=self.group,
            ticket_owner_id=self.user
        )

        # Test ticket creation
        self.assertEqual(ticket.ticket_code, 'TCK001')
        self.assertEqual(ticket.ticket_status, 'Created')
        self.assertEqual(ticket.ticket_type, 'TaskAssign')
        self.assertEqual(ticket.work_group, self.group)
        self.assertEqual(ticket.ticket_owner_id, self.user)

    def test_ticket_status_update(self):
        # Test if we can update ticket status
        ticket = WorkGroupTicket.objects.create(
            ticket_code='TCK002',
            ticket_title='Test Status Update',
            ticket_description='Ticket status update test.',
            ticket_status='Created',
            ticket_type='CustomTemplate',
            ticket_priority='Medium',
            work_group=self.group,
            ticket_owner_id=self.user
        )
        
        ticket.ticket_status = 'Completed'
        ticket.save()

        # Test if status is updated correctly
        ticket.refresh_from_db()  # Refresh to get the latest data
        self.assertEqual(ticket.ticket_status, 'Completed')
