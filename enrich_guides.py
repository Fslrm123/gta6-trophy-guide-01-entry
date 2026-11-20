#!/usr/bin/env python3
"""Enrich trophies.json with full authored guides. Names/ids/descriptions/grades untouched."""
import json, pathlib

SRC = pathlib.Path.home() / "workspace/makefun/kit/gta6-trophy-guide-01-kit/gta6-trophy-guide-01-kit/starter/app/data/trophies.json"
DST = pathlib.Path.home() / "workspace/makefun/gta6-trophy-guide-01-entry/app/data/trophies.json"

GUIDES = {}

GUIDES[1] = dict(
    guide=("The platinum pops the moment the other 54 trophies are in your cabinet — there is no separate task. "
           "Treat the whole list as a route: finish the story first (it unlocks the full map, both protagonists' "
           "abilities and most businesses), then sweep activities, collectibles and the 100% checklist. "
           "Keep a manual save before the final mission in case any choice-based trophy needs a second run."),
    tips="Difficulty and time are the sum of the list: expect 60-90 hours for a first platinum run.",
    missable="No — free roam continues after the credits and almost everything stays available.",
    difficulty=4, time="60-90 h")

GUIDES[2] = dict(
    guide=("Story trophy, unmissable. Gone Fishing is the game's opening mission: it introduces Lucia and Jason, "
           "the partner-switch mechanic and basic driving on the way to the coast. Simply play through the "
           "tutorial beats — follow the markers, take the boat out, and finish the fishing sequence. "
           "The trophy unlocks as the mission-complete screen fades."),
    tips="Do not rush the boat section; the game teaches steering and throttle control you will need for races later.",
    missable="No — first mission of the story.",
    difficulty=1, time="~20 min")

GUIDES[3] = dict(
    guide=("Story trophy, unmissable. Chapter 1 covers the couple's first scores around Vice City and ends with a "
           "set-piece that puts the heat on both of them. Play every gold mission marker in order; side content "
           "can wait. The trophy pops at the chapter-end cutscene, and Chapter 2's opening unlocks the northern "
           "half of Leonida for free roaming."),
    tips="Bank your cash and buy a safehouse garage before the chapter finale so early earnings are not lost to deaths.",
    missable="No — awarded for completing Chapter 1.",
    difficulty=1, time="4-6 h")

GUIDES[4] = dict(
    guide=("Story trophy, unmissable. Chapter 2 leans into the drug-running side of the operation — smuggling runs, "
           "stash houses and your first real taste of the Marked Bills laundering loop. Complete the chapter's main "
           "missions in sequence; the trophy unlocks when the final Chapter 2 mission wraps. "
           "This is also where the contacts who launder Marked Bills (needed for Dime on the Dollar) first appear."),
    tips="Start laundering Marked Bills whenever a contact offers it — the $250,000 target is cumulative and slow to grind late.",
    missable="No — awarded for completing Chapter 2.",
    difficulty=1, time="6-8 h")

GUIDES[5] = dict(
    guide=("Story trophy, unmissable. Chapter 3 is the Vice City chapter: neon, clubs, and the duo muscling into "
           "the city's nightlife economy. Finish its main missions to earn the trophy at the chapter's closing scene. "
           "Several shop-robbery and jewelry-store opportunities open up here, so it is a good moment to start on "
           "Retail Therapy and Sneakthief between missions."),
    tips="Night-time Vice City is when shop takings are highest — rob shops after dark for better payouts.",
    missable="No — awarded for completing Chapter 3.",
    difficulty=1, time="6-8 h")

GUIDES[6] = dict(
    guide=("Story trophy, unmissable. Chapter 4 raises the stakes with statewide jobs and the first heavy military "
           "hardware on the streets — the same Rhinos you will face for Challenging Tank. Complete the chapter's "
           "missions to unlock the trophy. By now both protagonists should have upgraded Combat Focus and a decent "
           "arsenal; the endgame is balanced around them."),
    tips="Stock up on armor and heavy weapons before the chapter's final stretch; supply runs get long.",
    missable="No — awarded for completing Chapter 4.",
    difficulty=2, time="6-9 h")

GUIDES[7] = dict(
    guide=("Gold story trophy. Complete the final mission of the main story — the last gold marker on the map. "
           "The finale is a multi-stage job that uses both protagonists, partner switching and everything you have "
           "built up, so go in with full armor, your best weapons and a fast getaway car parked nearby. "
           "The trophy unlocks during the ending sequence, and free roam resumes afterwards for cleanup."),
    tips="Make a separate manual save right before starting the finale — choices near the end can affect Actions Speak Louder progress.",
    missable="No — awarded for finishing the story; the world stays open afterwards.",
    difficulty=2, time="1-2 h (finale)")

GUIDES[8] = dict(
    guide=("Story mission trophy, unmissable. Breakfast Run is an early job built around a morning pickup that goes "
           "sideways — expect a short drive, a tense handoff and a quick escape. Follow the markers, keep the "
           "vehicle in one piece, and finish the delivery. The trophy pops on the mission-complete screen."),
    tips="The escape is easier if you swap to the partner with the cleaner record before the handoff.",
    missable="No — main-story mission.",
    difficulty=1, time="~15 min")

GUIDES[9] = dict(
    guide=("Story mission trophy, unmissable. The Cartel Heist is the game's first full bank job: casing, crew "
           "setup, the vault breach and a hot getaway. Play it straight — hit your marks, keep the crew alive, "
           "and lose the wanted level at the end. It also serves as the tutorial for the free-roam bank vaults "
           "counted by Maximum Withdrawal, so learn the vault routine here."),
    tips="Bring a four-door getaway car with upgraded armor; the escape route is long and the police are aggressive.",
    missable="No — main-story mission.",
    difficulty=2, time="~30 min")

GUIDES[10] = dict(
    guide=("Story mission trophy, unmissable. Child's Play is a character-driven mission that tests stealth and "
           "restraint more than firepower — stay quiet, avoid unnecessary kills, and follow the objective markers "
           "closely. The trophy unlocks when the mission completes. Failing an objective simply restarts the "
           "checkpoint, so there is nothing to lose by taking it slow."),
    tips="Crouch-walk through the guarded sections; being spotted adds a firefight but does not fail the mission.",
    missable="No — main-story mission.",
    difficulty=1, time="~20 min")

GUIDES[11] = dict(
    guide=("Story mission trophy, unmissable. Headliners is a showpiece job built around a public event — expect "
           "crowds, cameras and a very loud exit. Complete each stage as marked: infiltrate, grab the objective, "
           "and get clear of the area. The trophy pops at mission end. Keep an eye on the wanted stars; the "
           "escape is timed around police roadblocks."),
    tips="Use alleyways off the main boulevard during the getaway — the roadblocks only cover the big streets.",
    missable="No — main-story mission.",
    difficulty=2, time="~25 min")

GUIDES[12] = dict(
    guide=("Story mission trophy, unmissable. VCIA Takedown takes you to Vice City International Airport for a "
           "hijack-and-escape set piece. Work through the hangar fight, take control of the target vehicle/aircraft, "
           "and clear the airport perimeter to finish. It doubles as an introduction to VCIA's layout, which you "
           "will revisit for Catch Me If You Can."),
    tips="Learn where the service-road exits are during this mission — they are the fastest way out of VCIA in free roam.",
    missable="No — main-story mission.",
    difficulty=2, time="~25 min")

GUIDES[13] = dict(
    guide=("Story mission trophy, unmissable. Operation Savage Glory is a military-flavored assault mission — "
           "heavy weapons, armored vehicles and a storm-soaked battlefield. Push through the checkpoints, use "
           "cover, and let Combat Focus handle the crowded firefights. The trophy unlocks on completion. "
           "It is one of the best early places to practice the 5-kill Combat Focus streak for Gunslinger."),
    tips="Save Combat Focus for the courtyard fight halfway through — five targets cluster there naturally.",
    missable="No — main-story mission.",
    difficulty=2, time="~30 min")

GUIDES[14] = dict(
    guide=("The big one: reach 100% game completion as shown in the Stats menu. That means the full story, all "
           "Strangers & Freaks strands, every activity type, races, collectibles (cards, WAiNK spots, meditation "
           "spots), stunt jumps and the miscellaneous checklist items. Work category by category and use the "
           "in-game checklist to track what is left — the percentage only moves when a category item is fully done. "
           "This gold trophy is the long pole of the platinum; budget it as its own project after the credits."),
    tips="Leave collectible sweeps for last and do them district by district so you never re-drive the same roads.",
    missable="No — everything required stays available in free roam after the story.",
    difficulty=4, time="30-50 h")

GUIDES[15] = dict(
    guide=("Complete 250 stunts — stunt jumps, wheelies, near-misses and other stunt actions tracked in Stats. "
           "The fastest loop is a sport motorcycle on the coastal highway: hold wheelies between stunt ramps and "
           "chain near-misses in traffic. Stunt jumps over the canals and the airport perimeter ramps are the most "
           "reliable repeatable ones. Check Stats > Stunts to watch the counter climb."),
    tips="A maxed-out sports bike plus a long straight road can bank 30-40 stunts in ten minutes.",
    missable="No — stunts can be farmed any time in free roam.",
    difficulty=2, time="3-5 h")

GUIDES[16] = dict(
    guide=("Try each of the 9 activity types once: racing, fishing, bowling, the shooting range, drone racing, "
           "arcade games, hunting, meditation and the remaining leisure activity marked on the map. "
           "You only need to participate, not win — start each activity and finish a single round. "
           "The trophy pops when the ninth distinct activity is completed. Pair it with a map sweep so you "
           "discover new areas for The Goodtime State at the same time."),
    tips="Track which types you have tried in Stats; the counter lists them individually.",
    missable="No — all activities remain available in free roam.",
    difficulty=1, time="1-2 h")

GUIDES[17] = dict(
    guide=("Earn a gold medal in all 42 Shooting Range challenges (every weapon class at every difficulty tier). "
           "Gold is score-based: accuracy and speed both count, so aim for headshots and never let the timer idle. "
           "Work one weapon class at a time and replay immediately while the target patterns are fresh. "
           "The later tiers are the real test — budget several sessions rather than one marathon."),
    tips="Turn off aim assist for the precision tiers if it keeps snapping to body shots; headshots are worth double.",
    missable="No — the range stays open after the story.",
    difficulty=4, time="4-8 h")

GUIDES[18] = dict(
    guide=("Win a Top Fun drone race at each of the 14 Top Fun locations across Leonida. Each course is a timed "
           "checkpoint run; winning means beating the target time, not just finishing. Learn a course with one "
           "slow lap, then attack it — most target times have a few seconds of slack once you know the line. "
           "The trophy unlocks on the 14th location's win."),
    tips="Cut corners over rooftops instead of following the street line; the checkpoints forgive a lot of altitude.",
    missable="No — Top Fun stands stay open in free roam.",
    difficulty=3, time="2-4 h")

GUIDES[19] = dict(
    guide=("Win 20 different races — each race location counts once, so you need 20 distinct wins, not 20 wins on "
           "the same track. Street races unlock around the map as you progress; pick short city circuits first, "
           "where a tuned sports car wins easily. Rubber-banding is mild on lower difficulties, so a clean first "
           "lap usually decides it. The trophy pops on the 20th unique victory."),
    tips="Use the same maxed-out car for every race to learn its handling; variety of cars only slows you down.",
    missable="No — races can be replayed any time.",
    difficulty=2, time="2-3 h")

GUIDES[20] = dict(
    guide=("Beat Cal in a fishing challenge. Cal hangs around the docks and bait shops — talk to him to start a "
           "head-to-head fishing contest where the bigger total catch wins. Cast near structure (piers, rocks, "
           "weed beds) where fish bite faster, and reel in steadily rather than yanking. "
           "If Cal gets lucky with a big catch, simply challenge him again; there is no penalty for rematches."),
    tips="Fish at dawn or dusk in-game — bite rates are noticeably higher and Cal's luck matters less.",
    missable="No — Cal accepts rematches indefinitely.",
    difficulty=1, time="~20 min")

GUIDES[21] = dict(
    guide=("Complete any one arcade game — reach its ending or final stage, not just play a credit. Arcade cabinets "
           "sit in bars, arcades and a few safehouses; pick the shortest game (the side-scrolling shooter is the "
           "quickest clear) and play through to the end screen. Continues are allowed, so feed credits freely. "
           "The trophy unlocks when the game's completion screen appears."),
    tips="The twin-stick cabinet is the fastest to finish — about five minutes with continues.",
    missable="No — cabinets stay available in free roam.",
    difficulty=1, time="~10 min")

GUIDES[22] = dict(
    guide=("Complete the final mission in Andy's strand. Andy is one of the Strangers & Freaks contacts — his "
           "missions appear as a question-mark icon after you first meet him, and each completed job unlocks the "
           "next after some in-game time passes. Play the strand to its end; the trophy pops when his last mission "
           "completes. Andy's strand also counts toward the 8 strands needed for Strangers & Freaks."),
    tips="If the next Andy marker does not appear, sleep or do another activity — strands advance on a timer.",
    missable="No — stranger strands wait for you in free roam.",
    difficulty=1, time="1-2 h (strand)")

GUIDES[23] = dict(
    guide=("Complete the final mission in Kenton's strand. Kenton's jobs lean nautical — expect boats, docks and "
           "at least one story that ends with something sinking. Follow his question-mark markers in order until "
           "the strand concludes; the trophy unlocks on the final mission's completion screen. "
           "Counts toward Strangers & Freaks like every other completed strand."),
    tips="Kenton's later missions are easier with a fast boat of your own — buy one before the finale if you can.",
    missable="No — stranger strands wait for you in free roam.",
    difficulty=1, time="1-2 h (strand)")

GUIDES[24] = dict(
    guide=("Complete the final mission in Billy's strand. Billy is the biker of the stranger cast — his missions "
           "are road-focused, with long rides and at least one chase that punishes slow vehicles. "
           "Bring a fast motorcycle to his later jobs. The trophy pops when his final mission completes, "
           "and the strand counts toward Strangers & Freaks."),
    tips="Billy's chase missions are far easier on a maxed sports bike than in a car — the routes use narrow gaps.",
    missable="No — stranger strands wait for you in free roam.",
    difficulty=2, time="1-2 h (strand)")

GUIDES[25] = dict(
    guide=("Complete 8 full Strangers & Freaks mission strands anywhere in Leonida. A strand counts only when its "
           "final mission is done, so finish whole storylines rather than sampling first missions. "
           "Andy, Kenton, Billy, Randy and Tyrone each give a strand (and their own trophies), so three more "
           "strangers from the question-mark icons around the map complete the set. "
           "The silver trophy unlocks the moment the eighth strand's finale ends."),
    tips="Do the five named strands first — they pay well and their trophies stack with this one.",
    missable="No — all strands remain available after the story.",
    difficulty=2, time="6-10 h")

GUIDES[26] = dict(
    guide=("Complete the final mission in Randy's strand. Randy's jobs revolve around deliveries and small-time "
           "hustles that escalate — keep a reliable vehicle handy and expect the last mission to involve a timed "
           "run. The trophy unlocks when his final mission completes. Counts toward Strangers & Freaks."),
    tips="Randy's timed deliveries are generous if you use the highway instead of cutting through neighborhoods.",
    missable="No — stranger strands wait for you in free roam.",
    difficulty=1, time="1-2 h (strand)")

GUIDES[27] = dict(
    guide=("Complete the final mission in Tyrone's strand. Tyrone's missions mix street races with errands — "
           "win or survive each stage to advance the strand. His finale is the longest of the five named strands, "
           "so bring your best car. The trophy pops on completion, and the strand counts toward Strangers & Freaks."),
    tips="Tyrone's race stages allow any vehicle — your tuned race car from Earn Cash, Not Kudos trivializes them.",
    missable="No — stranger strands wait for you in free roam.",
    difficulty=2, time="1-2 h (strand)")

GUIDES[28] = dict(
    guide=("Meditate at all 18 meditation spots scattered across Leonida — beaches, overlooks, gardens and a few "
           "rooftops. Each spot is a small marked circle; stand in it and use the meditate prompt for a few seconds. "
           "There is no fail state, just travel time. Sweep them region by region alongside collectible runs so "
           "the driving doubles up with The Goodtime State exploration."),
    tips="Meditation spots glow faintly at night, which makes the rooftop and garden ones easier to spot.",
    missable="No — spots stay available in free roam.",
    difficulty=1, time="1-2 h")

GUIDES[29] = dict(
    guide=("Hunt the unique animal Bret asks for. Bret is a hunting contact — after you meet him, he marks a "
           "specific rare animal (a distinctive coat/pattern variant) somewhere in the Leonida wilds. "
           "Track it with the hunting scope, approach downwind and crouched, and take it down cleanly; "
           "a spooked animal flees and must be re-tracked. Deliver the result to Bret to finish and pop the trophy."),
    tips="Go at dawn when animals are active and the light makes the unique coat easy to pick out.",
    missable="No — Bret's request stays open until completed.",
    difficulty=2, time="~30 min")

GUIDES[30] = dict(
    guide=("Complete 3 full Collectible Card sets. Cards are hidden around Leonida — in shops, landmarks, "
           "safehouses and a few mission interiors — and each set has a theme (vehicles, landmarks, characters). "
           "A set completes when every card in it is collected; check the Collectibles menu to see which cards "
           "you still miss and their hint regions. Three completed sets unlock the silver trophy. "
           "This is a pure sweep: work district by district with the in-game hints."),
    tips="Cards inside shops can be grabbed while robbing them — combine the sweep with Retail Therapy runs.",
    missable="No — cards persist in free roam; none are locked behind story choices.",
    difficulty=3, time="4-6 h")

GUIDES[31] = dict(
    guide=("WAiNK It at 100 different locations. WAiNK is the in-game social app — at marked photo spots around "
           "Leonida, open the phone camera, frame the landmark and post. Each unique location counts once; "
           "repeats at the same spot do not advance the counter. There are well over 100 spots, so sweep the "
           "tourist areas first (Ocean Beach, downtown, the pier) where they cluster densely."),
    tips="Photo spots appear as small camera icons when you are close — drive slowly through landmark districts to reveal them.",
    missable="No — spots remain available in free roam.",
    difficulty=2, time="3-5 h")

GUIDES[32] = dict(
    guide=("Complete 50 Challenges from the Challenges menu — the rotating list of driving, combat, exploration "
           "and miscellaneous feats (near-misses, wheelies, headshots, distances and so on). "
           "Many complete passively while you play, so check the menu and deliberately finish the quick ones: "
           "most driving challenges can be farmed on the coastal highway in minutes. "
           "The trophy pops on the 50th completion; the counter is cumulative across both protagonists."),
    tips="Sort the challenge list by progress — half-finished challenges are the cheapest completions.",
    missable="No — challenges never expire.",
    difficulty=2, time="3-6 h")

GUIDES[33] = dict(
    guide=("Lose a 4-star Wanted Level while your partner is with you, and escape the heat. Easiest method: with "
           "both protagonists together, cause chaos in a quiet area until you hit 4 stars (destroying police cars "
           "works fast), then break line of sight — dive into a parking garage, tunnel or under a bridge and stay "
           "hidden until the stars flash and fade. Your partner must be present and alive when the wanted level "
           "fully clears. A respray shop also works if you can reach one unseen."),
    tips="Start near a multi-level parking garage: earn the stars outside, then hide on the top floor away from ramps.",
    missable="No — repeatable any time in free roam.",
    difficulty=2, time="~15 min")

GUIDES[34] = dict(
    guide=("Rob 3 shops back-to-back with your partner without losing your Wanted Level. Bring your partner, pick "
           "three shops close together (a strip mall or downtown block), and rob them in sequence: threaten the "
           "clerk, take the till, move straight to the next shop. The wanted level must stay active the whole "
           "time — if the stars fade between shops, the chain breaks. Keep a car running outside and do not "
           "stop to fight police between robberies."),
    tips="Ocean Beach's retail strip has three shops within one block — the whole run takes under two minutes.",
    missable="No — shops restock and can be robbed again after a cooldown.",
    difficulty=2, time="~15 min")

GUIDES[35] = dict(
    guide=("Discover 100 different vehicles — sit in or drive 100 unique models and they register in your vehicle "
           "index. Traffic variety does most of the work: drive through different districts (beach, downtown, "
           "industrial, countryside) and swap into anything you have not driven. Dealerships and parking lots are "
           "dense with models. The counter is in Stats; the trophy pops on the 100th unique vehicle."),
    tips="Vehicle showrooms and the airport rental lots together hold 20+ models in one stop.",
    missable="No — vehicles keep spawning in free roam.",
    difficulty=1, time="2-3 h")

GUIDES[36] = dict(
    guide=("Take down 5 enemies during a single use of Combat Focus (Lucia's slow-motion ability). "
           "You need five targets in one activation: story firefights with clustered enemies are ideal — "
           "the courtyard fight in Operation Savage Glory or any gang hideout assault. "
           "Activate Focus with a full meter, use a fast-firing weapon, and sweep headshots before the meter drains. "
           "Upgrading Combat Focus duration makes this dramatically easier."),
    tips="A fully upgraded Focus meter plus an SMG can clear 6-7 targets — do this after the upgrade, not before.",
    missable="No — repeatable in any large firefight or gang hideout.",
    difficulty=3, time="~20 min")

GUIDES[37] = dict(
    guide=("Make an unscheduled departure at VCIA (Vice City International Airport) — leave the airport in a way "
           "the timetable never intended: steal a plane or helicopter and take off without clearance, or blast "
           "through a service gate with a wanted level. The simplest route is to sneak to a parked aircraft on "
           "the apron, take off, and clear the airport airspace; the trophy pops as you leave the restricted zone. "
           "Expect police attention, so fly straight out to sea afterwards."),
    tips="Use the service-road gaps you scouted in VCIA Takedown to reach the apron without an early wanted level.",
    missable="No — VCIA is accessible in free roam.",
    difficulty=2, time="~15 min")

GUIDES[38] = dict(
    guide=("Deal with the Rhinos — the army tanks that roll out at high wanted levels and guard the military "
           "installations. The trophy is tied to surviving and destroying Rhino tanks: push your wanted level "
           "to the maximum near a military base or during the Chapter 4 set pieces, then destroy a Rhino with "
           "heavy weapons (RPGs, sticky bombs or an armed vehicle) and get clear. "
           "It is hot in there — bring armor, explosives and an escape route that is not a straight road."),
    tips="A Rhino is slow to turn: circle it at close range and plant sticky bombs on its rear armor.",
    missable="No — Rhinos respond to max wanted levels in free roam.",
    difficulty=3, time="~20 min")

GUIDES[39] = dict(
    guide=("Rob a jewelry store without being detected. Case the store first: note the cameras, the guard's patrol "
           "and the alarm panel. Enter masked at a quiet hour, disable the cameras (shoot or hack them from "
           "outside their view), take out the guard silently, then empty the cases and leave through the back "
           "before anyone raises the alarm. If you are seen or a wanted level triggers, the attempt fails — "
           "leave, let the heat die, and try again."),
    tips="The Ocean Beach jewelry store has a rear alley exit — park your getaway car there before you go in.",
    missable="No — jewelry stores can be re-robbed after a cooldown.",
    difficulty=3, time="~20 min")

GUIDES[40] = dict(
    guide=("Rob 5 bank vaults in free roam and escape each time. Banks with vaults are marked around Leonida; "
           "the routine mirrors The Cartel Heist — control the lobby, breach the vault (drill or thermite), "
           "grab the take and lose the wanted level. Each bank needs its own escape; getting caught or dying "
           "voids that attempt. Five successful vault jobs unlock the silver trophy. "
           "Banks cool down between hits, so rotate across the map."),
    tips="Smaller regional banks have thinner security than the downtown flagship — start there while you learn the routine.",
    missable="No — vaults restock after a cooldown.",
    difficulty=3, time="2-3 h")

GUIDES[41] = dict(
    guide=("Rob an armored truck and escape. Armored trucks drive set routes between banks — find one on the "
           "highway or near a bank, block it in, and force the crew out (shoot the tires or ram it to a stop; "
           "blowing the rear doors with a sticky bomb also works). Grab the cash cases, then lose the wanted "
           "level. The trophy pops once you are clear with the money. "
           "Trucks are tougher than they look — bring a heavy vehicle for the stop."),
    tips="Trucks spawn most reliably on weekday mornings near downtown banks; cruise the financial district to find one.",
    missable="No — trucks keep running their routes in free roam.",
    difficulty=2, time="~15 min")

GUIDES[42] = dict(
    guide=("Explore all 52 named areas of Leonida — every district, town, beach and landmark zone must be "
           "discovered (the area name flashes on screen the first time you enter). Driving the full highway "
           "loop plus the coastal roads covers most of them; the remainder are small towns and islands off the "
           "main routes. Check Stats > Areas to see the count. Pair this with collectible and WAiNK sweeps "
           "so one road trip ticks several trophies at once."),
    tips="A helicopter tour of the coastline reveals island areas that roads never touch.",
    missable="No — areas stay discovered once visited.",
    difficulty=1, time="3-5 h")

GUIDES[43] = dict(
    guide=("Rob an illegal operation belonging to each of Leonida's 9 gangs. Illegal operations — stash houses, "
           "chop shops, drug labs — are marked once you scout a gang's turf; each belongs to a specific gang, "
           "shown in the operation's info. Hit one per gang: clear the defenders, grab the take, and escape. "
           "The trophy pops on the ninth gang's operation. The gangs' territories are spread across the state, "
           "so this doubles as an exploration tour."),
    tips="Scout operations with a drone or from a rooftop first — the gang tag shows before you commit to the assault.",
    missable="No — operations restock after a cooldown.",
    difficulty=3, time="2-4 h")

GUIDES[44] = dict(
    guide=("Enjoy a cocktail with a view on Ocean Beach. Head to one of the beachfront bars on Ocean Beach, "
           "order a cocktail at the bar, and take it to a spot overlooking the water — the terrace or the "
           "boardwalk railing both work. Simply drink it while facing the ocean view. "
           "It is a thirty-second trophy and a good excuse to watch the sunset over the water."),
    tips="Sunset hour makes the view — and the screenshot — but any time of day counts.",
    missable="No — beach bars stay open in free roam.",
    difficulty=1, time="~5 min")

GUIDES[45] = dict(
    guide=("Smash your way out of a vehicle showroom in classic style: get inside a car dealership, take a "
           "display car, and drive it straight through the showroom's glass frontage onto the street. "
           "The trophy pops as you burst through the glass in the stolen display model. "
           "Expect an instant wanted level — have your escape route planned, or just enjoy the chaos and lose "
           "the police afterwards."),
    tips="The downtown luxury showroom has the biggest glass front — maximum style points, same trophy.",
    missable="No — showrooms restock their display cars.",
    difficulty=1, time="~10 min")

GUIDES[46] = dict(
    guide=("Play bowling at the Kolt & Associates bowling alley — and follow through: finish a full game, "
           "all frames, rather than quitting early. Bowling is a timing minigame: set your stance, aim with "
           "the curve, and release on the power sweet spot. Winning is not required, just completing the game. "
           "The trophy unlocks at the final score screen."),
    tips="A gentle curve from the right gutter into the pocket beats raw power for consistent strikes.",
    missable="No — the alley stays open in free roam.",
    difficulty=1, time="~15 min")

GUIDES[47] = dict(
    guide=("A partnership moment with mass appeal: perform a signature partner action in front of a crowd. "
           "With your partner alongside, pull off a showy duo move where people are watching — the crowded "
           "boardwalk, a beach party or a busy plaza all count. Partner interactions unlock as the story "
           "progresses; use one in a packed public place and the trophy pops when the crowd reacts. "
           "If it does not trigger, move to a denser crowd and try a different partner action."),
    tips="Weekend afternoons on Ocean Beach give the densest crowds in the game.",
    missable="No — partner actions stay available in free roam.",
    difficulty=1, time="~10 min")

GUIDES[48] = dict(
    guide=("Make choices — the game tracks your decisions (dialogue picks, mission approaches, sparing or "
           "finishing people, business calls) toward a running count of 500. Almost everything you decide "
           "counts, so this unlocks naturally over a full playthrough plus free-roam cleanup. "
           "If you finish the story short of the mark, run stranger missions and business decisions — they are "
           "dense with tracked choices. Progress shows in Stats."),
    tips="Business management decisions after the story are the fastest filler if you are a few dozen short.",
    missable="No — choices keep accumulating in free roam.",
    difficulty=1, time="Passive (full playthrough)")

GUIDES[49] = dict(
    guide=("Second time's the charm: fail something, then succeed at it on the retry. The cleanest route is a "
           "race — deliberately lose or quit a race, then immediately re-enter and win it. The trophy pops on "
           "the successful second attempt. Activity challenges and mission checkpoints work too, "
           "but the race method takes five minutes and cannot be messed up."),
    tips="Pick the shortest street race, idle at the start to fail it, then win the rematch properly.",
    missable="No — any failed-then-won activity counts.",
    difficulty=1, time="~10 min")

GUIDES[50] = dict(
    guide=("Witness something strange — Leonida has a few unexplained events that only appear under specific "
           "conditions (odd lights over the swamps at night, a figure that should not be there, sounds with no "
           "source). Explore the rural north and the swamp edges after midnight and watch for anything that "
           "does not belong; when the event plays out, the trophy pops. "
           "It is a pure discovery trophy — keep your eyes open during night-time collectible runs."),
    tips="The swamp boardwalks at night are the most reliable place to trigger something weird.",
    missable="No — the strange events recur in free roam.",
    difficulty=1, time="~30 min")

GUIDES[51] = dict(
    guide=("Bowl 'em over with a melee drive-by: from a moving vehicle, lean out and strike a pedestrian with a "
           "melee weapon so they are knocked down. Drive slowly past a target on a sidewalk, swing as you pass, "
           "and connect. A motorcycle makes the angle easiest, but any vehicle works. "
           "The trophy pops on the knockdown — no need to stop and check on them."),
    tips="Slow traffic on Ocean Beach gives you plenty of targets and room to line up the swing.",
    missable="No — repeatable anywhere with pedestrians.",
    difficulty=1, time="~10 min")

GUIDES[52] = dict(
    guide=("Earn $250,000 laundering Marked Bills through your contacts. Marked Bills come from heists and "
           "illegal operations; contacts (unlocked from Chapter 2 onward) convert them to clean money at a "
           "cut. The $250,000 is cumulative clean cash received, not a single delivery. "
           "Launder whenever a contact is available and keep Marked Bills flowing by robbing operations and "
           "vaults — this is a slow background grind, so start it early and let it accumulate."),
    tips="Different contacts take different cuts — always use the contact offering the best rate that day.",
    missable="No — laundering stays available after the story.",
    difficulty=2, time="Passive (10-20 h of play)")

GUIDES[53] = dict(
    guide=("Spend $100,000 across all shops — clothing, weapons, vehicle mods, food, everything counts toward "
           "one cumulative total. The fast route is vehicle customization and high-end clothing late in the "
           "game when money is plentiful; a couple of maxed-out cars plus a wardrobe refresh gets you most of "
           "the way. Track the total in Stats > Money. The trophy pops the moment cumulative spending crosses "
           "$100,000."),
    tips="Weapon upgrades for both protagonists are the most useful spending — do those first, then cosmetics.",
    missable="No — shops never close for good.",
    difficulty=1, time="Passive (late game)")

GUIDES[54] = dict(
    guide=("Purchase all 8 garage properties across Leonida. Garages appear on the property listings as you "
           "progress; prices climb from modest to eye-watering, so this is a late-game purchase spree. "
           "Buy each one from its property marker or the real-estate app — owning all 8 pops the trophy. "
           "Garages also store your vehicles safely, so buy the cheap ones early and the flagship last."),
    tips="The downtown multi-car garage is the priciest — save it for after the final heist payout.",
    missable="No — properties stay purchasable after the story.",
    difficulty=1, time="Passive (late game)")

GUIDES[55] = dict(
    guide=("Register 10 vehicles to the Scooter Bros app. Open the Scooter Bros app on your phone, and register "
           "vehicles you own — each registration needs the vehicle parked and in your possession. "
           "Ten different vehicles are required; cheap scooters and bikes count the same as supercars, so "
           "register whatever is already in your garages. The trophy pops on the tenth registration."),
    tips="Vehicles stored across all your garages can be registered from the app without driving to them.",
    missable="No — the app stays available in free roam.",
    difficulty=1, time="~15 min")

if __name__ == "__main__":
    data = json.loads(SRC.read_text(encoding="utf-8"))
    for t in data["trophies"]:
        g = GUIDES.get(t["id"])
        if g:
            t["guide"] = g["guide"]
            t["tips"] = g["tips"]
            t["missable"] = g["missable"]
            t["difficulty"] = g["difficulty"]
            t["time"] = g["time"]
    DST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    words = sum(len(t["guide"].split()) for t in data["trophies"])
    print(f"wrote {DST} — guides enriched: {len(GUIDES)}/55, guide words: {words}")
