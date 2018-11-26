Class {
	#name : #RAUserTagRelation,
	#superclass : #Object,
	#instVars : [
		'dict'
	],
	#classInstVars : [
		'uniqueInstance'
	],
	#category : #'ROSAnswers-Model'
}

{ #category : #accessing }
RAUserTagRelation class >> reset [

	uniqueInstance := nil
]

{ #category : #accessing }
RAUserTagRelation class >> uniqueInstance [

	^ uniqueInstance ifNil: [ uniqueInstance := self new ]
]

{ #category : #initialization }
RAUserTagRelation >> at: aRAUserId put: aTagId withValue: anInteger [
	dict
		at: aRAUserId
		ifPresent: [ :v | v add: #(aTagId anInteger) ]
		ifAbsentPut: [ {#(aTagId anInteger)} asOrderedCollection ]
]

{ #category : #initialization }
RAUserTagRelation >> initialize [ 
	super initialize.
	
	dict := Dictionary new.

]

{ #category : #initialization }
RAUserTagRelation >> tagsForUser: aRAUser [

	^ (self tagsForUser: aRAUser ) collect: [:pair | RATag tag: pair first]
]

{ #category : #initialization }
RAUserTagRelation >> tagsWithValueForUser: aRAUser [

	^ (dict at: aRAUser userid) collect: #first
]

{ #category : #initialization }
RAUserTagRelation >> usersForTag: aRATag [

	^ (dict associations select: [ :pair | pair value first = aRATag tagid ])
		collect: [ :pair | RAUser user: pair key ]
]
