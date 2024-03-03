# messages/models.py

from django.contrib.auth.models import User
from django.db import models
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField(null=True, blank=True)
    private_key = models.TextField(null=True, blank=True)  # Add private_key field
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.public_key:
            # Generate RSA key pair for the user if not provided
            key = RSA.generate(2048)
            self.public_key = key.publickey().export_key().decode()
            self.private_key = key.export_key().decode()  # Store private key
        super().save(*args, **kwargs)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)  # Field to store plaintext content
    encrypted_content = models.BinaryField(blank=True, null=True)  # Field to store encrypted content
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}"

    def encrypt_message(self, content, recipient_public_key):
        cipher = PKCS1_OAEP.new(recipient_public_key)
        encrypted_content = cipher.encrypt(content.encode())
        self.encrypted_content = base64.b64encode(encrypted_content)


    def decrypt_message(self, recipient_private_key_str):
        recipient_private_key = RSA.import_key(recipient_private_key_str)
        cipher = PKCS1_OAEP.new(recipient_private_key)
        encrypted_content = base64.b64decode(self.encrypted_content)
        decrypted_content = cipher.decrypt(encrypted_content)
        self.content = decrypted_content.decode()  # Update the content field with decrypted message
        return decrypted_content.decode() # Return decrypted content without updating the content field


