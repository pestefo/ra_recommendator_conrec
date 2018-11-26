"
I store metadata for this package. These meta data are used by other tools such as the SmalllintManifestChecker and the critics Browser
"
Class {
	#name : #ManifestROSAnswersModel,
	#superclass : #PackageManifest,
	#category : #'ROSAnswers-Model-Manifest'
}

{ #category : #'code-critics' }
ManifestROSAnswersModel class >> ruleRBUnaryAccessingMethodWithoutReturnRuleV1FalsePositive [
	^ #(#(#(#RGMethodDefinition #(#'RAModelInitializer class' #reset #true)) #'2018-11-26T14:54:11.046926-03:00') )
]
