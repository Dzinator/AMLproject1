# Applied Machine Learning (COMP551) - Project 1
Applied Machine Learning - Project 1

Multilingual Dialog Dataset

In order to provide conversational training data in other
languages than English we propose parsing openly available
theatre plays in French. For this purpose, we will be curating
dialog datasets in French, obtained by crawling through
websites that aggregate openly available theatre works in a
consistent and parseable format. In addition, we will parse
sample interviews, released by authors through free sources on
the web as well as language tutorials that feature conversations
in French.

Extracted dialogs are in an XML format like this:
`<dialog>
	<s>
		<utt uid=”1”>Hey, how are you?</utt>
		<utt uid=”2”>I’m fine thank you!</utt>
		<utt uid=”1”>Nice!</utt>
	</s>
	<s>
		<utt uid=”1”>Who’s around for lunch?</utt>
		<utt uid=”2”>Me!</utt>
		<utt uid=”3”>Me too!</utt>
	</s>
</dialog>`

Combined resulting corpus can be found at:
https://drive.google.com/open?id=0B1ItK6JlQ6ImRXAzMm1jSU9aOTA
