Check `summer_updates` for updated markov code (in the notebook).

#####################
#####    Data:   ####
#####################
chords.json: nested dict
- first level is the chord
	- second level is the bass note for that chord, containing the
	pitch values of that chord+bass combination
	- pitch values are the column labels in the dataset.

data.json: nested dict
- same structure as chords.json
- instead of pitch values (strings), it contains the MIDI value

encoded.csv: 
- original dataset, but pitch_x values are changed from YES->1 and NO->0.

#######################

Untitled1.ipynb is the scratchwork for updating the markov code.
It should contain the code for:
- creating `data.json` and `encoded.csv`
- the updated markov classes (Chain, prefix)
- model training/input
- MIDI generation and inline player
	- Note: the player does not work in jupyterlab, 
		and only shows up using the original notebook workflow.

Updates:
- markov model now generates with both starting chord and bass tuple
 (rather than previously having a separate model for chord and bass). 
- the MIDI generation force adds the defined "first" chord/bass as the first
 note, which for some reason did not happen before. 
- changes to the logic handling the repeat chord sequences

Notes:
- when generating `data.json` the chord midi/pitch values might be slightly 
off since it uses the first instance of a chord/bass pair. this means that
the MIDI values for the chord may be off since the first instance might have
a transition note included. 
- I gathered all chord/bass pairs and their pitch values and there's a lot
of variance in the resulting MIDI pitches. Making this more robust might 
improve the markov model generation.
- Because the code has been modified drastically for the Bach chorale dataset,
it might work a little wonky with the alice_oz.txt data. it might be worth using
the original markov code (which it worked best with) along with the bach markov
code, so that there are two different "models" that the students work with.


