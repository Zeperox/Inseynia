<h1>Inseynia</h1>
<br>
<h3>Welcome to Bolgerna!</h3>
<p>The land of mystery, magic, prosperity, and mystic powers. But make sure you don’t dive in too deep; otherwise, you will regret it.</p>
<br>
<br>
<p>Anyways, this is where you can look at the code and help find issues that you probably found while testing. We appreciate your help 🙂</p>
<lr></lr>
<h1>Change Logs</h1>
<h2>Dev 1.6 (Overwrite)</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added tile, drop, and enemy IDs</li>
  <li>Added drop map and loading drops from the map</li>
  <li>Added enemy map and loading enemies from the map</li>
  <li>Added animation support to entities</li>
  <li>Added a special menu of save selection</li>
  <li>Added the ability to have up to 3 standalone saves</li>
  <li>Added a functional SFX slider (there aren't any sound effects yet though)</li>
  <li>Removed standalone enemy classes</li>
  <li>Added AI classes to group enemies</li>
  <li>Removed inventory hotbar</li>
  <li>Added inventory menu, which contains your inventory, your equipment, your stats, and a map (map isn't done yet)</li>
  <li>Removed stackable items</li>
  <li>Removed resolution setting, now it is hard-set to 1280x720 (programming the game was harder and tons of sprites broke when using different resolutions)</li>
  <li>Added item tooltip</li>
  <li>Added music room</li>
  <li>Added a song that I... totally didn't steal from cthethan</li>
  <li>Removed melee combat</li>
  <li>Removed rolling, leaving only dashes to use to avoid</li>
  <li>Added the ability for an enemy's projectile to hit other enemies</li>
  <li>Added the ability for certain projectiles to stick to the wall or "fall" to the ground</li>
  <li>Added a new dedicated slot for armor equipment</li>
  <li>Removed the second weapon slot</li>
  <li>Added secondry slot, which could either hold a shield or, if you have 2 classes, a second weapon (basically if you wanna be offensive then you gotta sacrifice using the shield)</li>
  <li>Shields no longer account for you defense and your weight</li>
  <li>Added the ability to stop projectiles when holding your shield</li>
  <li>Added the ability to cause projectiles to ricochet if you hold your shield at the correct timing (each shield has a different ricochet speed and distance)</li>
  <li>Added a small miniboss, called Ekreta Tree</li>
  <li>Removed Big Eye boss</li>
  <li>Removed Fist</li>
  <li>Added "No Archer Weapon", "No Mage Weapon", and "No Armor" sprites</li>
  <li>Changed how entities are drawn so that they look like as if they're behind or infront of a wall (looks wonky because of the art but once that's fixed it should look good)</li>
  <li>Added the ability to pick up thrown projectiles</li>
  <li>Added an error popup whenever the game crashes</li>
  <li>Removed charged attacks (could be brought back though)</li>
  <li>Added piercing projectiles</li>
  <li>Added a new random caption</li>
  <li>Added the ability to delete saves</li>
  <li>Removed story intro (might be brought back though)</li>
  <li>Added the ability for certain weapons to auto-fire</li>
  <li>Added knockback</li>
  <li>Added knockback resistence tag for enemies and armor</li>
  <li>Added the ability to chain dashes if timed right</li>
  <li>Added the ability to regain mana</li>
  <li>Added a knockback power tag to projectiles</li>
  <li>Added .py files for each weapon</li>
</ul>
<h3>Changes/Improvements</h3>
<ul>
  <li>Completely rewrote the entire code</li>
  <li>Improved map loading</li>
  <li>Changed dash input to spacebar</li>
  <li>Revamped inventory (it was extremely similar to survival games)</li>
  <li>Changed text system from .ttf based to .png based</li>
  <li>Text rendering is now much faster</li>
  <li>Changed font</li>
  <li>Improved player movement and made it even smoother (it used to be kinda choppy before)</li>
  <li>Completely redid the menus</li>
  <li>Optimized sliders</li>
  <li>Changed from stat bars to stat icons and numbers</li>
  <li>Completely changed how the player interacts with the inventory (hover over item with mouse to select it, use left click to equip/unequip or use right click to throw)</li>
  <li>Updated a bunch of sprites</li>
  <li.Changed how FPS works since it turned out to be broken</li>
  <li>Made projectiles independent of the shooter (meaning if the shooter dies the projectile won't "die" with him)</li>
  <li>Changed projectile's travel length to time-based rather than distance based</li>
  <li>Heavily improved enemy point-of-view, now it isn't a rectangle and you can hide behind walls to ambush them</li>
  <li>Heavily improved enemy AI (bound to change)
    <ul>
      <li>Added 4 AI phases: wander, suspicious, alert, and lookout
        <ul>
          <li>Wander: the enemy moves around its current location</li>
          <li>Suspicious: the enemy moves towards the player slowly once the player enters its suspicion fov, and after a certain amount of time it will be alert</li>
          <li>Alert: the enemy aggresively charges at the player and starts attacking once the player enters its alert fov or has been in its suspicion fov for a while, its alert point-of-view will also massively increase, covering the suspicion fov</li>
          <li>the enemy goes to your last known location and looks for you, if it couldn't find you then it will go back to wandering</li>
        </ul></il>
      <li>Hitting an enemy will cause it to look where it was hit, which also increases its alert point-of-view</li>
    </ul></il>
  <il>Heavily improved the debug mode's performance (used to take away up to 70% of the FPS)</li>
  <li>Separated between shield and armor</li>
  <li>Updated the "No Shield" sprite</li>
  <li>Heavily improved mod support
    <ul>
      <li>Added the ability to play with multiple mods</li>
      <li>Added the ability to write down your own AI and add it to the game</li>
      <li>Added the ability to compose your own music and add it to the game</li>
      <li>Added the ability to add your own maps to the game</li>
    </ul></li>
  <li>Changed dashing from being player movement direction based to mouse position based</li>
  <li>Improved textbox rendering</li>
  <li>Changed FPS slider to only increase by increments of 5</li>
  <li>Improved how menus are linked together</li>
  <li>Improved camera</li>
  <li>Optimized collision detection</li>
  <li>Improved image loading</li>
  <li>Replaced "end destroy" and "wall destroy" projectile tags with "end stick" and "wall stick"</li>
  <li>Changed weapon data from being stored in a json to being stored in .py files</li>
  <li>Made the wooden bow shoot 5 arrows (temporary change, just for testing the new weapon code capabilities)</li>
  <li>Changed the stats of some weapons</li>
  <li>Improved button, slider, and textbox backend code</li>
  <li>Updated credits</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where sometimes the sliders would break</li>
  <li>Fixed a bug where the game could crash if the image wasn't in the image data file</li>
  <li>Fixed a bug where just 5 projectiles would hinder the FPS</li>
  <li>Fixed a bug where projectiles wouldn't rotate if their path has changed</li>
  <li>Fixed a bug where you can still attack with an empty quiver or mana, causing the stat to go to negative numbers</li>
  <li>Fixed a bug where UIs can sometimes appear above one another</li>
  <li>Fixed a bug where holding the dash button will allow you to perform the next dash (should be based on button presses ONLY)</li>
</ul>
<br>
  
<h2>Dev 1.5 (Combat)</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added real-time combat</li>
  <li>Added melee attacks (direction depends on where your mouse is)</li>
  <li>Added magic attacks (direction depends on where your mouse is)</li>
  <li>Added ranged attacks (direction depends on where your mouse is)</li>
  <li>Added the ability of having multiple classes, now the max amount of classes you can have is 2</li>
  <li>Added projectiles
    <ul>
      <li>It contains 5 types: normal, mouse follow, nearest target follow, boomerang, and drop from sky (somehow even working when you are locked inside a box</li>
      <li>It contains different speed attributes</li>
      <li>It has a max range, with each projectile type does something about this range
        <ul>
          <li>Normal, Mouse Follow, Nearest Target Follow: stops once reaches the range</li>
          <li>Drop From Sky: Ignores range limit</li>
          <li>Boomerange: Returns back once the projectile reaches the limit</li>
        </ul>
      <li>Some projectiles can go through enemies</li>
    </ul></li>
  <li>Added discord rich presence</li>
  <li>Added a functional music volume slider</li>
  <li>Added dual wielding</li>
  <li>Added the ability for enemies to damage the player</li>
  <li>Added dodging
    <ul>
      <li>Rolling: ~250 pixels in 0.4 secs (10 pixels per frame, 1 stamina loss)</li>
      <li>Dashing: ~300 pixels in 0.34 secs (15 pixels per frame, 2 stamina loss)</li>
    </ul></li>
  <li>Added functional defense for enemies and player</li>
  <li>Added a ranged enemy, with its own AI (moves back when player is near, sprints towards the player if the player is far, and moves around semi-randomly to dodge player attacks and shoots 3 arrows at random times)</li>
  <li>Added the ability for enemies to go towards the last time they saw you when you leave their line of sight</li>
  <li>Added more collision capabilities</li>
  <li>Added a boss (it has 2 phases, phase 1 has 3 attacks and phase 2 has 6 attacks in total... and the game became a bullet-hell :))
</ul>
<h3>Changes/Improvements</h3>
<ul>
  <li>Improved player stats</li>
  <li>Updated the "No Shield" sprite (it looked childish)</li>
  <li>Slight change to the "Wooden Shield" sprite (to fit with the new "No Shield" sprite)</li>
  <li>Improved image rendering</li>
  <li>Improved image loading</li>
  <li>Complete overhaul of the assets folder</li>
  <li>Completely new camera system
    <ul>
      <li>It can be set to be behind the player or exactly at the player</li>
      <li>It now has the ability to focus on/move to other entities</li>
      <li>It now has the ability to focus on/move to a specific location</li>
    </ul></li>
  <li>Revamed the UI
    <ul>
      <li>Moved the inventory to the right</li>
      <li>Moved the player stats to the left</li>
      <li>Added text that shows your attack strength</li>
      <li>Added text that shows your defense</li>
      <li>Added text that shows your money</li>
      <li>Added text that shows your level</li>
      <li>Added icons for each bar and text</li>
    </ul></li>
  <li>Improved memory management for music (should hopefully take less RAM)</li>
  <li>Changed weight effects from changing your speed to changing you acceleration and stamina cost</li>
  <li>Improved test enemy movement AI</li>
  <li>Improved debug collision rendering</li>
  <li>Updated the credits</li>
  <li>Improved text rendering (it used to be a massive performance bottleneck)</li>
  <li>Improved inventory rendering, making it less of a bottleneck for performance</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where throwing items would crash your game</li>
  <li>Fixed a bug where the equipment slots would render as 3 slots instead of 2</li>
  <li>Fixed a bug where enemies slingshot you when they touch you</li>
  <li>Fixed a bug where thrown equipments that are then picked up can crash your game</li>
  <li>Fixed a bug where you couldn't see the chosen slots when your resolution was set to 4:3</li>
  <li>Fixed a bug where the game crashes when you try to equip an empty item</li>
  <li>Fixed a bug where the debug menu appears behind buttons in the settings menu and its pages</li>
  <li>Fixed a bug where equiping an item after throwing another item from the equipment would crash the game</li>
  <li>Fixed a bug where you couldn't play the game unless you are in the dev room (bug was in the leaked version)</li>
</ul>
<h3>Known Issues</h3>
<ul>
  <li>You can still teleport when you press a movement key in the pause menu</li>
  <li>projectiles don't change their rotations when they have to (I tried to fix it but it caused an uncontrollable lag)</li>
</ul>
<br>

<h2>Dev 1.4.2</h2>
<h3>Bug Fixes</h3>
<ul>
  <li>For some reason most of the files and folders didn't update from 1.3 to 1.4, which should now work</li>
</ul>
<h2>Dev 1.4.1</h2>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where the game crashed trying to look for the settings file, which didn't generate yet</h3>
</ul>
<h2>Dev 1.4 (Improvements)</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added MacOS and Linux support</li>
  <li>Added acceleration and friction to all moveable entities (enemies don't have it yet though)</li>
  <li>Added main menu music (though it plays throughout the entire game for now)</li>
  <li>Added pre-game settings (like player class and game difficulty)</li>
  <li>Added permadeath mode which is only accessible by beating hard mode (though it doesn't do anything till now)</li>
  <li>Added smooth movement to enemies</li>
  <li>Added the ability to hold multiple stacks of one item in your inventory</li>
  <li>Removed ticks from the debug menu</li>
  <li>Removed combat temporarily</li>
  <li>Removed daylight cycle</li>
</ul>
<h3>Changes/Improvements</h3>
<ul>
  <li>Moved the "save.json" and "settings.json" files from "AppData\Local\.inseynia\saves\" to "InseyniaDir\scripts\data\"</li>
  <li>Replaced exit button with return button in the pause menu</li>
  <li>Improved story text rendering</li>
  <li>Improved enemy detection</li>
  <li>The game will no longer screw over small resolution settings, the window size will almost always be the same</li>
  <li>Improved brightness backend</li>
  <li>Improved inventory rendering</li>
  <li>Improved map rendering</li>
  <li>Improved button rendering</li>
  <li>Improved player bars (health bar and stamina/projectiles/mana bar) rendering</li>
  <li>Made the game run MUCH smoother, jumping from 80 FPS all the way up to ~500 FPS (tested on an Intel core i5 6200U)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where some entities render on-top of HUD</li>
  <li>Fixed a bug where some texts were using a different font (there might be some remains)</li>
  <li>Fixed a bug where the "Press space to continue" text is merged with the story text in low resolutions</li>
  <li>Fixed a bug where the map sometimes doesn't show the area it is supposed to show</li>
  <li>Fixed a bug where the map can get misplaced when you change your resolution</li>
</ul>
<h3>Known Issues</h3>
<ul>
  <li>You can teleport when you press a movement key in the pause menu</li>
  <li>Touching enemies can slingshot you off the map</li>
</ul>
<br>

<h2>Dev 1.3.1</h2>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed player and enemy positioning problems when a fight starts</li>
</ul>
<h2>Dev 1.3 (World Taking Shape)</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added a message saying "the game was not optimized for resolutions over 1080p" when you choose your resolution as "current"</li>
  <li>Added rooms to the main game</li>
  <li>Added minor mod support</li>
  <li>Added indivdual page skipping in the story</li>
  <li>Added world collision for enemies</li>
  <li>Added undertale-like combat when you choose special attack (each class has a different thing to do)</li>
</ul>
<h3>Changes/Improvements</h3>
<ul>
  <li>Improved brightness and cleaned up code related to it</li>
  <li>Massively improved story text rendering and is now faster</li>
  <li>Changed the crash easter egg from being just totally random to having a 0.1% chance of occuring</li>
  <li>Now the story will move to the next page only if you press space bar instead of taking 5 seconds then automatically move to the next page</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where the FPS slider doesn't start where it should be when the FPS is set to the lowest option</li>
  <li>Fixed a bug where text boxes can delete player-written text</li>
  <li>Fixed a bug where the story images won't appear</li>
  <li>Fixed flipped daylight cycle (again)</li>
  <li>Fixed a bug where the semi-transparent black overlay in the pause menu didn't update if the resolution was changed in-game</li>
  <li>Enemies now no longer get slower/faster depending on the FPS</li>
  <li>Fixed Daylight cycle timing issues</li>
  <li>Fixed a bug where the daylight cycle stops working once half of the cycle is finished</li>
  <li>Fixed a bug where the attack cooldown didn't sync with different FPS (i.e. the enemy's turn)</li>
</ul>
<br>

<h2>Dev 1.2.1</h2>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a major bug where the settings file generator was outdated, cause the game to crash once it starts (after the story)</li>
</ul>
<h2>Dev 1.2 (Effects)</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added credits</li>
  <li>Added proper rooms (only in the dev room)</li>
  <li>Added a black outline to the test player to make it easier to see</li>
  <li>Added tile collisions (can be viewed in the dev room)</li>
  <li>Added scroll effect (only in the dev room)</li>
</ul>
<h3>Changes/Improvements</h3>
<ul>
  <li>Improved text rendering</li>
  <li>Improved player spawning</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where if you have the max amount of an item you can carry and then pick it up, it will disappear from the ground yet you won't get the item</li>
  <li>Fixed a bug where the pick-up range of items was longer in one side but not the other</li>
</ul>
<br>

<h2>Dev 1.1.1</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added "Always Day" and "Always Night" areas</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where day and night were swapped</li>
</ul>
<h2>Dev 1.1 (Time)</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added daylight cycle</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
  <li>Fixed a bug where the FPS counter won't update</li>
  <li>Fixed a bug where people with screen larger than UHD can have weird background problems</li>
</ul>
<br>
<h2>Dev 1.0.1</h2>
<h3>Additions/Removals</h3>
<ul>
  <li>Added pause menu</li>
</ul>
<br>

<h2>Dev 1.0</h2>
<h3>Release</h3>
<ul>
  <li>Released to GitHub</li>
</ul>
