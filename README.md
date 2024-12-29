# SquadRelated

Code that is related to Squad Game

## Rotation

Based on latest layer rule for Squad and POST.

Mainly designed by:

- | Mode                   | Prob(Approximately) |
	| ---------------------- | ------------------- |
	| AAS/RAAS               | 45                  |
	| Invasion               | 15                  |
	| Skirmish               | 10                  |
	| TC                     | 25                  |
	| Insurgency/Destruction | 5                   |

- Same level won't appear twice in 10.
- Invasion/Insurgency/Destruction mode won't appear twice in 5.
- Time for layer is not at daytime won't appear twice in 5.
- Layer size is not large won't appear twice in 3.
- Battle group type is not same won't appear twice in 5.

Requirement:

- Download sheet "Map Layers", "BG Layer Availability" as .csv file from OWI/Squad e.g https://docs.google.com/spreadsheets/d/1A3D4zeOS8YxoEYrWcXa8edBCG_EUueZK9cX2oFMLY9U/edit?gid=1796438364#gid=1796438364 and place them in Rotation folder.

To run:

Clone the res, enter the Rotaion folder and run the python file

```bash
git clone https://github.com/MonsterXia/SquadRelated.git
cd SquadRelated/Rotation
python Rotation.py
```

**Result**

Result will be available at ./Rotation/LayerRotation.cfg

**Advance Usage**

Adjust the WEIGHT_* in thr front to generate at different weight

Modify the stack_capacity passed in the candidate_level_check() and balance_check() to apply different number for not appear twice for rules, respectively.

## RandomRank[Abandoned]

If you are searching for tools to make layers in rotation randomly, dowanload randomRank and open it in Your IDE.

Default original rotation root is in randomRank/src/com/monsterxia/simpletry/texttorandom/LayerRotation.cfg

Default target rotation root is in randomRank/src/com/monsterxia/simpletry/texttorandom/LayerRotation.cfg

If you want to change the cfgs' root, change here and rebuild to run

![root](https://s2.loli.net/2023/04/17/VEto4SB2AzaJlcD.png)
