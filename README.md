# project
Goal: 
Help teachers invite students to engage more with online teaching.
Help students analyze their own engagement in the lectures they are attending.
Help teachers analyze the average engagement in the lectures they are teaching.
To do that, we enable students to
Analyze emotions (e.g., confusion, attentiveness, agreement, disagreement, etc.) during each lecture or over a series of lectures. They can use the report for themselves and, optionally, share anonymously with their teachers.
Convey actions (e.g., nodding, raising hand, clapping, even smiling) in real time easily in their virtual lectures. The assumption here is that most students have turned their video off due to bandwidth concerns and would like to still convey these actions in real time. 

Students can download an app that will
Analyze the live webcam video in real time.
Display the aforementioned actions/emotions during video calls by replacing the live webcam with a pre-recorded video of the user. Each video communicates a specific action/emotional indicator. 
Return a report to the student with a breakdown of their engagement with the lecture.

Usage
Users need to start the utility on their laptop while they are attending a lecture. Once the lecture is done or earlier if they wish, they can stop analysis. 
Extension: the utility will stop itself when the meeting is over.

vroom analyze start <user_email> <lecture_id>
vroom analyze stop <user_email> [lecture_id]    // assuming only one lecture is on

Set-up process
	
pip install vroom
vroom calibrate <calibration_video> <user_email>
