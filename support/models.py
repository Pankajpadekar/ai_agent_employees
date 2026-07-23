from django.db import models
from django.contrib.auth.models import User
from orders.models import Order
# Create your models here.

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='conversations')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation by {self.id}: {self.user.username} at {self.timestamp}"
    
class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('agent', 'Agent'),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=200, choices=ROLE_CHOICES)  # Could be 'user' or 'agent'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.role} : {self.content[:50]} at {self.timestamp}"
    

class AgentLog(models.Model):
    EVENT_CHOICES = [
        ('support', "Support Agent"),
        ("tool_call", "Tool Call"),
        ('tool_result', 'Tool Result'),
        ('manager', "Manager Agent"),
        ('risk', 'Risk Agent'),
        ("final", "Final Reply")
        # Add more event types as needed
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='agent_logs')
    event_type = models.CharField(max_length=200, choices=EVENT_CHOICES)  # e.g., 'response_generated', 'error', etc.
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AgentLog: {self.event_type} : {self.message[:50]} at {self.timestamp}"