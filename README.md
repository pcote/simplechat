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
The default setup for this application is not intended to be secure.  How to secure it properly is left to the discretion of the user.
That being said, here are some pointers to consider.....

- Before you type "vagrant up", change the database password.  The default password is "temporary_password" and it needs changing in a couple of places.
    - provision.sh: It shows up three times in the setup_database function.
    - chatservice/settings.ini: Change the db_password parameter so it matches what you set it to in provision.sh
    - Use the mysql administration tool of your choice to change the password of the mysql root account.

- Change the secret key: The secret key helps secure the session cookie used by simplechat.
    - chatservice/settings.ini:  Change the "secret_key" parameter to a sufficiently long and random string of characters.

- Make a new db_user with restricted privileges.
    - chatservice/settings.ini: Change the db_user parameter from "root" to the less privileged user account.
    - chatservice/settings.ini: Change the db_password parameter to the password that matches the less privileged account.
    - Make sure the less privileged account in question exists with the password specified.
        - The account should have SELECT and INSERT rights on the USERS and MESSAGES tables in the SIMPLECHAT database.
        - See the manual for the MySQL admin tool of your choice for specifics on how to carry this out.

