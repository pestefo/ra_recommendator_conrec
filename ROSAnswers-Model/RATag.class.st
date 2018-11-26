Class {
	#name : #RATag,
	#superclass : #Object,
	#instVars : [
		'tagid',
		'name'
	],
	#category : #'ROSAnswers-Model-Core'
}

{ #category : #accessing }
RATag class >> tag: aTagId [

	^ RAModelInitializer tag: aTagId 
]

{ #category : #comparing }
RATag >> = anObject [
	^ super = anObject
		ifTrue: [ true ]
		ifFalse: [ self class = anObject class and: [ self tagid = anObject tagid ] ]
]

{ #category : #initialization }
RATag >> initializeFromRosTagTable: anArray [
	"Example:
	#(5 'gmapping')"
	
	self tagid: (anArray at: 1) asInteger.
	self name: (anArray at: 2).
]

{ #category : #accessing }
RATag >> name [
	^ name
]

{ #category : #accessing }
RATag >> name: anObject [
	name := anObject
]

{ #category : #accessing }
RATag >> tagid [
	^ tagid
]

{ #category : #accessing }
RATag >> tagid: anObject [
	tagid := anObject
]
