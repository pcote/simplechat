SimpleChat

Purpose: A demonstration of a way to create a basic chat program.

Host Environment Requirements
=============================
- A 64-bit Host Operating System.  (note: Project developed and tested on a Windows 8.1 host.)
- VirtualBox installation ( https://www.virtualbox.org/wiki/Downloads )
- Vagrant ( https://www.vagrantup.com/ )
- Git (optional but recommended)
- A recent browser.  Any browser newer than Internet Explorer 9 should work fine.


How to Install (the simplest way)
=================================
1. Use Git to clone the project to the directory of your choice.  Open a command prompt to that directory and type this....
git clone https://github.com/pcote/simplechat.git

2. Navigate to the simplechat directory.  Type the following....
vagrant up

After a few minutes of automated set up.  You should now have a full virtual server with a working chap application on it.


Getting to know the chat room
=============================
After you've gotten the server going, you'll need to create an account.  Do the following....

1.  Open up a browser and go to http://localhost

2.  Click the link to "create new account".

3.  Fill in the fields presented here.  The password must be 8 characters or longer and made up of letters, numbers, and symbols.

4.  Click the "create" button.  If the username is new and the password passes muster, you will be taken straight to the chat room under the account you just created.

5.  Try it out by putting in some messages in the field bar underneath the chat message display.

6.  When done, simply close the browser.  Closing the browser should automatically log you out.


And that's it.  If you want to log in again later, just go to http://localhost and log yourself in with your account.

Chatting with other people
==========================
You'll want to communicate with other people.  This requires making it available on the Internet.  Here's a simple way.

1.  Download and install ngrok ( https://ngrok.com/ )

2.  Open up a command prompt and type this:
ngrok 80

3.  Ngrok will give you a url that you can send to a friend that you want to chat with.

4.  Have a nice chat.


Security considerations
========================
TODO

