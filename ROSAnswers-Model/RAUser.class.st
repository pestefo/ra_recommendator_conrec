Class {
	#name : #RAUser,
	#superclass : #Object,
	#instVars : [
		'userid',
		'name',
		'upVotes',
		'downVotes'
	],
	#category : #'ROSAnswers-Model-Core'
}

{ #category : #accessing }
RAUser class >> user: anUserId [

	^ RAModelInitializer user: anUserId
]

{ #category : #accessing }
RAUser >> = anObject [
	^ super = anObject
		ifTrue: [ true ]
		ifFalse: [ self class = anObject class and: [ self userid = anObject userid ] ]
]

{ #category : #accessing }
RAUser >> downVotes [
	^ downVotes
]

{ #category : #accessing }
RAUser >> downVotes: anObject [
	downVotes := anObject
]

{ #category : #initialization }
RAUser >> initializeFromRosUserTable: anArray [
	"Example:
	#(3 'tfoote' 2938 80)"
	
	self userid: (anArray at: 1) asInteger.
	self name: (anArray at: 2).
	self upVotes: (anArray at: 3) asInteger.
	self downVotes: (anArray at: 4) asInteger.
]

{ #category : #accessing }
RAUser >> name [
	^ name
]

{ #category : #accessing }
RAUser >> name: anObject [
	name := anObject
]

{ #category : #accessing }
RAUser >> printOn: aStream [

	| title |
	title := self class name.
	aStream
		nextPutAll: 'User(';
		nextPutAll: userid asString;
		nextPutAll: ')'.
]

{ #category : #accessing }
RAUser >> upVotes [
	^ upVotes
]

{ #category : #accessing }
RAUser >> upVotes: anObject [
	upVotes := anObject
]

{ #category : #accessing }
RAUser >> userid [
	^ userid
]

{ #category : #accessing }
RAUser >> userid: anObject [
	userid := anObject
]
