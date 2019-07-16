const robot = require("robotjs");
require('dotenv').config()

// Speed up the mouse.
robot.setMouseDelay(2);

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    const screenSize = robot.getScreenSize();
    const desktopIconLocation = {
        width: screenSize.width - 50,
        height: 30,
    };
    robot.moveMouse(desktopIconLocation.width, desktopIconLocation.height);
    robot.mouseClick();
    robot.keyTap('enter');
    await sleep(30000);
    robot.typeString(process.env.CARMODOO_ID);
    robot.keyTap('tab');
    robot.typeString(process.env.CARMODOO_PW);
    robot.keyTap('enter');
    await sleep(30000);
})();

