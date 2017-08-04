# About pyMTGDeckCheck
Imports a MTG deck list file and notifies you when each of your cards will rotate out of standard and verifies that your deck is standard legal. It should automatically support reprints and generally be pretty reliable.

Interfaces with magicthegathering.io and whatsinstandard.com to retrieve card data automatically without relying on a local database. All SDK dependencies should be downloaded and installed automatically.

# Instructions #
1. Download this repository from Github. Cllick "Clone or download" => "Download ZIP" or use a git client
2. Download python 3 from here (note that python 2.X is not supported by magicthegathering.io SDK so it will not work): 
https://www.python.org/downloads
3. Export your deck from MTGO, tappedout.net or any other common tool. Choose a basic text file as the file format
4. Run the script by drag-and-dropping your deck file on top of the script. A few deck files are included in the repository for you to test the script. It's also possible to run it from the commandline if you prefer.

The program output should then look something like this:

<pre>
=== 77 CARDS TOTAL IMPORTED ===
Aether Hub
Attune with Aether
Blossoming Defense
Bristling Hydra
Rhonas the Indomitable
Harnessed Lightning
Electrostatic Pummeler
Sage of Shaila's Claim
Sheltered Thicket
Invigorated Rampage
Voltaic Brawler
Game Trail
Servant of the Conduit
Built to Smash
Glorybringer
Appetite for the Unnatural
Deadlock Trap
Woodcutter's Grit
Brute Strength
Magma Spray
Lathnu Hellion
Prowling Serpopard

These cards rotate Q4 2018:
  Aether Hub
  Attune with Aether
  Blossoming Defense
  Bristling Hydra
  Rhonas the Indomitable
  Harnessed Lightning
  Electrostatic Pummeler
  Sage of Shaila's Claim
  Sheltered Thicket
  Invigorated Rampage
  Voltaic Brawler
  Servant of the Conduit
  Built to Smash
  Glorybringer
  Appetite for the Unnatural
  Deadlock Trap
  Brute Strength
  Magma Spray
  Lathnu Hellion
  Prowling Serpopard
These cards rotate 2017-09-29:
  Game Trail
  Woodcutter's Grit
Your deck seems to be valid

Press enter to exit
</pre>

Here is an example of an invalid deck and the errors
<pre>
Too many copies of 'Black lotus' (42), only 4 copies are allowed
=== 45 CARDS TOTAL IMPORTED ===
Too few cards in total (45)
Censor
Void Shatter
Black Lotus
   Not Standard legal!
Doubling Season
   Not Standard legal!

These cards rotate Q4 2018:
  Censor
These cards rotate 2017-09-29:
  Void Shatter
Your deck is not valid
</pre>

# Troubleshooting #
The script should automatically download the magicthegathering.io libraries to your python directory. If that does not work out you may install them manully by opening a terminal in your python script folder (ex 'C:\Python3\Scripts') and running "pip install mtgsdk". You might have to add python to your PATH system variable if the python installer didn't.

# Source modifications #
If you have basic programming knowledge there is a configuration parameter that allows you to verify your deck against other formats (Modern/Legacy etc). You are free to change and distribute the source according to the GPL license.
