### Alexa Skill and Google Action Translations

The two files in this folder contain the phrases and template strings that are used to control the phrases that invoke the voice actions and the voice responses.

##### AlexaIntentStrings.json

This is a combined file that defines the invocation phrase and sample utterances that are used to trigger intents.

Each section corresponds to a specific version of the Skill or Action available in the stores. The important bits that can use translation would be the  *"invocationName"* and the phrases under the *"samples"* within each intent.

##### AlexaSkillResponseStrings.json

This file contains the template strings that are used to construct responses spoken by the voice assistant. They are divided into *Static*, *Measure*, *Error*, and *Time* sections.

- **Static** - Raw text strings that do not contain any placeholders or variables
- **Measure** - These strings contain placeholders that will be replaced by value from the printer. For example the template string "{0} is currently {1}" will be read back as "Your Printer is currently Printing"
- **Error** - These are template strings for any error messages that could be generated
- **Time** - These are time duration words in a specific language

You can see that there is a "default" tag with all of the strings defined, as well as specific elments for each region. If a phrase is not found under one of the specific locales, it will fallback to using the default version of the template (i.e. English).

##### Contributing

In each file you should be able to see how the different languages are separated. I would love any help getting these into other languages which I will then quickly use to deploy the skill/action to the various regions. So far they have rejected versions that have used English resposnes in non-English locales.

I've taken a stab at it using Google Translate but I'm sure to a native speaker some of these will be hilariously wrong, so any help is appreciated!

If you're interested in helping, you can either edit in-line to create a pull-request into the *skill_translations* branch, or clone/edit/commit/push through a standard Git workflow.

##### Questions

Please leave a comment on Issue #5 if you have any issues or questions. You can also reach me @johnnyruz on the OctoPrint Community Forum.
