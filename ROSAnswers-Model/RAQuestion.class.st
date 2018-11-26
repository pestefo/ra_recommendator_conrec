Class {
	#name : #RAQuestion,
	#superclass : #Object,
	#instVars : [
		'questionid',
		'title',
		'author',
		'addedAt',
		'summary',
		'lastActivityAt',
		'lastActivityBy',
		'viewCount',
		'votes'
	],
	#category : #'ROSAnswers-Model-Core'
}

{ #category : #services }
RAQuestion class >> question: aQuestionId [

	^ RAModelInitializer question: aQuestionId 
]

{ #category : #accessing }
RAQuestion >> addedAt [
	^ addedAt
]

{ #category : #accessing }
RAQuestion >> addedAt: anObject [
	addedAt := anObject
]

{ #category : #accessing }
RAQuestion >> author [
	^ author
]

{ #category : #accessing }
RAQuestion >> author: anObject [
	author := anObject
]

{ #category : #accessing }
RAQuestion >> initializeFromRosQuestionTable: anArray [
	"Example:
	#(9036 'What is a ROS package?' 2 1297698004 '<p>Information on ROS packages.</p>
' 'http://answers.ros.org/question/9036/what-is-a-ros-package/' 1297722788 3 702 3)"
	self questionid: (anArray at: 1) asInteger.
	self title: (anArray at: 2).
	self author: (RAUser user: (anArray at: 3) asInteger).
	self addedAt: (DateAndTime fromUnixTime: (anArray at: 4) asInteger).
	self summary: (anArray at: 5).
	self lastActivityAt: (DateAndTime fromUnixTime: (anArray at: 7) asInteger).
	self lastActivityBy: (RAUser user: (anArray at: 8) asInteger).
	self viewCount: (anArray at: 9) asInteger.
	self votes: (anArray at: 10) asInteger.


]

{ #category : #accessing }
RAQuestion >> lastActivityAt [
	^ lastActivityAt
]

{ #category : #accessing }
RAQuestion >> lastActivityAt: anObject [
	lastActivityAt := anObject
]

{ #category : #accessing }
RAQuestion >> lastActivityBy [
	^ lastActivityBy
]

{ #category : #accessing }
RAQuestion >> lastActivityBy: anObject [
	lastActivityBy := anObject
]

{ #category : #accessing }
RAQuestion >> questionid [
	^ questionid
]

{ #category : #accessing }
RAQuestion >> questionid: anObject [
	questionid := anObject
]

{ #category : #accessing }
RAQuestion >> summary [
	^ summary
]

{ #category : #accessing }
RAQuestion >> summary: anObject [
	summary := anObject
]

{ #category : #accessing }
RAQuestion >> title [
	^ title
]

{ #category : #accessing }
RAQuestion >> title: anObject [
	title := anObject
]

{ #category : #accessing }
RAQuestion >> url [
	^ 'http://answers.ros.org/question/9036/what-is-a-ros-package/', self questionid asString
]

{ #category : #accessing }
RAQuestion >> viewCount [
	^ viewCount
]

{ #category : #accessing }
RAQuestion >> viewCount: anObject [
	viewCount := anObject
]

{ #category : #accessing }
RAQuestion >> votes [
	^ votes
]

{ #category : #accessing }
RAQuestion >> votes: anObject [
	votes := anObject
]
