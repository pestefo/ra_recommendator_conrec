Class {
	#name : #RAQuestionTest,
	#superclass : #TestCase,
	#category : #'ROSAnswers-Model-Tests'
}

{ #category : #tests }
RAQuestionTest >> testCreation [
	"Assert that a question has its participants correctly"

	| q |
	q := RAQuestion question: 9045.

	self assert: q title equals: 	'Plume Sim in ROS'	.
	self assert: q summary equals: 	'<p>I have used plume sim in Player/Stage - now I want to use it in ROS. However, I am not able to get much of a clue about installing it and using it.</p>
'	.
	self assert: q author  equals: (RAUser user: 7).
	self assert: q lastActivityBy  equals: (RAUser user: 23668).
	self assert: q lastActivityAt equals: (DateAndTime fromUnixTime: 1459868877).
	self assert: q addedAt equals: (DateAndTime fromUnixTime: 1297721473).
	self assert: q viewCount equals: 296.

self assert: q votes equals: 1.



]

{ #category : #tests }
RAQuestionTest >> testParticipants [
	"Assert that a question has its participants correctly"

	| q |
	q := RAQuestion question: 9045.

	self assert: q participants equals: 	#(437 44 51 10 3) asRAUsers	.
	self assert: q nbOfParticipants equals: 5.


]
