# vroom
The goal of this project is to help students engage more with online learning. The program allows students who are uncomfortable turning on their video to convey relevant emotions and engage with the lesson by detecting specific actions such as smiling or raising a hand and conveying them through an avatar.
There are a lot of sections so scroll through and read the headers to tell which information will be useful to you.  

Demonstration: 
https://youtu.be/5kFrOYaHkvc

## Students

So you're a student, who, for whatever reason, doesn't want to turn on their camera. Teachers aren't legally allowed to make you do so, but that doesn't seem to stop them (some of them at least #notallteachers). Wouldn't it be cool to be able to show the teacher that you're still paying attention without showing your face? (Yes, it would, is the correct answer. No other options allowed.) (Arguably) even cooler, you can raise your hand without having to press that weird yellow hand reaction in zoom, which isn't terrible – it's the wrong skin color no matter who you are and I respect that – actually, no, it's pretty terrible and that's the only good thing I have to say about it. 

Ever spent hours at a time obsessively creating picrews? (iykyk) Well, now's the time to put them to good use. Sure, regular profile pictures are fun, but what about a profile picture that reflects your actions? If you squint, it even looks like animation (figuratively, that is. If you actually squint, it'll squint too).

If you don't know what picrews are, they're basically customizable avatars. When you download this program, it comes with a very generic one as an example, but the whole point is for you to change it!! Here are some that you can try: 

https://picrew.me/image_maker/344854 (used for the default)

https://picrew.me/image_maker/137904

https://picrew.me/image_maker/567717

https://picrew.me/image_maker/114808

https://picrew.me/image_maker/407027

https://picrew.me/image_maker/644129

https://picrew.me/image_maker/420013

https://picrew.me/image_maker/154823 (one of my favorites)*

https://picrew.me/image_maker/14314 (another favorite)*

*However, it is more useful if the images match up with the expressions (squint, wide-eyed, smile -- more to come!!)

Side note: I sincerely doubt that anyone will be judging your picrews – I wouldn't and I'm a very judgemental person – but, hey, I get it. You can still use it with friends for fun (anyone have online friends they're not allowed to show their face to? no? just me?) and obviously, there's no restriction on which images you choose. Yes, that does mean you can use memes, raccoon pictures, etc. Who can stop you? Why use this instead of just setting your profile picture to your picture of choice? Well, consider this: not one raccoon meme, but four. 

Also featuring a rough graph of engagement during a call that students can view, just for funzies (Am I using that ironically? Yes. Am I aware that using a term or phrase ironically usually leads to using it unironically? Also yes, but we're going to ignore that for now.) 

Another IMPORTANT side note: 
Currently, this program works by changing your profile picture in real time, so you have to turn off your video to use it, and it only works on Zoom. But, in the future, look out for a version that creates an entirely new stream for you to select as your video source in any video call application. Also, that doesn't make you run the program in terminal every time you want to use it. Basically just an overall better version.

Ok, pitch over. Want to learn about this project without suffering through my attempts to be funny? Just keep reading, past the Instructions section (although that's probably also useful), second star on the right, and straight on till morning (i.e., the project summary section).

## Teachers

Here's the part especially relevant for teachers reading this: 
You can integrate this program into a lesson. Let's take smiling, which has been shown to improve happiness levels. For example, ask your students to smile to show they've understood what you've said. Now you're asking everyone to interact with the lesson in a way that has a positive impact and is likely to increase their interest in the lesson. In the future, different hand gestures and more expressions will be added, expanding the range of gestures you can use to increase their engagement.

## Instructions
If you don't have homebrew and python3, this is a more involved process.
### Download
Open terminal. (For each step, copy-paste the line of code in terminal and press enter. )
#### 0. Install command line tools
`xcode-select --install`

#### 0.5. Install homebrew
`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
Don't forget to press enter when it prompts you to.

#### 0.75. Install python3 (if you don't have it)
`brew install python python3`

#### 1. Install cmake
`brew install cmake`

#### 1.5. Create virtual environment (optional)
`python3 -m venv vroom-venv`

#### 2. Install the package
`pip3 install --timeout 10000 vroompkg`
(Don't move the downloaded folder from Downloads. If you really have to, it's easy to fix the code if you already have Python experience. You can also contact me and I can send you a version of the program that works for you.)

#### 3. Get zoom API token (in the near future, I will drop this requirement)
Go to [https://marketplace.zoom.us/develop/create] (https://marketplace.zoom.us/develop/create)
* Log in with your zoom account
* Choose "Build App" in the Develop dropdown at the top right
* Choose JWT
* Put in "test" (or whatever you like) as the app name and company name
* Create a token by putting "test" in company name and your name and email into developer information
* Create a token by setting a long expiry, say 1 week from now. 
* Copy the JWT token and save it -- you will need it to use the Vroom tool. 

### Change the Images:
In the downloaded folder, you'll find four images: defaultpic.png, smilepic.png, squintpic.png, and widepic.png. Hopefully the names are pretty self-explanatory. When you have your own versions of a default picture, a smiling picture, a squinting picture, and a wide-eyed picture, delete the existing ones and drag yours into the folder. Make sure to name them the exact same things.

### Run
#### 1. Join your meeting. Turn your video off.

#### 1.5 Activate virtual environment (if you created it when downloading)
`source vroom-venv/bin/activate`

#### 2. Run
Open terminal. Type `python3 -m vroompkg -u <your zoom account email> -m <10-digit meeting ID, no spaces> -t <the JWT token you saved>`
example: `python3 -m vroompkg -u user@random.org -m 1234567890`
Make sure your JWT token hasn't expired.

#### 3. End
When your meeting is over, go back to terminal and press control C. 

#### 4. Access reports
In terminal, you should see a breakdown in percentages of how much you performed the detected expressions. In Finder, search with the date in the format `mm-dd-yy`. You should find two files titled with the date – a .csv file and a .png. The .csv will show you the same thing you can see in terminal, but the .png will contain a graph of estimated engagement/interest over time.
example: `02-24-21.png` and `02-24-21.csv` (you can find these examples in the Github repo if you want to see what they look like)


#### 5. Fill out survey.
Please take 30 seconds to fill out the survey (no hard questions, I promise):
https://forms.gle/mFYcfHfwdKJcEAgQA

## Known issues and limitations
* doesn't end when meeting ends, you have to press control C
* hand detection not yet implemented
* only works on Zoom
* 1 to 2 second delay


## Project Summary
This project will:
* Help teachers invite students to engage more with online teaching.
* Help students interact more with the lesson while still being able to turn their camera off.
* Help students analyze their own engagement in the lectures they are attending.


Students can download an app that will
* Analyze the live webcam video in real time.
* Display the aforementioned actions/emotions during video calls by replacing the live webcam with a user-selected image, communicating a specific action/emotional indicator. 
* Return a report to the student with a breakdown of their engagement with the lecture.
