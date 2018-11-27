Class {
	#name : #RAAnswer,
	#superclass : #Object,
	#instVars : [
		'answerid',
		'author',
		'date',
		'votes',
		'isAccepted'
	],
	#category : #'ROSAnswers-Model-Core'
}

{ #category : #accessing }
RAAnswer class >> answer: answerId [

	^ RAModelInitializer answer: answerId
]

{ #category : #accessing }
RAAnswer >> = anObject [
	^ super = anObject
		ifTrue: [ true ]
		ifFalse: [ self class = anObject class and: [ self answerid = anObject answerid ] ]
]

{ #category : #accessing }
RAAnswer >> answerid [
	^ answerid
]

{ #category : #accessing }
RAAnswer >> answerid: anObject [
	answerid := anObject
]

{ #category : #accessing }
RAAnswer >> author [
	^ author
]

{ #category : #accessing }
RAAnswer >> author: anObject [
	author := anObject
]

{ #category : #accessing }
RAAnswer >> date [
	^ date
]

{ #category : #accessing }
RAAnswer >> date: anObject [
	date := anObject
]

{ #category : #initialization }
RAAnswer >> initializeFromRosAnswerTable: anArray [
	"Example:
	#(4	 3 'answer' '2011-02-14	16:33:08 -0500'	12	1)"
	
	self answerid: (anArray at: 1).
	self author: (RAUser user: (anArray at: 2)).
	self date: (DateAndTime fromString: (anArray at: 4)).
	self votes: (anArray at: 5).
	self isAccepted: (anArray at: 6) asInteger asBoolean.
]

{ #category : #accessing }
RAAnswer >> isAccepted [
	^ isAccepted
]

{ #category : #accessing }
RAAnswer >> isAccepted: anObject [
	isAccepted := anObject
]

{ #category : #initialization }
RAAnswer >> isAnswer [

	^ true
]

{ #category : #initialization }
RAAnswer >> isComment [

	^ false
]

{ #category : #accessing }
RAAnswer >> votes [
	^ votes
]

{ #category : #accessing }
RAAnswer >> votes: anObject [
	votes := anObject
]