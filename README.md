# layout-signalling-scheme
A model railway signalling system for my layout written in Python for the Raspberry Pi with a DCC control of signals and points 
via the Pi-SPROG-3 DCC Command station and train detection via the GPIO ports on the Pi.

This has been created to provide a representation of my layout, complete with points, signals and "track occupancy" sections
The DCC interface drives a DCC Accessory Bus bus to provide digital control of all signals and points out on the layout. 
The GPIO interface allows external train detectors such as the BlockSignalling BOD2-NS to be connected in via opto-isolators.

All of the functions for creating and managing 'signals', 'points' and 'sections' have been developed as a Python Package 
to promote re-use across other layouts. This includes functions to support the interlocking of signals and points to enable 
fully prototypical signalling schemes to be developed. The signals and points opjects can be easily mapped to one or more DCC 
addresses in a manner that should be compatible with the majority of DCC signal/points decoders currently on the market. 
Track sensors can also be easily integrated (via the Raspberry Pi's GPIO interface) to enable full automatic control.

These core 'library'functions are now in a seperate repository (https://github.com/johnrm174/model-railway-signalling)- which
I plan to publish as a standalone Python Package in PyPI soon

As far as the code is concerned, I've tried to keep it simple - and readable to those that aren't intimately familiar with
some of the "advanced" aspects of the python language (e.g. I've avoided most of the object-oriented constructs where possible)

To give it a go, just clone the repository and and run 'my_layout'. This is still very much work in progress but should give 
a good example of how a fully interlocked (and relatively complex) signalling system can be built using the generic functions 
provided by the 'model-railway-signalling' Package. As my layout is still DC (rather than DCC) it also includes layout power 
switching. At the moment I have no plans to include this as a feature in the core package.

Comments and suggestions welcome - but please be kind - the last time I coded anything it was in Ada96 ;)
