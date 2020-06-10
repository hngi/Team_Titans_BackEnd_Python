# HNG_TASK3
An SMS notfication service

Running the app with docker locally:
On a Mac or Linux Machine, run sudo bash docker_start.sh to build and run the container.
On a Windows Machine, Build and Run the container Yourself.

This app was built around Twilio API
It is a micro-service that allows sending SMS's to phone numbers using a client app.

You can register and get a trial account at https://www.twilio.com. There are a lot of docs and walkthroughs on the site that will assist you immensely and make the experience easy, these walkthroughs include working codes per your language of choice.

Click this link for a better idea https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply.
To test "Sending custom replies" on your local machine, you will need to download ngrok from https://www.ngrok.com which also has a self explanatory walkthrough that pops up after logging in on the site.

The idea of a microservice is to avoid monolithic (All services in one app) apps, so bare in mind as you design in your language of choice to keep your application as simple and straightforward as possible while not letting back on functionality.
This task however should be able to fit well into one application as there's only one service.

If you have knowledge of Python, you can look at the code here, it's quite easy to understand and is well commented.
Should you still have any confusions, hit me up @Red.

This task is available on http://hng-task3.herokuapp.com and is more of an API.
You'd have to get your number registered on the account being used as it's a trial account, so DM me for that.
The available endpoints are http://hng-task3.herokuapp.com/details and http://hng-task3.herokuapp.com/send
The third endpoint http://hng-task3.herokuapp.com/sms is accessed via SMS and gives a reply.
You'll also have to get registered for that. 

The repo we'd use is still unavailable as at now so do your work locally until then.
This task was originally chosen to be done in Python/Django, but it turns out the concept of the framework defeats the whole purpose of having a micro-service.
The language we'll be doing this task in is Node.js.
Everyone is welcome to still try it out in any framework of their choice, for their personal experience.

Thanks for coming to my Ted Talk.
