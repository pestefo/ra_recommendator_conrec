Class {
	#name : #RAComment,
	#superclass : #RAAnswer,
	#category : #'ROSAnswers-Model-Core'
}

{ #category : #'accessing comment' }
RAComment class >> comment: commentId [

	^ RAModelInitializer answer: commentId
]

{ #category : #accessing }
RAComment >> isAccepted [
	^ false
]

{ #category : #accessing }
RAComment >> isAnswer [

	^ false
]

{ #category : #accessing }
RAComment >> isComment [

	^ true
]
