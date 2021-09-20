<h1>Inseynia</h1>
<br>
<h3>Welcome to Bolgerna!</h3>
<p>The land of mystery, magic, prosperity, and mystic powers. But make sure you don’t dive in too deep; otherwise, you will regret it.</p>
<br>
<br>
<p>Anyways, this is where you can look at the code and help find issues that you probably found while testing. We appreciate your help 🙂</p>
<lr></lr>
<h2>Change Logs</h2>
<h3>Dev 1.5 (Pre-Release updates)</h3>
<ul>
  <li>Added real-time combat</li>
  <li>Added melee attacks (direction depends on where your mouse is)</li>
  <li>Added magic attacks (direction depends on where your mouse is)</li>
  <li>Added ranged attacks (direction depends on where your mouse is)</li>
  <li>Improved player stats</li>
  <li>Fixed a bug where throwing items would crash your game</li>
  <li>Fixed a bug where the equipment slots would render as 3 slots instead of 2</li>
  <li>Updated the "No Shield" sprite (it looked childish)</li>
  <li>Slight change to the "Wooden Shield" sprite (to fit with the new "No Shield" sprite)</li>
  <li>Fixed a bug where enemies slingshot you when they touch you</li>
  <li>Added the ability of having multiple classes, now the max amount of classes you can have is 2</li>
  <li>Added projectiles
    <ul>
      <li>It contains 5 types: normal, mouse follow, nearest target follow, drop from sky (somehow even working when you are locked inside a box), boomerang</li>
      <li>It contains different speed attributes</li>
      <li>It has a max range, with each projectile type does something about this range
        <ul>
          <li>Normal, Mouse Follow, Nearest Target Follow: stops once reaches the range</li>
          <li>Drop From Sky: Ignores range limit</li>
          <li>Boomerange: Returns back once the projectile reaches the limit</li>
        </ul>
      <li>Some projectiles can go through enemies</li>
    </ul></li>
  <li>Fixed a bug where thrown equipments that are then picked up can crash your game</li>
  <li>Added discord rich presence</li>
  <li>Added a functional music volume slider</li>
  <li>Fixed a bug where you couldn't see the chosen slots when your resolution was set to 4:3</li>
  <li>Added dual wielding</li>
  <li>Added the ability for enemies to damage the player</li>
  <li>Fixed a bug where the game crashes when you try to equip an empty item</li>
  <li>Fixed a bug where the debug menu appears behind buttons in the settings menu and its pages</li>
  <li>Improved image rendering</li>
  <li>Improved image loading</li>
  <li>Complete overhaul of the assets folder</li>
  <li>Made the camera movement cooler (though the player is slightly gittery)</li>
  <li>Added evading
    <ul>
      <li>Rolling: ~250 pixels in 0.4 secs (10 pixels per frame, 1 stamina loss)</li>
      <li>Dashing: ~300 pixels in 0.34 secs (15 pixels per frame, 2 stamina loss)</li>
    </ul></li>
  <li>Fixed a bug where equiping an item after throwing another item from the equipment would crash the game</li>
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
  <li>Removed weight-based speed (the heavier the armor, the less speed you have)</li>
  <li>Added weight-based acceleration and weight-based stamina cost(the heavier the armor, the worse acceleration you have and the more stamina it takes to dash/roll)</li>
  <li>Added functional defense for enemies and player</li>
  <li>Improved test enemy movement AI</li>
  <li>Added a ranged enemy, with its own AI (moves back when player is near, sprints towards the player if the player is far, and moves around semi-randomly to dodge player attacks and shoots 3 arrows at random times)</li>
  <li>Fixed a bug where you couldn't play the game unless you are in the dev room (bug was in the leaked version)</li>
  <li>Added the ability for enemies to go towards the last time they saw you when you leave their line of sight</li>
  <li>Added rotating rectangle collisions</li>
  <li>Improved debug collision rendering</li>
  <li>Added polygon collisions</li>
<h3>Dev 1.4.2</h3>
<ul>
  <li>For some reason most of the files and folders didn't update from 1.3 to 1.4, which should now work</li>
</ul>
<h3>Dev 1.4.1</h3>
<ul>
  <li>Fixed a bug where the game crashed trying to look for the settings file, which didn't generate yet</h3>
</ul>
<h3>Dev 1.4</h3>
<ul>
  <li>Added MacOS and Linux support</li>
  <li>Moved the "save.json" and "settings.json" files from "AppData\Local\.inseynia\saves\" to "InseyniaDir\scripts\data\"</li>
  <li>Added acceleration and friction to all moveable entities (enemies don't have it yet though</li>
  <li>Fixed a bug where some entities render on-top of HUD</li>
  <li>Fixed a bug where some texts were using a different font (there might be some remains)</li>
  <li>Fixed a bug where the "Press space to continue" text is merged with the story text in low resolutions</li>
  <li>Replaced exit button with return button in the pause menu</li>
  <li>Improved story text rendering</li>
  <li>Fixed a bug where the map sometimes doesn't show the area it is supposed to show</li>
  <li>Improved enemy detection</li>
  <li>Added main menu music (though it plays throughout the entire game for now)</li>
  <li>Added this new random caption: ...yPRGDyAR yLB JMAIGLE GR BCCN GL y AyTC...</li>
  <li>Added pre-game settings (like player class and game difficulty)</li>
  <li>Added permadeath mode which is only accessible by beating hard mode (though it doesn't do anything till now)</li>
  <li>The game will no longer screw over small resolution settings, the window size will almost always be the same</li>
  <li>Added smooth movement to enemies</li>
  <li>Improved brightness backend</li>
  <li>Added the ability to hold multiple stacks of one item in your inventory</li>
  <li>Improved inventory rendering</li>
  <li>Improved map rendering</li>
  <li>Removed ticks from the debug menu</li>
  <li>Improved button rendering</li>
  <li>Improved player bars (health bar and stamina/projectiles/mana bar) rendering</li>
  <li>Made the game run MUCH smoother, jumping from 80 FPS all the way up to ~500 FPS (tested on an Intel core i5 6200U)</li>
  <li>Removed combat temporarily</li>
  <li>Fixed a bug where the map can get misplaced when you change your resolution</li>
  <li>Removed daylight cycle</li>
  <li><strong>Known Issues:</strong> 1) You can teleport when you press a movement key in the pause menu. 2) Touching enemies can slingshot you off the map</li>
</ul>
<h3>Dev 1.3.1</h3>
<ul>
  <li>Fixed player and enemy positioning problems when a fight starts</li>
</ul>
<h3>Dev 1.3</h3>
<ul>
  <li>Fixed a bug where the FPS slider doesn't start where it should be when the FPS is set to the lowest option</li>
  <li>Added a message saying "the game was not optimized for resolutions over 1080p" when you choose your resolution as "current"</li>
  <li>Improved brightness and cleaned up code related to it</li>
  <li>Fixed a bug where text boxes can delete player-written text</li>
  <li>Massively improved story text rendering and is now faster</li>
  <li>Fixed a bug where the story images won't appear</li>
  <li>Changed the crash easter egg from being just totally random to having a 0.1% chance of occuring</li>
  <li>Fixed flipped daylight cycle (again)</li>
  <li>Added rooms to the main game</li>
  <li>Added minor mod support</li>
  <li>Fixed a bug where the semi-transparent black overlay in the pause menu didn't update if the resolution was changed in-game</li>
  <li>Added indivdual page skipping in the story</li>
  <li>Now the story will move to the next page only if you press space bar instead of taking 5 seconds then automatically move to the next page</li>
  <li>Enemies now no longer get slower/faster depending on the FPS</li>
  <li>Fixed Daylight cycle timing issues</li>
  <li>Fixed a bug where the daylight cycle stops working once half of the cycle is finished</li>
  <li>Fixed a bug where the attack cooldown didn't sync with different FPS (i.e. the enemy's turn)</li>
  <li>Added world collision for enemies</li>
  <li>Added undertale-like combat when you choose special attack (each class has a different thing to do)</li>
</ul>
<h3>Dev 1.2.1</h3>
<ul>
  <li>Fixed a major bug where the settings file generator was outdated, cause the game to crash once it starts (after the story)</li>
</ul>
<h3>Dev 1.2</h3>
<ul>
  <li>Improved text rendering</li>
  <li>Added credits</li>
  <li>Fixed a bug where if you have the max amount of an item you can carry and then pick it up, it will disappear from the ground yet you won't get the item</li>
  <li>Added proper rooms (only in the dev room)</li>
  <li>Added a black outline to the test player to make it easier to see</li>
  <li>Added tile collisions (can be viewed in the dev room)</li>
  <li>Improved player spawning</li>
  <li>Added scroll effect (only in the dev room)</li>
  <li>Added a "show hitbox" hotkey (B)</li>
  <li>Fixed a bug where the pick-up range of items was longer in one side but not the other</li>
</ul>
<h3>Dev 1.1.1</h3>
<ul>
  <li>Fixed a bug where day and night were swapped</li>
  <li>Added "Always Day" and "Always Night" areas</li>
</ul>
<h3>Dev 1.1.0</h3>
<ul>
  <li>Added daylight cycle</li>
  <li>Fixed a bug where the FPS counter won't update</li>
  <li>Fixed a bug where people with screen larger than UHD can have weird background problems</li>
</ul>
<h3>Dev 1.0.1</h3>
<ul>
  <li>Added pause menu</li>
</ul>
<h3>Dev 1.0.0</h3>
<ul>
  <li>Released into GitHub</li>
</ul>
