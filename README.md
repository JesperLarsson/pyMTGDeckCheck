# pyMTGDeckCheck
Imports MTG deck list and notifies you when each of your cards will rotate out of standard and if your deck is standard legal. Retrieves card data from magicthegathering.io and whatsinstandard.com

# Instructions #
1. Download python 3 from here: https://www.python.org/downloads/
2. Install magicthegathering.io library by opening a terminal in your python script folder (ex 'C:\Python3\Scripts') and running pip install mtgsdk. You might have to add python to your PATH system variable
3. Export your deck from MTGO / tappedout.net /etc. Choose a basic text file as the format
4. Run the script from the commandline and give your filename as the first argument like so: "pyMTGDeckCheck.py test_deck.txt". A basic test deck file is included for your use.

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
