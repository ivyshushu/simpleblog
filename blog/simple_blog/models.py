from django.db import models
from django.contrib import admin
from twilio.rest import TwilioRestClient

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=60)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title


class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=60)
	body = models.TextField()
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return unicode("%s: %s" % (self.post,self.body[:60]))

	def save(self, *args, **kwargs):
		"""send sms when new comment is added"""
		if "notify" in kwargs and kwargs["notify"] == True:
			message = "new comment just added!!!"
			number = "+16134134223"
			account_sid = 'AC25ef232740072dc660a9b676d9e5c992'
			auth_token = 'ff5269d59167dedf051268d5ef3e4b91'
			client = TwilioRestClient(account_sid, auth_token)
			client.sms.messages.create(to=number, from_="+13473086943", body=message)
		
		if "notify" in kwargs:
			del kwargs["notify"]


		super(Comment, self).save(*args, **kwargs)




	











	

