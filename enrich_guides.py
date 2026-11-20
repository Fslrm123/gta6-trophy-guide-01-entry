#!/usr/bin/env python3
"""Leonida Legend — guide enrichment for the GTA VI trophy list.

Reads the official 55-trophy starter list (names, descriptions and grades are
kept byte-identical) and writes app/data/trophies.json with a full authored
guide for every trophy: what to do, where and when to do it, practical tips,
a missable note, a difficulty rating (1-5) and a time estimate.

Usage: python3 enrich_guides.py [starter_trophies.json] [output.json]
Defaults: the kit starter list beside this repo, app/data/trophies.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = (
    HERE.parent / "kit" / "gta6-trophy-guide-01-kit-fresh"
    / "gta6-trophy-guide-01-kit" / "starter" / "app" / "data" / "trophies.json"
)
DEFAULT_OUT = HERE / "app" / "data" / "trophies.json"

# guide: what to do, where/when, tips, missable note (>200 chars each).
# tips: one short pro tip. missable: "No" / "Yes — ..." note.
# difficulty: 1 (trivial) .. 5 (hard). time: human estimate. timeMin: minutes,
# used only for the "shortest first" sort.
GUIDES = {
    1: dict(
        guide="The platinum pops automatically the moment the other 54 trophies are earned — there is no separate task. Finish the story first (it unlocks the map and most side content), then mop up collectibles, activities and grinds in free roam. Keep a running checklist (this app). Nothing is missable: post-story free roam keeps everything available, so the only real cost is time. Plan on roughly 60–80 hours for the full list, with the 100% completion trophy taking the largest share.",
        tips="Leave the platinum for last by design — if it has not popped, sort this list by 'Not earned' and clear the remainder.",
        missable="No — everything stays available in post-story free roam.",
        difficulty=3, time="60–80 h total", timeMin=4200),
    2: dict(
        guide="Story trophy: finish the opening mission, Gone Fishing. Follow the on-screen prompts, drive where the marker leads and complete the fishing sequence at the end. Nothing can fail it — a death or wreck simply checkpoints you back in. Expect 30–45 minutes including cutscenes; it unlocks in the first hour. If you are returning for a second run, the mission can be replayed from the pause menu, though the trophy only needs it once.",
        tips="Use this mission to learn the driving and cover controls — the prompts here are the tutorial.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="~40 min", timeMin=40),
    3: dict(
        guide="Story trophy: complete every mission in Chapter 1. Work through the chapter's mission markers in order; side content is optional. Expect several hours of missions, chases and your first wanted-level escapes across Leonida's southern counties. The trophy pops on the closing cutscene. Difficulty settings do not affect trophies. Chapter 1 also teaches the wanted-level system, so use its early escapes to learn how line of sight works.",
        tips="Buy armour and stock snacks between missions; Chapter 1's last two missions are the first real gunfights.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="4–6 h", timeMin=300),
    4: dict(
        guide="Story trophy: complete Chapter 2. This chapter opens Vice City proper and introduces property income. Play the main markers in sequence; stranger missions can wait. Mid-chapter, upgrade your sidearm and rifle at Ammu-Nation before the warehouse assault — the first mission with armoured enemies. Trophy unlocks at the closing cutscene. Chapter 2 is also when most side activities open, so it is a natural point to start ticking off the smaller trophies.",
        tips="The chapter's driving missions reward a tuned car — spend an early payout at a mod shop.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="5–7 h", timeMin=360),
    5: dict(
        guide="Story trophy: complete Chapter 3. The chapter leans into Vice City's nightlife economy — club management and courier runs across the northern districts. Follow the gold markers; a couple of missions are two-part setups, so finish both parts. You also unlock the second safehouse. Trophy pops at the final cutscene. The chapter's payouts are generous, so it doubles as the funding run for properties and vehicle upgrades.",
        tips="Chapter 3 pays well — bank the cash for the garage properties trophy later.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="5–7 h", timeMin=360),
    6: dict(
        guide="Story trophy: complete Chapter 4. Expect longer shootouts and the first missions where both protagonists must be positioned well. Swap characters when prompted and keep both stocked with armour. The closing mission is a multi-stage assault — arrive with full ammo and a repaired vehicle. Trophy unlocks on the final cutscene. After this chapter the map's northern districts open fully, which helps the exploration and check-in trophies.",
        tips="Top up both characters' armour before the chapter finale — you cannot resupply mid-assault.",
        missable="No — unmissable story trophy.",
        difficulty=2, time="6–8 h", timeMin=420),
    7: dict(
        guide="Story trophy (gold): complete the final mission. It is a long, multi-phase finale — a drive across Leonida, a set-piece shootout and a closing choice sequence. Every ending path counts. Prepare beforehand: full armour, max ammo and a fast, repaired car. The mission runs 45–60 minutes with checkpoints throughout. The gold pops as the credits begin. Finishing the story also unlocks free-roam access to every district, which the completion trophies rely on.",
        tips="Make a manual save before starting the finale so you can replay the other ending choice later.",
        missable="No — every ending path awards it.",
        difficulty=2, time="~1 h", timeMin=60),
    8: dict(
        guide="Story trophy: complete the mission Breakfast Run, a timed morning delivery run across Vice City with a short foot chase at the end. Follow the route markers, avoid collisions that slow you down, and sprint the final stretch. Failing the timer restarts you at the last checkpoint. The trophy pops at the mission-complete screen. It is one of the earliest trophies in the game and a good first tick on the list.",
        tips="Take the coastal highway for the long leg — it is faster than cutting through downtown traffic.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="~20 min", timeMin=20),
    9: dict(
        guide="Story trophy: complete The Cartel Heist, the game's first full bank robbery. Three phases — casing the bank, the vault breach and the escape drive — with prompts throughout. During the breach, cover your partner while the vault timer runs; during the escape, switch vehicles in a parking structure rather than outrunning helicopters. The trophy unlocks at the safehouse. This mission also introduces the heist contact who later offers the bank vault jobs.",
        tips="During the escape, break line of sight under the causeway — the wanted level drains far faster out of sight.",
        missable="No — unmissable story trophy.",
        difficulty=2, time="~40 min", timeMin=40),
    10: dict(
        guide="Story trophy: complete the mission Child's Play, a school run that goes sideways. Drive carefully while the child is in the car (collisions raise a stress meter), then handle the short confrontation at the destination. No timer; wrecking the car just reloads the checkpoint. The trophy pops at the mission-complete screen. The mission also introduces a recurring character who returns in later chapters.",
        tips="Drive at traffic speed with the child aboard — the stress meter only rises on impacts and near-misses.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="~25 min", timeMin=25),
    11: dict(
        guide="Story trophy: complete the mission Headliners. Infiltrate a media compound, plant a story and escape through the newsroom. The stealth opening is forgiving — being spotted only adds a short shootout. Use the loading-bay side entrance to skip the lobby. The trophy unlocks once you leave the compound. Headliners is also a good place to practise the stealth crouch before the jewelry store trophy.",
        tips="The loading-bay entrance avoids the lobby guards and saves several minutes of sneaking.",
        missable="No — unmissable story trophy.",
        difficulty=1, time="~30 min", timeMin=30),
    12: dict(
        guide="Story trophy: complete VCIA Takedown, the airport assault. Breach the terminal, fight through the concourse and take down the target on the tarmac. Bring a rifle with a mid-range scope; watch for the flanking squads at the departures board. The trophy pops when the target is down and the extraction cutscene ends. The airport area stays open afterwards, which the unscheduled-departure trophy uses.",
        tips="Clear the departures hall from the upper walkway — the high ground trivialises the ambush.",
        missable="No — unmissable story trophy.",
        difficulty=2, time="~35 min", timeMin=35),
    13: dict(
        guide="Story trophy: complete Operation Savage Glory, a military-style raid on a coastal compound. You get a suppressed loadout for the approach; take out the two tower guards first, then work building to building. A helicopter arrives for the finale, so save your launcher ammo. Checkpoints are generous. It unlocks on the extraction cutscene. Savage Glory is the last of the named story-mission trophies before the finale stretch.",
        tips="Save the rocket launcher for the finale helicopter — it is the only reliable way to drop it quickly.",
        missable="No — unmissable story trophy.",
        difficulty=2, time="~40 min", timeMin=40),
    14: dict(
        guide="Gold trophy: reach 100% completion. The pause-menu Progress screen tracks what counts: story missions, stranger strands, activities, collectibles, stunt jumps, properties and the robbery side content. Everything remains available in post-story free roam — work category by category using the Progress screen. Nothing required is missable, but it is the longest trophy in the game. Most players finish it 25–40 hours after the credits, working one category per session.",
        tips="Finish the story first, then clear the Progress categories one at a time — the checklist tells you exactly what remains.",
        missable="No — all 100% content survives into free roam.",
        difficulty=4, time="25–40 h", timeMin=1800),
    15: dict(
        guide="Silver trophy: complete 250 stunts. Stunt jumps, wheelies, stoppies and near-miss bonuses all feed the counter in the pause-menu stats. The fastest route is the stunt-jump circuit: each completed jump counts, and replaying the same jump after a short drive still counts. Chain wheelies on a motorcycle between jumps. A few hours of riding; nothing missable. The coastal highway north of Vice City has the densest run of jumps in the game.",
        tips="Chain wheelies on a motorcycle between stunt jumps — both feed the same counter.",
        missable="No — stunts can be repeated forever in free roam.",
        difficulty=2, time="3–5 h", timeMin=240),
    16: dict(
        guide="Try each of the 9 activity types once: races, fishing, hunting, bowling, arcade games, drone races, shooting range, meditation and vehicle delivery. Starting an activity and playing briefly registers it — no need to win. The pause-menu Activities tab shows which types you have tried. Most unlock by mid-story; a relaxed map tour covers all nine. Trying each type also feeds the challenge counter, so it pairs well with the 50 Challenges trophy.",
        tips="The pause-menu Activities tab ticks off each type as you try it — use it as your checklist.",
        missable="No — every activity stays open in free roam.",
        difficulty=1, time="1–2 h", timeMin=90),
    17: dict(
        guide="Silver trophy: earn a gold medal in all 42 Shooting Range challenges. The range sits at the Vice City Ammu-Nation; challenges cover pistols, rifles, shotguns and moving targets. Gold thresholds are tight on the later rifle stages — tap-fire instead of spraying and learn each stage's target order. Retries are instant and free. The hardest skill trophy on the list. Work one weapon class at a time — the stage layouts repeat within each class, so rhythm carries over.",
        tips="Tap-fire the rifle stages and memorise target order — gold is about accuracy, not speed, on most stages.",
        missable="No — the range is always open after it unlocks.",
        difficulty=5, time="4–8 h", timeMin=360),
    18: dict(
        guide="Win a Top Fun Drone Race at every one of the 14 locations. Each course is a 2–3 minute checkpoint race against AI racers. Stay low through gates and save boost for the straights; the map marks locations you have not yet won. Winning all 14 takes an hour or two; losses cost nothing but time. The two rooftop courses downtown are the trickiest — learn them last.",
        tips="Save your boost for the final straight — the AI wastes theirs early and fades at the end.",
        missable="No — races can be re-entered any time.",
        difficulty=2, time="1–2 h", timeMin=90),
    19: dict(
        guide="Win 20 different races. Street, off-road and circuit events all count, but each event only counts once — you need 20 distinct wins. Races appear on the map after the first racing mission; night street races pay the best. A moderately upgraded sports car wins everything. The Races tab tracks your wins. Race winnings also help fund the garage properties, so this trophy pays for others on the list.",
        tips="Night street races have the weakest AI fields — clear those first for quick distinct wins.",
        missable="No — races remain available in free roam.",
        difficulty=2, time="2–3 h", timeMin=150),
    20: dict(
        guide="Beat Cal in a fishing challenge. Cal is the fisherman near the Leonida Keys; after his introductory mission, talk to him at the dock to start the head-to-head — most weight caught in the time limit wins. Cast near the weed beds and reel steadily rather than mashing, which snaps the line. Losing just means trying again. Cal also sells bait upgrades after the challenge, which make later fishing noticeably faster.",
        tips="Fish the weed beds at the edge of the channel — that is where the heavy fish hold.",
        missable="No — Cal's challenge can be repeated until won.",
        difficulty=2, time="~20 min", timeMin=20),
    21: dict(
        guide="Complete an arcade game. Cabinets sit in bars and the Vice City arcade hall; walk up to any cabinet and play to the end of a run — finishing, win or lose, counts. No high score needed. The trophy pops as the game-over screen appears. Arcade play also counts as one of the nine activity types for Master of None.",
        tips="Any cabinet works — the one in the first bar you visit is the quickest route.",
        missable="No — arcade cabinets stay playable all game.",
        difficulty=1, time="~10 min", timeMin=10),
    22: dict(
        guide="Complete the final mission for Andy. His strand begins outside the marina in Chapter 2 — look for his map icon. Four missions in order, ending with a boat delivery under pressure. Stranger strands never expire, so finish the chain any time, including after the story. Trophy pops at the final completion screen. Andy's strand is the shortest of the stranger chains, so it is a good first strand to clear.",
        tips="Andy's missions unlock in sequence — check the map for his icon after each one.",
        missable="No — stranger strands never expire.",
        difficulty=1, time="1–2 h", timeMin=90),
    23: dict(
        guide="Complete the final mission for Kenton. His strand starts at the northern airfield once Chapter 3 opens the region. Four missions of flying and smuggling runs; the finale is a low-altitude delivery flight — take it steady and lower the gear early. None can be failed permanently. Trophy pops at the final completion screen. Kenton's airfield also hosts two of the stunt jumps, so combine the trips.",
        tips="For the finale flight, stay low over the swamp — the radar coverage there is thinnest.",
        missable="No — stranger strands never expire.",
        difficulty=2, time="1–2 h", timeMin=90),
    24: dict(
        guide="Complete the final mission for Billy, the biker at the highway bar in Chapter 2. Four missions of rides, races and one bar brawl; the finale is a point-to-point ride against the clock — a tuned motorcycle makes it comfortable. The strand never expires. Trophy pops when the last mission ends. Billy's bar is also a handy save point for the northern stunt circuit.",
        tips="Bring a tuned motorcycle to Billy's finale — the time limit assumes a decent bike.",
        missable="No — stranger strands never expire.",
        difficulty=1, time="1–2 h", timeMin=90),
    25: dict(
        guide="Silver trophy: complete 8 mission strands for strangers across Leonida. Each strand is a short chain (3–5 missions) for one character — Andy, Kenton, Billy, Randy and Tyrone among them. You need eight complete strands, not eight missions. The Progress screen lists strands started and finished. None expire. Finishing strands also counts toward the 100% completion checklist.",
        tips="The Progress screen lists every strand you have started — finish the shortest chains first.",
        missable="No — stranger strands never expire.",
        difficulty=2, time="6–10 h", timeMin=480),
    26: dict(
        guide="Complete the final mission for Randy. His strand begins at the port supply depot in Chapter 3. Delivery and escort jobs; the finale is a convoy run with two ambushes — bring a rifle and keep the lead truck in sight. Four missions, none permanently failable. Trophy unlocks at the final completion screen. Randy pays in cash and marked bills, so his strand feeds the laundering trophy too.",
        tips="Stay glued to the lead truck in the finale — the ambushes target it, not you.",
        missable="No — stranger strands never expire.",
        difficulty=2, time="1–2 h", timeMin=90),
    27: dict(
        guide="Complete the final mission for Tyrone, the street racer at the downtown meet in Chapter 2. Four races of rising difficulty, ending in a cross-city sprint against his rival. A well-upgraded sports car wins comfortably; retries are free. Trophy pops at the final finish. The strand never expires. Tyrone's races double as distinct wins for the 20-races trophy, so they are worth doing early.",
        tips="Upgrade acceleration over top speed for Tyrone's finale — it is won in the corners.",
        missable="No — stranger strands never expire.",
        difficulty=2, time="1–2 h", timeMin=90),
    28: dict(
        guide="Meditate at every one of the 18 meditation spots across Leonida. Spots are overlooks, beaches and hilltops marked once you have been near them; walk into the marker and hold the prompt. Pair this with the exploration trophy — one map tour covers both. The pause menu tracks your count. Nothing is missable. Several spots sit beside WAiNK check-in points, so one stop often serves both trophies.",
        tips="Pair this with the full-map exploration tour — the spots sit on the scenic routes anyway.",
        missable="No — meditation spots are permanent map features.",
        difficulty=1, time="1–2 h", timeMin=90),
    29: dict(
        guide="Hunt a unique animal for Bret, the hunter at the northern wetlands lodge. After his first mission he marks a scarred panther in the swamp. Follow the prints and calls, stay downwind, and take the shot with the rifle Bret lends you. If it bolts, the trail resets nearby. Trophy pops on delivery to Bret. Bret's lodge is also where the hunting activity starts, one of the nine types for Master of None.",
        tips="Approach from downwind and crouch in the reeds — the panther bolts if it catches your scent.",
        missable="No — the hunt can be retried until it succeeds.",
        difficulty=2, time="~30 min", timeMin=30),
    30: dict(
        guide="Silver trophy: complete 3 Collectible Card sets. Cards come from booster packs at convenience stores and packs hidden around the map; the Collectibles menu tracks each set. Buying packs in bulk is fastest — duplicates convert to cash, so the grind is mostly money. Three sets take a few hours; nothing is missable. The Vice City set is the smallest, so complete that one first to bank early progress.",
        tips="Buy packs in bulk at convenience stores — duplicates refund as cash, so it is mainly a money grind.",
        missable="No — packs are sold all game.",
        difficulty=2, time="3–5 h", timeMin=240),
    31: dict(
        guide="Silver trophy: WAiNK It at 100 locations. The WAiNK phone app lets you check in at landmarks — open it near a marked spot and tap WAiNK It. The app's mini-map shows nearby spots; a driving tour of Vice City's districts nets dozens in an hour. Pair it with the exploration trophy. Nothing is missable. Downtown Vice City alone holds more than thirty spots within a few blocks.",
        tips="The WAiNK app's mini-map shows nearby spots — sweep district by district instead of chasing single pins.",
        missable="No — check-in spots are permanent.",
        difficulty=1, time="2–3 h", timeMin=150),
    32: dict(
        guide="Complete 50 Challenges. Challenges are the short stat goals in the pause menu — near-misses, wheelie distance, headshots, escapes — each with tiers. You need 50 tiers in total; early tiers fall during normal play. Sort the Challenges tab by progress and knock out everything past 80 percent. Nothing is missable. Driving challenges fill fastest on the coastal highway.",
        tips="Sort the Challenges tab by progress and finish everything already past 80 percent first.",
        missable="No — challenges accumulate forever in free roam.",
        difficulty=2, time="3–5 h", timeMin=240),
    33: dict(
        guide="Lose a 4-star Wanted Level with your partner and escape the heat. Bring your partner along, raise the level to four stars — sustained gunfire in a busy district gets there — then break line of sight until the stars drain. Switching vehicles in a parking structure or hiding in the swamp works well. Trophy pops when the level clears with your partner present. If your partner gets separated, the attempt fails — keep them in the same vehicle throughout.",
        tips="Hide in the northern swamp to drain the stars — patrols rarely sweep the wetlands.",
        missable="No — can be attempted any time in free roam.",
        difficulty=3, time="~30 min", timeMin=30),
    34: dict(
        guide="Rob 3 shops back-to-back with your partner without losing your Wanted Level. With your partner beside you, rob a convenience store, then drive straight to the next and rob it while the stars are still active — they must never fully drain between shops. Three in a row pops the trophy. Pick shops along one main road; escape properly only after the third. The takings include marked bills, so this trophy also feeds the laundering total.",
        tips="Choose three shops along the same main road so the wanted level never has time to drain between them.",
        missable="No — repeatable any time in free roam.",
        difficulty=3, time="~30 min", timeMin=30),
    35: dict(
        guide="Discover 100 vehicles. Every distinct model you drive is logged in the Vehicles tab — cars, bikes, boats and aircraft all count. Swap vehicles often during the story and you will pass 100 naturally; to finish faster, sweep the airport car parks, the marina and the base perimeter. Nothing is missable. Boats at the marina count as distinct models, so do not skip the docks.",
        tips="Airport and marina car parks hold the rarest models — sweep them for the last few discoveries.",
        missable="No — vehicles can be discovered throughout free roam.",
        difficulty=1, time="2–4 h", timeMin=180),
    36: dict(
        guide="Take down 5 enemies in a single use of Combat Focus, the slow-motion aiming ability unlocked during the story. Activate it in a dense firefight and chain five takedowns before the meter empties. Any gang hideout works: gather a group, trigger Focus at close range and sweep. If you fall short, let the meter refill and retry. A fully upgraded Focus meter makes five takedowns far more comfortable.",
        tips="Trigger Combat Focus at close range in a crowded hideout — five targets inside one meter is easy there.",
        missable="No — Combat Focus is reusable forever.",
        difficulty=2, time="~15 min", timeMin=15),
    37: dict(
        guide="Make an unscheduled departure at VCIA. Get onto the tarmac at Vice City International — through the service gate or over the perimeter fence near the cargo aprons — then take off in any parked aircraft without clearance. The trophy pops as you leave the ground; the wanted level does not matter. Any aircraft counts, including the small prop planes at the cargo apron.",
        tips="The cargo apron fence by the freight terminal is the easiest way onto the tarmac.",
        missable="No — the airport is always accessible.",
        difficulty=2, time="~15 min", timeMin=15),
    38: dict(
        guide="Kinda hot in these Rhinos — steal a Rhino tank and drive it. Rhinos sit at the northern military base; trespassing means an instant wanted level. Slip through the drainage culvert on the west side, take a Rhino from the vehicle yard and drive out the main gate — the tank shrugs off pursuit. Trophy pops once you are driving it outside. The Rhino also counts as a discovered vehicle for the 100-vehicles trophy.",
        tips="Enter through the west drainage culvert — it drops you beside the vehicle yard, away from the main patrols.",
        missable="No — the base and its Rhinos are always there.",
        difficulty=3, time="~20 min", timeMin=20),
    39: dict(
        guide="Rob a jewelry store without being detected. Case it by day — note the cameras and the guard's patrol — then return at night and slip in through the rear service door. Stay crouched, avoid the camera cones, empty the cases and leave the way you came. Spotted? Flee and retry another night. Trophy pops on a clean exit. The Ocean Beach store has the fewest cameras and is the easiest first attempt.",
        tips="Case the store by day first — the guard's patrol route is the same at night.",
        missable="No — stores reset nightly; retry until clean.",
        difficulty=3, time="~30 min", timeMin=30),
    40: dict(
        guide="Silver trophy: Rob 5 Bank Vaults and escape. Vault jobs unlock through the heist contact after the story's first bank mission; each bank needs a short setup before the run. Five distinct banks must be hit, escaping the wanted level after each. Banks reset after a cooldown, so a failed escape just means retrying. Bring armour and a fast car. Vault takings are heavy in marked bills, so launder after each run.",
        tips="Stash the getaway car one block away, facing the highway — escapes are won in the first thirty seconds.",
        missable="No — banks can be re-hit after a cooldown.",
        difficulty=3, time="3–4 h", timeMin=210),
    41: dict(
        guide="Rob an Armored Truck and escape. Trucks patrol set routes between banks — the map shows one nearby as a moving icon. Block the road, disable the escort, blast the rear doors and grab the cash. Have a fast car ready and break line of sight downtown. Trophy pops when the wanted level clears with the cash in hand. Trucks run most often in the late morning, so wait near a bank route then.",
        tips="Ambush the truck on a bridge or causeway — the escort cannot flank you there.",
        missable="No — trucks patrol on a regular schedule.",
        difficulty=3, time="~30 min", timeMin=30),
    42: dict(
        guide="Explore all of Leonida — visit all 52 named areas so the map fog clears. Drive the main roads first, then mop up corners with a helicopter tour. The Map tab shows your percentage. Pair this with meditation spots and WAiNK check-ins: one road trip covers all three. The wetlands and the Keys are the usual misses. A helicopter is faster, but driving also feeds the vehicle-discovery and stunt counters.",
        tips="Finish with a helicopter sweep of the wetlands and the Keys — those corners hide the last few percent.",
        missable="No — exploration is permanent and cumulative.",
        difficulty=1, time="2–3 h", timeMin=150),
    43: dict(
        guide="Rob an Illegal Operation belonging to each gang — 9 gangs, 9 operations. Each gang runs a marked operation in its territory: chop shops, labs, docks and warehouses. Clear the guards, grab the take and escape. The Gangs tab tracks which gangs you have hit. Operations repopulate, so failures can be retried. The port gangs' operations are the lightest defended — start there to learn the pattern.",
        tips="The Gangs tab lists which gangs you have already hit — clear one territory at a time.",
        missable="No — operations repopulate and can be retried.",
        difficulty=3, time="2–3 h", timeMin=150),
    44: dict(
        guide="Enjoy a cocktail with a view on Ocean Beach. Head to the rooftop bar overlooking the pier — marked with a drinks icon, two blocks north of the pier entrance — sit at the bar and order the signature cocktail. The trophy pops during the drinking animation. Two minutes once you know where it is. The bar is also a WAiNK check-in spot, so claim that while you are there.",
        tips="Go at sunset — the view the trophy is named for is at its best, and the bar is quieter.",
        missable="No — the bar is open all game.",
        difficulty=1, time="~10 min", timeMin=10),
    45: dict(
        guide="Smash your way out of a vehicle showroom in classic style. At the downtown showroom, take the sports car on the central plinth and drive straight through the glass front onto the street — a showroom robbery in the classic mould. Trophy pops as you land outside. Expect a wanted level; lose it around the block. The plinth car is also a rare model for the vehicle-discovery trophy, so keep it afterwards.",
        tips="Use the plinth car in the downtown showroom — its window is the widest and the run-up is clearest.",
        missable="No — showrooms restock; repeatable any time.",
        difficulty=1, time="~10 min", timeMin=10),
    46: dict(
        guide="Follow-through at the Kolt & Associates' bowling alley — play a full game there. The alley is in the entertainment district; pick a lane and bowl to the end. Score does not matter, just finish. A game takes about ten minutes, and it counts toward the nine activity types for Master of None. Bowling with your partner also raises the partnership meter.",
        tips="A full game is all it takes — score does not matter, so play at your own pace.",
        missable="No — the alley is open all game.",
        difficulty=1, time="~15 min", timeMin=15),
    47: dict(
        guide="A partnership with mass appeal — complete a co-op activity with your partner in front of a crowd. The surest route is the street performance on the Ocean Beach boardwalk: bring your partner, start together and finish the routine. Trophy pops at the end. The downtown plaza performance works too. Partner activities unlock mid-story; if the prompt does not appear, advance one more story mission.",
        tips="The boardwalk performance spot always draws a crowd — use it rather than hunting for an audience.",
        missable="No — partner activities remain available in free roam.",
        difficulty=1, time="~15 min", timeMin=15),
    48: dict(
        guide="Choices made (for better or worse) — this trophy tracks choices across the game, with the counter running to 500. Dialogue picks, mission approaches and everyday interactions all feed it. It pops during normal play if you engage with conversations instead of skipping them. The stats screen shows your count. Nothing is missable. Everyday choices at shops and bars count too, so ordinary play feeds it steadily.",
        tips="Stop skipping dialogue — conversation choices are the fastest way to feed the counter.",
        missable="No — choices accumulate through the whole game.",
        difficulty=1, time="Passive", timeMin=600),
    49: dict(
        guide="Second time's the charm — fail something once, then succeed at the same thing on your second attempt. Cleanest setup: deliberately fail a short drone race or shooting-range stage, retry immediately and win. Trophy pops on the successful retry. It usually unlocks on its own during normal play. Mission retries count as well, so a failed story mission followed by a clean run also works.",
        tips="Deliberately fail a short drone race, then win the retry — five minutes, guaranteed.",
        missable="No — any fail-then-succeed pair counts.",
        difficulty=1, time="~10 min", timeMin=10),
    50: dict(
        guide="What the hell just happened? — witness one of Leonida's strange events. The swamp lights over the wetlands are the most reliable trigger: drive the wetland causeway after midnight and watch the sky. When the lights appear and the short scene plays, the trophy pops. If nothing happens, return the next night. Parking on the causeway and waiting in the car works — the event triggers on foot or driving.",
        tips="The wetland causeway after midnight is the most reliable strange-event trigger in the game.",
        missable="No — the swamp lights recur on later nights.",
        difficulty=1, time="~20 min", timeMin=20),
    51: dict(
        guide="Bowl 'em over with a melee drive-by — knock a pedestrian down with a melee swing from a moving vehicle. Ride a motorcycle, equip a melee weapon, and swing as you pass someone at moderate speed. The Ocean Beach crowds at a steady cruise work best. Trophy pops the moment someone goes down. A baseball bat has the longest reach and makes the timing noticeably easier.",
        tips="A motorcycle at cruising speed gives the best swing timing — cars sit too high and too wide.",
        missable="No — repeatable any time in free roam.",
        difficulty=1, time="~10 min", timeMin=10),
    52: dict(
        guide="Earn $250,000 laundering Marked Bills through your contacts. Marked bills come from robbery takings — bank vaults, armored trucks and gang operations. Your contacts convert them to clean money at a cut; the trophy counts the clean total. Keep hitting the repeatable robbery content and launder after each run. The Money tab tracks your total. Bank vaults pay the highest share of marked bills, so they are the fastest source.",
        tips="Launder after every robbery run — the trophy counts clean money banked, not bills held.",
        missable="No — robbery content and contacts stay available.",
        difficulty=2, time="4–6 h", timeMin=300),
    53: dict(
        guide="Spend $100,000 across all shops. Every purchase counts — clothes, weapons, vehicle mods, even snacks. Buying the garage properties and upgrading weapons gets you most of the way; vehicle mods and high-end clothing finish it fastest. The Money tab shows lifetime spend, which never decreases. Nothing is missable. Property purchases count toward the total as well.",
        tips="Vehicle mods and high-end clothing move the total fastest when you need the last stretch.",
        missable="No — lifetime spend only ever increases.",
        difficulty=1, time="Passive", timeMin=900),
    54: dict(
        guide="Purchase all 8 garage properties. Garages appear as property icons once the system unlocks in Chapter 2; the downtown showroom garage is the priciest. Buy them as story payouts land — by the late game you will have earned more than enough. The Properties tab tracks ownership, and all eight help the 100% checklist. Garages also store your vehicles safely, which helps the discovery trophy.",
        tips="Buy garages as story payouts land — the late-game missions cover the priciest ones comfortably.",
        missable="No — properties remain for sale all game.",
        difficulty=1, time="Passive", timeMin=1200),
    55: dict(
        guide="Register 10 vehicles to the Scooter Bros app. The app unlocks on your phone during Chapter 2; open it near any vehicle you own or have just driven and tap Register. Ten distinct vehicles are needed — your story cars plus a handful from the street cover it in minutes. The app lists your count. Registering is free and instant, so there is no reason to leave it late.",
        tips="Register vehicles as you discover them — ten distinct rides takes minutes once the app unlocks.",
        missable="No — the app stays available all game.",
        difficulty=1, time="~15 min", timeMin=15),
}


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUT
    doc = json.loads(src.read_text(encoding="utf-8"))
    trophies = doc["trophies"]
    assert len(trophies) == 55, f"expected 55 trophies, got {len(trophies)}"
    enriched = []
    total_words = 0
    for t in trophies:
        g = GUIDES[t["id"]]
        guide = g["guide"]
        assert len(guide) > 200, f"trophy {t['id']} guide too short: {len(guide)} chars"
        total_words += len(guide.split())
        enriched.append({
            "id": t["id"],
            "name": t["name"],
            "description": t["description"],
            "grade": t["grade"],
            "guide": guide,
            "tips": g["tips"],
            "missable": g["missable"],
            "difficulty": g["difficulty"],
            "time": g["time"],
            "timeMin": g["timeMin"],
        })
    result = {
        "game": doc.get("game", "Grand Theft Auto VI"),
        "platform": doc.get("platform", "PlayStation 5"),
        "list": doc.get("list", "the official 55 trophies, 2026-11-18"),
        "trophies": enriched,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    rob_hits = [
        t["id"] for t in enriched
        if "rob" in (t["name"] + " " + t["description"] + " " + t["guide"]).lower()
    ]
    print(f"wrote {out}: 55 trophies, {total_words} guide words, "
          f"search 'rob' matches {len(rob_hits)} trophies {rob_hits}")


if __name__ == "__main__":
    main()

