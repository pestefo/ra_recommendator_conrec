Extension { #name : #SmallInteger }

{ #category : #'*ROSAnswers-Model' }
SmallInteger >> asBoolean [
	"1 = true, 0 = false, <0 or >1 raises error"
	self = 0 ifTrue: [ ^ false ].
	self = 1 ifTrue: [ ^ true ].
	Error signal: 'only 1 or 0 understand this message.'
]
