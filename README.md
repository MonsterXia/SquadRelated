# SquadRelated

Code that is related to Squad Game

## Tools

### Rotation

Based on latest layer rule for Squad and POST.

**Overall Mode Probability**


| Mode                   | Prob(Approximately) |
| ---------------------- | ------------------- |
| AAS/RAAS               | 69                  |
| Invasion               | 12                  |
| Skirmish               | 6                   |
| TC                     | 9                   |
| Insurgency/Destruction | 4                   |

**Mainly pre-defined rules**

- Level
    - Same level won't appear twice in 10.

- Layer
    - Invasion/Insurgency/Destruction mode won't appear twice in 6.
    - Skirmish/TC mode won't appear twice in 5.
    - If the mode is not AAS/RAAS, won't appear twice in 2, i.e. at least there is a RAAS/AAS layer in 2.
    - Time for layer is not at daytime won't appear twice in 5.
    - Layer size is not large won't appear twice in 3.

- Factions
    - Battle group type is not balance won't appear twice in 5.


Requirement:

- Download sheet "Map Layers", "BG Layer Availability" as .csv file from OWI/Squad e.g https://docs.google.com/spreadsheets/d/1A3D4zeOS8YxoEYrWcXa8edBCG_EUueZK9cX2oFMLY9U/edit?gid=1796438364#gid=1796438364 and place them in Rotation folder.

To run:

Clone the res, enter the Rotaion folder and run the python file

```bash
git clone https://github.com/MonsterXia/SquadRelated.git
cd SquadRelated/Tools/Rotation
python Rotation.py
```

**Result**

Result will be available at ./Tools/Rotation/LayerRotation/\*.cfg

**Advance Usage**

Adjust the WEIGHT_* in the front to generate at different weight

Modify the stack_capacity passed in the candidate_level_check() and balance_check() to apply different number for not appear twice for rules, respectively.

### POST

#### Assessment toolkit

Designed for Prep/POST assessment.

To get a random grenade/LAT/HAT equipment.

**Update**

Changing the requirement:

Modify grenade_must, LAT_must, HAT_must

Add more equipment:

Modify grenade_random,LAT_random, HAT_random

**Usage**

Download .exe file from ./Tools/POST/'Assessment toolkit'/dist/

**Advance Usage**

Change icon:

Replace the logo.ico and run the get_logo_bitmap.py to update icon's bitmap.

Forming the .exe file:

```bash
cd ./Tools/POST/'Assessment toolkit'
pyinstaller --onefile  --noconsole --icon=logo.ico '.\Assessment toolkit.py'
```

### RandomRank[Abandoned]

If you are searching for tools to make layers in rotation randomly, dowanload randomRank and open it in Your IDE.

Default original rotation root is in randomRank/src/com/monsterxia/simpletry/texttorandom/LayerRotation.cfg

Default target rotation root is in randomRank/src/com/monsterxia/simpletry/texttorandom/LayerRotation.cfg

If you want to change the cfgs' root, change here and rebuild to run

![root](https://s2.loli.net/2023/04/17/VEto4SB2AzaJlcD.png)
