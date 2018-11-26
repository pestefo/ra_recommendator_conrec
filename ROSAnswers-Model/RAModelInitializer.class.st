Class {
	#name : #RAModelInitializer,
	#superclass : #Object,
	#instVars : [
		'questions',
		'users',
		'answers',
		'tags'
	],
	#classInstVars : [
		'uniqueInstance'
	],
	#category : #'ROSAnswers-Model'
}

{ #category : #accessing }
RAModelInitializer class >> answer: anAnswerId [

	^ self uniqueInstance answer: anAnswerId 
]

{ #category : #accessing }
RAModelInitializer class >> question: aQuestionId [

	^ self uniqueInstance question: aQuestionId 
]

{ #category : #accessing }
RAModelInitializer class >> reset [ 	
	uniqueInstance := nil
]

{ #category : #accessing }
RAModelInitializer class >> tag: aTagId [ 

	^ self uniqueInstance tag: aTagId 
]

{ #category : #accessing }
RAModelInitializer class >> uniqueInstance [ 

	^ uniqueInstance ifNil: [ uniqueInstance := self new.  ]
]

{ #category : #accessing }
RAModelInitializer class >> user: anUserId [

	^ self uniqueInstance user: anUserId 
]

{ #category : #accessing }
RAModelInitializer >> answer: anAnswerId [

 	^ answers detect: [ :a | a answerid = anAnswerId  ]
	
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> answersCount [

	^ answers size
]

{ #category : #files }
RAModelInitializer >> answersDataFile [

	^ (self pathToDataFiles , '/ros_answer.csv') asFileReference 
]

{ #category : #accessing }
RAModelInitializer >> clean [ 
	
	users removeDuplicates.
	questions removeDuplicates.
	answers removeDuplicates.
	tags removeDuplicates.
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> commentsCount [

	^ (answers select: #isComment) size
]

{ #category : #initialization }
RAModelInitializer >> initialize [
	"initialize all the models"

	users := OrderedCollection new.
	questions := OrderedCollection new.	
	answers := OrderedCollection new.	
	tags := OrderedCollection new.
]

{ #category : #files }
RAModelInitializer >> pathToDataFiles [ 

	^ '/home/pestefo/projects/experiment_1/data'
]

{ #category : #initialization }
RAModelInitializer >> populateAnswers [

	(NeoCSVReader on: self answersDataFile readStream)
		do: [ :row | 
			(row at: 3) = 'answer'
				ifTrue: [ answers add: (RAAnswer new initializeFromRosAnswerTable: row) ]
				ifFalse: [ (row at: 3) = 'comment'
						ifTrue: [ answers add: (RAComment new initializeFromRosAnswerTable: row) ]
						ifFalse: [ Error signal: 'Current row is not an answer nor a comment' ] ] ]
]

{ #category : #initialization }
RAModelInitializer >> populateModels [

	self populateUsers.
	self populateQuestions.
	self populateAnswers.
	self populateTags.	
]

{ #category : #initialization }
RAModelInitializer >> populateQuestions [

	(NeoCSVReader on: self questionsDataFile readStream) do: [ :row |
		questions add: (RAQuestion new initializeFromRosQuestionTable: row)   ]
]

{ #category : #initialization }
RAModelInitializer >> populateTags [

	(NeoCSVReader on: self tagsDataFile readStream) do: [ :row |
		tags add: (RATag new initializeFromRosTagTable: row)   ]
]

{ #category : #initialization }
RAModelInitializer >> populateUsers [

	(NeoCSVReader on: self usersDataFile readStream) do: [ :row |
		users add: (RAUser new initializeFromRosUserTable: row)   ]
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> pureAnswersCount [

	^ (answers select: #isAnswer) size
]

{ #category : #accessing }
RAModelInitializer >> question: aQuestionId [
	^ questions
		detect: [ :q | q questionid = aQuestionId ]
		ifNone: [ questions add: (RAQuestion new questionid: aQuestionId).
			Transcript
				show:
					(''
						join:
							{'Question id:'.
							aQuestionId asString.
							' was not found. I created a RAQuestion instance with an incomplete profile'}) ]
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> questionsCount [

	^ questions size
]

{ #category : #files }
RAModelInitializer >> questionsDataFile [

	^ (self pathToDataFiles , '/ros_question.csv') asFileReference 
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> questionsFullProfileCount [

	^ (questions select: #profileComplete) size
]

{ #category : #accessing }
RAModelInitializer >> tag: aTagId [ 

 	^ tags detect: [ :t | t tagid = aTagId  ]
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> tagsCount [

	^ tags size
]

{ #category : #files }
RAModelInitializer >> tagsDataFile [

	^ (self pathToDataFiles , '/ros_tag.csv') asFileReference 
]

{ #category : #accessing }
RAModelInitializer >> user: anUserId [
	^ users
		detect: [ :u | u userid = anUserId ]
		ifNone: [ users add: (RAUser new userid: anUserId).
			Transcript
				show:
					(''
						join:
							{'User id:'.
							anUserId asString.
							' was not found. I created a RAUser instance with an incomplete profile'}) ]
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> usersCount [

	^ users size
]

{ #category : #files }
RAModelInitializer >> usersDataFile [

	^ (self pathToDataFiles , '/ros_user.csv') asFileReference 
]

{ #category : #'as yet unclassified' }
RAModelInitializer >> usersFullProfileCount [

	^ (users select: #profileComplete) size
]
