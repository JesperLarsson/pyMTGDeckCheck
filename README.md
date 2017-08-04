# About pyMTGDeckCheck
Imports a MTG deck list file and notifies you when each of your cards will rotate out of standard and verifies that your deck is standard legal. It should automatically support reprints and generally be pretty reliable.

Interfaces with magicthegathering.io and whatsinstandard.com to retrieve card data automatically without relying on a local database. All SDK dependencies should be downloaded and installed automatically.

# Instructions #
1. Download this repository from Github. Cllick "Clone or download" => "Download ZIP" or use a git client
2. Download python 3 from here (note that python 2 does not work as magicthegathering.io requires version 3 or greater): 
https://www.python.org/downloads
3. Export your deck from MTGO / tappedout.net /etc. Choose a basic text file as the file format
4. Run the script by drag-and-dropping your deck file on top of the script. A basic test deck file is included in the repository for you to test the script.
It's also possible to run it from the commandline and give your filename as the first argument like so: <pre>"pyMTGDeckCheck.py test_deck.txt"</pre> 

The program output should then look like this:

<pre>
=== 75 CARDS TOTAL IMPORTED ===
Aether Hub
Aether Meltdown
Blessed Alliance
Blighted Cataract
Cast Out
Censor
Disallow
Essence Scatter
Fumigate
Glimmer of Genius
Irrigated Farmland
Kefnet the Mindful
Prairie Stream
Pull from Tomorrow
Shielded Aether Thief
Supreme Will
Torrential Gearhulk
Approach of the Second Sun
Baral's Expertise
Dispel
Hour of Revelation
Negate
Oketra's Last Mercy

These cards rotate on Q4 2018:
        Aether Hub
        Aether Meltdown
        Cast Out
        Censor
        Disallow
        Essence Scatter
        Fumigate
        Glimmer of Genius
        Irrigated Farmland
        Kefnet the Mindful
        Pull from Tomorrow
        Shielded Aether Thief
        Supreme Will
        Torrential Gearhulk
        Approach of the Second Sun
        Baral's Expertise
        Hour of Revelation
        Negate
        Oketra's Last Mercy
These cards rotate on 2017-09-29T00:00:00.000Z:
        Blessed Alliance
        Blighted Cataract
        Prairie Stream
        Dispel
</pre>

# Troubleshooting #
The script should automatically download the magicthegathering.io libraries to your python directory. If that does not work out you may install them manully by opening a terminal in your python script folder (ex 'C:\Python3\Scripts') and running "pip install mtgsdk". You might have to add python to your PATH system variable if the python installer didn't.

# Source modifications #
If you have basic programming knowledge there is a configuration parameter that allows you to verify your deck against other formats (Modern/Legacy etc). You are free to change and distribute the source according to the GPL license.
