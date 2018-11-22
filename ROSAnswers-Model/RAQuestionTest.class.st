Class {
	#name : #RAQuestionTest,
	#superclass : #TestCase,
	#category : #'ROSAnswers-Model-Tests'
}

{ #category : #tests }
RAQuestionTest >> testParticipants [
	"Assert that a question has its participants correctly"

	| q |
	q := RAQuestion question: 9045.

	self assert: q participants equals: 	#(437 44 51 10 3) asRAUsers	.
	self assert: q nbOfParticipants equals: 5.


]
