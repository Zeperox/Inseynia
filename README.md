# Inseynia

### Welcome to Inseynia!

This is an action open-world bullethell top-down story rpg game (wow that's a mouthful)

Anyway, this is where you can look at the code and help find issues that you probably found while testing. We appreciate your help 🙂

---

# Change Logs

## Pre-Alpha 0.2.1

### Additions/Removals
- Added `Primary Special Attack` and `Secondary Special Attack` control buttons

### Changes/Improvements
- Changed how menus are handled
- Changed the save data shown when selecting a save from HP, Stamina, and class stats to showing the player level and classes
- The game's name will no longer change languages

### Bug Fixes
- Fixed a couple of bugs relating to navigating through the controls menu in the settings
- Fixed a couple of button highlighting issues in the controls menu in the settings
- Fixed a bug where if you opened your inventory after your backpack breaks the game might crash
- Fixed a bug where using keyboard navigation in the music room to change the music would crash the game
- (POTENTIALLY) Fixed a bug where the game would weirdly auto-save (there is literally no line that tells it to auto-save) and restart itself, causing the map to reset but the player data stay the same

## Pre-Alpha 0.2

### Additions/Removals

- Added a hearing radius around enemies, in which if you enter the radius they become suspicious
- Added sneaking which makes you slower but makes your hitbox smaller and makes it harder for enemies to detect you
- Added 2 new classes, Swordsman and Thief
- Added chestplates and leggings
- Added a dagger with a stab attack and the ability to deal 3x the base damage when stealth killing
- Added a sword with a swing attack
- Added buttons to dialogues
- Added the ability to still be able to use weapons after your class stats deplete but with compromises
    - Archer: once you run out of ammo, your weapon can be used as a melee attack
    - Mage: once you run out of mana, you'll consume your stamina, once that runs out you'll start consuming your HP
    - Swordsman: once you run out of vigor, your attacks are slower, weaker, and deal less knockback
    - Thief: there are none because your attacks are unlimited
    - FOR ALL: cannot use specials (later in the changelog)
- Added the ability to equip weapons (only as your secondry) that don't correspond with your secondry class but with compromises (similar to those written up)
- Added "Mods" button
- Added the ability to quickly go back to the previous page in the menu by pressing right-click, shift, escape, or backspace
- Added vsync option
- Removed the apply button in settings
- Added a way to reset the settings back to default by pressing the middle mouse button
- Removed the brightness code file, replacing it with a more linear approach (doesn't affect anything in-game)
- The save menu now shows your stats (health, stamina, and class stats) for every save file
- Added functional difficulty
- Added enemy drops
- Added an icon to the error popup
- Added inventory controls that show whenever you open the inventory
- Added quests
- Added .gif support
- Added the ability to rebind controls to the mouse
- Added controller rebinding
- Added the ability to invert the controller sticks
- Added asset pack functionality, which replaces the default assets
- Added behavior pack functionality, which replaces the default code
- Added special attacks (Q/RB for primary, E/LB for secondary)
- Added power gauge which requires 50 hits to activate a special attack
- Added an attack cooldown indicator
- Added special tiles with unique functionalities
- Added a max width to tooltips to make it impossible for the tooltip to go off screen 
- Added image support to text by using `<sp:sprite_name>`
- Added tiles that don't stop bullets
- Added health increase number popup
- Added status effects
- Added projectiles that can deal status effects

### Changes/Improvements

- Made the "Interact" popup change depending on whether you're using a controller or a keyboard
- Changed how sleeping works
- Changed inventory layout
- Changed how armor works
- Changed how inventory slot selecting works
- Slightly changed how projectiles stop
- Slightly improved the assets folder layout
- Made dialogue text appear faster
- Completely rewrote the dialogue system
- Removed the gradient from inventory slots
- Made the inventory and pause menus' backgrounds more transparent
- Completely rewrote how texts work
- Replaced font pngs with font ttfs
- Changed the font from a custom-made font to UniFont
- Completely rewrote menus
- Made the settings take effect the moment you change something
- Made it possible to have duplicate controls, but the game warns you
- Made it possible to align the text inside the button (in code)
- Changed how UI is rendered
- Changed how music is loaded
- Updated some of Jlokshi's attacks
- Improved dialogues
- Made boss healthbars transparent
- Improved boss health bar when there are more than 2 bosses (not tested)
- Changed how animations are loaded 
- Made the game fully pause during dialogues or cutscenes
- Attempting to render something on screen without it actually existing will no longer crash the game but rather will render an image with black and purple squares
- Made the in-game player stats UI longer
- Slightly changed the inventory menu to instead be a collection of sub-menus
- Changed how item tooltips are rendered
- Changed how item tooltips are loaded
- Changed how the level up system works
- Improved how the attack stats are handled
- Made loading the game faster
- Improved the input system
- Made it possible to rebind the attack controls
- Improved menu navigation via keyboard or controller
- Completely rewrote map loading
- Changed how the scripts folder is loaded
- Made it possible to collect dropped projectiles from enemies again, but you can only pick up the ones that you also shoot
- Changed the default interact button in keyboard to r
- Changed the sleep & interact buttons in controller to Y & X respectively
- Improved sprite data
- Improved UI rendering speeds
- Upgraded to py 3.11.3
- Changed the map files from multiple .csv files to a single .json file
- Improved tile collision
- Improved entity rendering
- Improved the checking code for the sleep requirements
- Heavily improved saving and loading saves
- Made the FPS update every half a second rather than every second
- Changed the damage number popup animation
- Items fall in random places rather than all in the same place when your backpack breaks
- Changed the inventory slot selection rectangle color to fit with the rest of the game
- Temporarily disabled health, stamina, and magic regen (not sure if I'll bring it back)

### Bug Fixes

- Fixed a bug where hitting a sign would cause the game to crash
- Fixed a bug where the brightness slider's brightness would somewhat break
- Fixed a bug where some UI render above the debug menu
- Fixed a bug where items with no tooltips would have a tall tooltip box
- Fixed a bug where the numbers would be flipped if you change the language from arabic to a different language
- Fixed a bug where the sticks wouldn't work when you first open the game forcing you to reconnect the controller, which then broke the back button
- Fixed a bug where when you try to continue through the dialogue with a controller the dialogue ends instead
- Fixed a bug where sometimes the game crashes for failing to detect collidable tiles adjacent to an entity
- Fixed a bug where the dialogue's rendered text wouldn't reset if you enter the dialogue again
- Fixed a bug where some UI elements would appear above the inventory
- Fixed a bug where the item tooltip wouldn't be rendered if you are navigating the inventory using a keyboard or a controller
- Fixed a bug where if the save name is too long it can appear outside its box in the save selection screen
- Fixed a bug where attacking some NPCs would cause the game to crash
- Fixed a bug where some timings would be off when you unpause the game
- Fixed a bug where the game could crash when you unpause the game
- Fixed a bug where having a full inventory would stop you from grabbing dropped projectiles and spirits
- Fixed a bug where weapons with extended cooldowns would cause your stats to deplete every frame
- Fixed a FPS issue where json was doing a lot of redundant loads that kinda slowed down performance
- Fixed a multitude of issues with tile loading
- Fixed a bug where the player was able to move while sleeping
- Fixed a bug where a portion of the Arabic tooltip wouldn't render
- Fixed all bugs relating to diagonal tiles
- Fixed a bug where the damage number popup animation would break in higher fps 
- Fixed a bug where the damage number popup in NPCs didn't have an animation

## Pre-Alpha 0.1

### Additions/Removals

- Added a low HP effect at the screen edge
- Added language support
    - English
    - Arabic
    - Japanese
    - Russian
    - Spanish
    - French
- Added the ability to mod your own custom main loops (cannot overwrite the main loop of the main game)
- Added dialogues
- Added NPCs
- Added cutscenes
- Added signs
- Added friction to all enemies
- Added acceleration to enemies
- Added enemy sub-AI (basically a file with a modified version of a certain AI)
- Stopped the functions entities and tiles outside of the screen
- Added the ability for stuck arrows to dissappear if there are too much of them, lowering the lag
- Removed projectile types
- Added the ability for enemies and weapons to have their own unique projectile movement
- Added backpacks
    - Added item weight (won't affect movement like armor weight)
    - Backpacks would break if the items exceed the backpack's max weight
- Added player levels, which increases the player's health, stamina, and mana
- (IN CODE) Removed unnecessary data stored in projectiles
- Added a way to manually save the game
- Removed auto-save
- Added sleeping which increases your stamina, health, and mana
- Removed spawn map
- Added connectors to maps, or areas that get you to a new map
- Added the ability to spawn pre-damaged enemies
- Added VFX for spirits being sucked out of their mana
- Spirits no longer stay in place when your mana is full but rather disappear
- Removed the "Map coming soon :)" text
- Added critical hits
- Added a damage multiplyer range, between *0.75 to *1.25
- Added a visual indicator for damage output
- Added the ability to pause the game by simply moving your mouse outside the game, this is to help accidentally minimizing of the game
- Added a new map with some new tiles
- Removed a bunch of random captions
- Added the ability to have invisible collideable tiles
- Added a boss named "Jlokshi"
- Added controller support
- Added the ability to use your keyboard for the menus and for the inventory
- Added room and boss music
- Added health, stamina, and mana potions (well more precisely fish)
- Added an icon for the game
- Added enchanted arrows (a drop) which when used would refill your quiver
- Added text that shows the version
- Added "projnum" in the debug menu
- Added player health, stamina, and mana regen
- Added pixel-perfect collisions (only used for colliding with entities/projectiles)
- Added diagonal tiles
- Added camera zoom (cannot be previewed in the pre-alpha)
- Added game over screen
- Added a popup for when you can interact with an object
- Removed the main menu background (will be readded in the next update hopefully)

### Changes/Improvements

- Slightly changed menus
- Improved rendering speed
- Changed FPS limiter
- Heavily boosted FPS
- Slightly improved RAM usage when loading maps
- Completely rewrote the text rendering system
- Slightly improved player movement
- Completely changed how animations are handled
- Slightly changed how knockback works
- Changed the screen resolution from 1280x720 to 640x360 with 2x scale, also scales up with monitor size
- Updated credits
- Increased image loading speed
- Changed how projectile movement is handled
- Improved error popup's text
- Changed the inventory size to 5 slots
- Fixed a misalignment bug with items in the inventory
- Improved new save creation
- Improved save file
    - Enemies now save their data
    - Drops now save their locations
    - NPCs and cutscenes now save their locations
- Changed inventory stats UI
- Seperated the background tiles from the normal tiles, making a seperate map for background tiles
- Changed the dev room's tiles
- Slightly improved inventory FPS
- Improved fullscreen options code
- Changed dashes from dashing to the mouse location to the direction you are facing
- Improved UI rendering speed
- Slightly changed the English font
- Improved item tooltip loading speed
- Changed doors from immediately going through them to having the requirement to press "E" in order to enter them
- Slightly changed dev room map layout to show some sort of a "doorway" into another room
- Imporoved entity functions speed
- Made the camera to lock to the midpoint coordinates between you and the boss(es) if there is any boss
- Made bosses display their HP
- EkretaTree is no longer considered as a boss
- Changed the stats of EkretaTree
- Changed the i-frames from 0.5 seconds to 0.1 seconds
- Made it possible to change the i-frames for specific entities
- Slightly improved inventory slot collision (used for detecting where the mouse is)
- Separated between spirits, projectile drops, and normal drops (backend)
- Made projectiles only pickable if you (the player) threw them
- Changed how projectile drops are registered (backend
- Changed the collisions of entities, now it's smaller than the sprite
- Changed how tile collisions work
- Slightly improved the math with inventory rendering
- Made music pause when you're in the pause menu rather than play the main menu theme
- Changed how enemy AI is loaded
- Changed the starting ammo count for archers to 200

### Bug Fixes

- Fixed a bug where the game's rendering would break if you die
- Fixed a bug where invalid text characters would crash the game
- Fixed a bug where trying to load custom enemies/weapons from mods would crash the game
- Fixed a bug where the player would shake instead of dash in lower FPS
- Fixed a bug where the dash distance is much higher in lower FPS
- Fixed a bug where the entities would shake instead of getting knockbacked in lower FPS
- Fixed a bug where the knockback distance is much higher in lower FPS
- Fixed a bug where holding a shield while being knockbacked would just pause the knockback, leaving the shield would cause you to continue
- Fixed a bug where the error popup wouldn't work when the game is in fullscreen
- Fixed a bug where projectiles can sometimes be jittery
- Fixed a misalignment bug with items in the inventory
- Fixed a bug where you can skip the wait time of picking up items by opening the inventory
- Fixed a bug where projectiles' shot time (the time the projectile was shot) would break once you open the inventory
- Fixed a bug where everything gets teleported/skipped once you pause
- Fixed a bug where spirits would no longer render after 1 has already been spawned
- Fixed a bug where touching a projectile as it disappears could cause a crash
- Fixed a backend bug where text alpha would return "None" rather than a number
- Fixed a bug where if the map has an opening at the end of it you would be able to leave
- Fixed a bug where holes in a map would cause visual bugs
- Fixed a bug where setting the FPS to any value other than "unlimited" would cause the "unlimited" option to break
- Fixed a bug where entering a new room wouldn't reset the camera position, causing the camera to move through the room to reach your location
- Fixed a bug where if you die while there is a lot of bullets on the screen to the point that they despawn, then reload you save file, the game would crash
- Fixed a bug where if you have more than 1 of the same item, the inventory would always use the first item in the inventory rather than the selected item
- Fixed a bug where you could open the pause menu in the inventory menu
- Fixed a bug where camera movement based on coordinates rather than an entity would always ignore the map borders
- Fixed a bug where if you dash into a wall you would freeze
- Fixed a bug where if you press "apply" while there is a control waiting for a new key the game would crash
- Fixed a bug where entering the music room plays the main menu theme at first instead of the first song in the list
- Fixed a bug where if you died and restarted the game without quitting the game, enemies will still have their lost health from when you fought them before you died
- Fixed a bug where the text would break if there are more than 2 lines

### Known Bugs

- Dashing towards the end of the map that isn't enclosed by a tile would cause you to get stuck outside the map
- Starting a dialogue using a controller would bug out the dialogue
- Triggering the cutscene in certain areas would cause the cutscene's test enemy to get stuck behind some walls making it unable to continue

<br>

## Dev 1.6.1

### Bug Fixes

- Fixed a bug where the game would crash because the cache file would be missing (thanks github)
- Fixed a bug where the game would fail to generate a map folder in the cache causing it to crash

## Dev 1.6 (Overwrite)

### Additions/Removals

- Added tile, drop, and enemy IDs
- Added drop map and loading drops from the map
- Added enemy map and loading enemies from the map
- Added animation support to entities
- Added a special menu of save selection
- Added the ability to have up to 3 standalone saves
- Added a functional SFX slider (there aren't any sound effects yet though)
- Removed standalone enemy classes
- Added AI classes to group enemies
- Removed inventory hotbar
- Added inventory menu, which contains your inventory, your equipment, your stats, and a map (map isn't done yet)
- Removed stackable items
- Removed resolution setting, now it is hard-set to 1280x720 (programming the game was harder and tons of sprites broke when using different resolutions)
- Added item tooltip
- Added music room
- Added a song that I... totally didn't steal from cthethan
- Removed melee combat
- Removed rolling, leaving only dashes to use to avoid
- Added the ability for an enemy's projectile to hit other enemies
- Added the ability for certain projectiles to stick to the wall or "fall" to the ground
- Added a new dedicated slot for armor equipment
- Removed the second weapon slot
- Added secondry slot, which could either hold a shield or, if you have 2 classes, a second weapon (basically if you wanna be offensive then you gotta sacrifice using the shield)
- Shields no longer account for you defense and your weight
- Added the ability to stop projectiles when holding your shield
- Added the ability to cause projectiles to ricochet if you hold your shield at the correct timing (each shield has a different ricochet speed and distance)
- Added a small miniboss, called Ekreta Tree
- Removed Big Eye boss
- Removed Fist
- Added "No Archer Weapon", "No Mage Weapon", and "No Armor" sprites
- Changed how entities are drawn so that they look like as if they're behind or infront of a wall (looks wonky because of the art but once that's fixed it should look good)
- Added the ability to pick up thrown projectiles
- Added an error popup whenever the game crashes
- Removed charged attacks (could be brought back though)
- Added piercing projectiles
- Added a new random caption
- Added the ability to delete saves
- Removed story intro (might be brought back though)
- Added the ability for certain weapons to auto-fire
- Added knockback
- Added knockback resistence tag for enemies and armor
- Added the ability to chain dashes if timed right
- Added the ability to regain mana
- Added a knockback power tag to projectiles
- Added .py files for each weapon

### Changes/Improvements

- Completely rewrote the entire code
- Improved map loading
- Changed dash input to spacebar
- Revamped inventory (it was extremely similar to survival games)
- Changed text system from .ttf based to .png based
- Text rendering is now much faster
- Changed font
- Improved player movement and made it even smoother (it used to be kinda choppy before)
- Completely redid the menus
- Optimized sliders
- Changed from stat bars to stat icons and numbers
- Completely changed how the player interacts with the inventory (hover over item with mouse to select it, use left click to equip/unequip or use right click to throw)
- Updated a bunch of sprites
- Changed how FPS works since it turned out to be broken
- Made projectiles independent of the shooter (meaning if the shooter dies the projectile won't "die" with him)
- Changed projectile's travel length to time-based rather than distance based
- Heavily improved enemy point-of-view, now it isn't a rectangle and you can hide behind walls to ambush them
- Heavily improved enemy AI (bound to change)
    - Added 4 AI phases: wander, suspicious, alert, and lookout
        - Wander: the enemy moves around its current location
        - Suspicious: the enemy moves towards the player slowly once the player enters its suspicion fov, and after a certain amount of time it will be alert
        - Alert: the enemy aggresively charges at the player and starts attacking once the player enters its alert fov or has been in its suspicion fov for a while, its alert point-of-view will also massively increase, covering the suspicion fov
        - the enemy goes to your last known location and looks for you, if it couldn't find you then it will go back to wandering
    - Hitting an enemy will cause it to look where it was hit, which also increases its alert point-of-view
- Heavily improved the debug mode's performance (used to take away up to 70% of the FPS)
- Separated between shield and armor
- Updated the "No Shield" sprite
- Heavily improved mod support
    - Added the ability to play with multiple mods
    - Added the ability to write down your own AI and add it to the game
    - Added the ability to compose your own music and add it to the game
    - Added the ability to add your own maps to the game
- Changed dashing from being player movement direction based to mouse position based
- Improved textbox rendering
- Changed FPS slider to only increase by increments of 5
- Improved how menus are linked together
- Improved camera
- Optimized collision detection
- Improved image loading
- Replaced "end destroy" and "wall destroy" projectile tags with "end stick" and "wall stick"
- Changed weapon data from being stored in a json to being stored in .py files
- Made the wooden bow shoot 5 arrows (temporary change, just for testing the new weapon code capabilities)
- Changed the stats of some weapons
- Improved button, slider, and textbox backend code
- Updated credits

### Bug Fixes

- Fixed a bug where sometimes the sliders would break
- Fixed a bug where the game could crash if the image wasn't in the image data file
- Fixed a bug where just 5 projectiles would hinder the FPS
- Fixed a bug where projectiles wouldn't rotate if their path has changed
- Fixed a bug where you can still attack with an empty quiver or mana, causing the stat to go to negative numbers
- Fixed a bug where UIs can sometimes appear above one another
- Fixed a bug where holding the dash button will allow you to perform the next dash (should be based on button presses ONLY)
<br>
  
## Dev 1.5 (Combat)

### Additions/Removals

- Added real-time combat
- Added melee attacks (direction depends on where your mouse is)
- Added magic attacks (direction depends on where your mouse is)
- Added ranged attacks (direction depends on where your mouse is)
- Added the ability of having multiple classes, now the max amount of classes you can have is 2
- Added projectiles
    - It contains 5 types: normal, mouse follow, nearest target follow, boomerang, and drop from sky (somehow even working when you are locked inside a box
    - It contains different speed attributes
    - It has a max range, with each projectile type does something about this range
        - Normal, Mouse Follow, Nearest Target Follow: stops once reaches the range
        - Drop From Sky: Ignores range limit
        - Boomerange: Returns back once the projectile reaches the limit
    - Some projectiles can go through enemies
- Added discord rich presence
- Added a functional music volume slider
- Added dual wielding
- Added the ability for enemies to damage the player
- Added dodging
    - Rolling: ~250 pixels in 0.4 secs (10 pixels per frame, 1 stamina loss)
    - Dashing: ~300 pixels in 0.34 secs (15 pixels per frame, 2 stamina loss)
- Added functional defense for enemies and player
- Added a ranged enemy, with its own AI (moves back when player is near, sprints towards the player if the player is far, and moves around semi-randomly to dodge player attacks and shoots 3 arrows at random times)
- Added the ability for enemies to go towards the last time they saw you when you leave their line of sight
- Added more collision capabilities
- Added a boss (it has 2 phases, phase 1 has 3 attacks and phase 2 has 6 attacks in total... and the game became a bullet-hell :))

### Changes/Improvements
- Improved player stats
- Updated the "No Shield" sprite (it looked childish)
- Slight change to the "Wooden Shield" sprite (to fit with the new "No Shield" sprite)
- Improved image rendering
- Improved image loading
- Complete overhaul of the assets folder
- Completely new camera system
    - It can be set to be behind the player or exactly at the player
    - It now has the ability to focus on/move to other entities
    - It now has the ability to focus on/move to a specific location
- Revamed the UI
    - Moved the inventory to the right
    - Moved the player stats to the left
    - Added text that shows your attack strength
    - Added text that shows your defense
    - Added text that shows your money
    - Added text that shows your level
    - Added icons for each bar and text
- Improved memory management for music (should hopefully take less RAM)
- Changed weight effects from changing your speed to changing you acceleration and stamina cost
- Improved test enemy movement AI
- Improved debug collision rendering
- Updated the credits
- Improved text rendering (it used to be a massive performance bottleneck)
- Improved inventory rendering, making it less of a bottleneck for performance

### Bug Fixes

- Fixed a bug where throwing items would crash your game
- Fixed a bug where the equipment slots would render as 3 slots instead of 2
- Fixed a bug where enemies slingshot you when they touch you
- Fixed a bug where thrown equipments that are then picked up can crash your game
- Fixed a bug where you couldn't see the chosen slots when your resolution was set to 4:3
- Fixed a bug where the game crashes when you try to equip an empty item
- Fixed a bug where the debug menu appears behind buttons in the settings menu and its pages
- Fixed a bug where equiping an item after throwing another item from the equipment would crash the game
- Fixed a bug where you couldn't play the game unless you are in the dev room (bug was in the leaked version)

### Known Issues

- You can still teleport when you press a movement key in the pause menu
- projectiles don't change their rotations when they have to (I tried to fix it but it caused an uncontrollable lag)
<br>

## Dev 1.4.2

### Bug Fixes

- For some reason most of the files and folders didn't update from 1.3 to 1.4, which should now work

## Dev 1.4.1

### Bug Fixes

- Fixed a bug where the game crashed trying to look for the settings file, which didn't generate yet

## Dev 1.4 (Improvements)

### Additions/Removals

- Added MacOS and Linux support
- Added acceleration and friction to all moveable entities (enemies don't have it yet though)
- Added main menu music (though it plays throughout the entire game for now)
- Added pre-game settings (like player class and game difficulty)
- Added permadeath mode which is only accessible by beating hard mode (though it doesn't do anything till now)
- Added smooth movement to enemies
- Added the ability to hold multiple stacks of one item in your inventory
- Removed ticks from the debug menu
- Removed combat temporarily
- Removed daylight cycle

### Changes/Improvements

- Moved the "save.json" and "settings.json" files from "AppData\Local\.inseynia\saves\" to "InseyniaDir\scripts\data\"
- Replaced exit button with return button in the pause menu
- Improved story text rendering
- Improved enemy detection
- The game will no longer screw over small resolution settings, the window size will almost always be the same
- Improved brightness backend
- Improved inventory rendering
- Improved map rendering
- Improved button rendering
- Improved player bars (health bar and stamina/projectiles/mana bar) rendering
- Made the game run MUCH smoother, jumping from 80 FPS all the way up to ~500 FPS (tested on an Intel core i5 6200U)

### Bug Fixes

- Fixed a bug where some entities render on-top of HUD
- Fixed a bug where some texts were using a different font (there might be some remains)
- Fixed a bug where the "Press space to continue" text is merged with the story text in low resolutions
- Fixed a bug where the map sometimes doesn't show the area it is supposed to show
- Fixed a bug where the map can get misplaced when you change your resolution

### Known Issues

- You can teleport when you press a movement key in the pause menu
- Touching enemies can slingshot you off the map
<br>

## Dev 1.3.1

### Bug Fixes

- Fixed player and enemy positioning problems when a fight starts

## Dev 1.3 (Maps)

### Additions/Removals

- Added a message saying "the game was not optimized for resolutions over 1080p" when you choose your resolution as "current"
- Added rooms to the main game
- Added minor mod support
- Added indivdual page skipping in the story
- Added world collision for enemies
- Added undertale-like combat when you choose special attack (each class has a different thing to do)

### Changes/Improvements

- Improved brightness and cleaned up code related to it
- Massively improved story text rendering and is now faster
- Changed the crash easter egg from being just totally random to having a 0.1% chance of occuring
- Now the story will move to the next page only if you press space bar instead of taking 5 seconds then automatically move to the next page

### Bug Fixes

- Fixed a bug where the FPS slider doesn't start where it should be when the FPS is set to the lowest option
- Fixed a bug where text boxes can delete player-written text
- Fixed a bug where the story images won't appear
- Fixed flipped daylight cycle (again)
- Fixed a bug where the semi-transparent black overlay in the pause menu didn't update if the resolution was changed in-game
- Enemies now no longer get slower/faster depending on the FPS
- Fixed Daylight cycle timing issues
- Fixed a bug where the daylight cycle stops working once half of the cycle is finished
- Fixed a bug where the attack cooldown didn't sync with different FPS (i.e. the enemy's turn)
<br>

## Dev 1.2.1

### Bug Fixes

- Fixed a major bug where the settings file generator was outdated, causing the game to crash once it starts (after the story)

## Dev 1.2 (Effects)

### Additions/Removals

- Added credits
- Added proper rooms (only in the dev room)
- Added a black outline to the test player to make it easier to see
- Added tile collisions (can be viewed in the dev room)
- Added scroll effect (only in the dev room)

### Changes/Improvements

- Improved text rendering
- Improved player spawning

### Bug Fixes

- Fixed a bug where if you have the max amount of an item you can carry and then pick it up, it will disappear from the ground yet you won't get the item
- Fixed a bug where the pick-up range of items was longer in one side but not the other
<br>

## Dev 1.1.1

### Additions/Removals

- Added "Always Day" and "Always Night" areas

### Bug Fixes

- Fixed a bug where day and night were swapped

## Dev 1.1 (Time)

### Additions/Removals

- Added daylight cycle

### Bug Fixes

- Fixed a bug where the FPS counter won't update
- Fixed a bug where people with screen larger than UHD can have weird background problems
<br>

## Dev 1.0.1

### Additions/Removals

- Added pause menu
<br>

## Dev 1.0

### Release

- Released to GitHub
