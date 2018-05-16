


## FSL Feat 3 Column Format


 https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT/UserGuide                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        #

 For a single-event experiment with irregular timing for the stimulations, a custom file can be used.
 With Custom (1 entry per volume), you specify a single value for each timepoint. The custom file should be a raw
 text file, and should be a list of numbers, separated by spaces or newlines, with one number for each volume
 (after subtracting the number of deleted images). These numbers can either all be 0s and 1s, or can take a range of
 values. The former case would be appropriate if the same stimulus was applied at varying time points; the latter would
 be appropriate, for example, if recorded subject responses are to be inserted as an effect to be modelled. Note that
 it may or may not be appropriate to convolve this particular waveform with an HRF - in the case of single-event, it is.

 For even finer control over the input waveform, choose Custom (3 column format). In this case the custom file consists
 of triplets of numbers; you can have any number of triplets. Each triplet describes a short period of time and the value
 of the model during that time. The first number in each triplet is the onset (in seconds) of the period,
 the second number is the duration (in seconds) of the period, and the third number is the value of the input during
 that period. The same comments as above apply, about whether these numbers are 0s and 1s, or vary continuously.
 The start of the first non-deleted volume correpsonds to t=0.
