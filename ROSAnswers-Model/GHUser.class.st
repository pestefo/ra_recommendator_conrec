Class {
	#name : #GHUser,
	#superclass : #Object,
	#instVars : [
		'userid',
		'username',
		'followers',
		'url',
		'name',
		'company',
		'email'
	],
	#category : #'ROSAnswers-Model-Core'
}

{ #category : #accessing }
GHUser >> company [
	^ company
]

{ #category : #accessing }
GHUser >> company: anObject [
	company := anObject
]

{ #category : #accessing }
GHUser >> email [
	^ email
]

{ #category : #accessing }
GHUser >> email: anObject [
	email := anObject
]

{ #category : #accessing }
GHUser >> followersCount [
	^ followers
]

{ #category : #accessing }
GHUser >> followersCount: anObject [
	followers := anObject
]

{ #category : #initialization }
GHUser >> initializeFromGhUserTable: anArray [
	"Example:
	#(2 'gonzalocasas' 58 'https://github.com/gonzalocasas' 'Gonzalo Casas' 'ETH Zürich, Institute of Technology in Architecture' 'gonzalocasas@gmail.com')"
	
	self userid: (anArray at: 1).
	self username: (anArray at: 2).
	self followersCount: (anArray at: 3).
	self url: (anArray at: 4).
	self name: (anArray at: 5).
	self company: (anArray at: 6).
	self email: (anArray at: 7).	
	
]

{ #category : #accessing }
GHUser >> name [
	^ name
]

{ #category : #accessing }
GHUser >> name: anObject [
	name := anObject
]

{ #category : #accessing }
GHUser >> url [
	^ url
]

{ #category : #accessing }
GHUser >> url: anObject [
	url := anObject
]

{ #category : #accessing }
GHUser >> userid [
	^ userid
]

{ #category : #accessing }
GHUser >> userid: anObject [
	userid := anObject
]

{ #category : #accessing }
GHUser >> username [
	^ username
]

{ #category : #accessing }
GHUser >> username: anObject [
	username := anObject
]
