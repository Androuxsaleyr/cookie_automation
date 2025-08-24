// ==UserScript==
// @name         Cookie Clicker AI + Fallback (Upgrades First + Smart Buildings)
// @namespace    http://your.namespace.here
// @version      4.0
// @description  Sends game state to Flask, executes AI recommendations, and falls back to upgrades + smart building purchases
// @match        https://orteil.dashnet.org/cookieclicker/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    console.log("✅ Violentmonkey script injected");

    const waitForGame = setInterval(() => {
        if (typeof Game !== 'undefined' && Game.ready && Game.cookies > 0) {
            clearInterval(waitForGame);
            console.log("🚀 Game is ready. Starting game state loop...");

            const sendGameState = () => {
                try {
                    const upgrades = [];
                    let count = 0;
                    for (let id in Game.UpgradesById) {
                        if (count >= 100) break;
                        const upg = Game.UpgradesById[id];
                        upgrades.push({
                            id: parseInt(id),
                            name: upg.name,
                            basePrice: upg.basePrice,
                            bought: upg.bought,
                            unlocked: upg.unlocked
                        });
                        count++;
                    }

                    const buildings = [];
                    for (let id in Game.ObjectsById) {
                        const bld = Game.ObjectsById[id];
                        buildings.push({
                            id: parseInt(id),
                            name: bld.name,
                            price: bld.price,
                            baseCps: bld.storedCps,
                            storedTotalCps: bld.storedTotalCps,
                            bought: bld.amount,
                            locked: bld.locked
                        });
                    }

                    const payload = {
                        cookies: Game.cookies,
                        cps: Game.cookiesPs,
                        upgrades: upgrades,
                        buildings: buildings
                    };

                    console.log("📤 Sending game state to Flask:", payload);

                    fetch("http://127.0.0.1:5000/save-game-state", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    })
                    .then(res => res.json())
                    .then(data => {
                        console.log("✅ Flask response:", data);
                        setTimeout(fetchAndExecuteRecommendation, 1000); // Delay to avoid race condition
                    })
                    .catch(err => {
                        console.error("❌ Error sending game state:", err);
                        runFallbackStrategy(); // Fallback if saving fails
                    });
                } catch (error) {
                    console.error("❌ Error collecting game state:", error);
                    runFallbackStrategy();
                }
            };

            const fetchAndExecuteRecommendation = async () => {
                try {
                    const res = await fetch("http://127.0.0.1:5000/recommend", {
                        method: "POST"
                    });
                    const data = await res.json();
                    const lines = data.recommendation?.trim().split("\n");

                    if (!lines || lines.length === 0 || !lines[0].includes(":")) {
                        console.warn("⚠️ AI recommendation missing or invalid. Running fallback strategy...");
                        runFallbackStrategy();
                        return;
                    }

                    lines.forEach(line => {
                        if (line.startsWith("upgrade:")) {
                            const id = parseInt(line.split(":")[1]);
                            const upgrade = Game.UpgradesById[id];
                            if (upgrade && !upgrade.bought && upgrade.unlocked && Game.cookies >= upgrade.basePrice) {
                                console.log(`🛒 Buying upgrade ${id}: ${upgrade.name}`);
                                upgrade.buy();
                            }
                        } else if (line.startsWith("building:")) {
                            const [idStr, amountStr] = line.split(":")[1].split(",");
                            const id = parseInt(idStr);
                            const amount = parseInt(amountStr);
                            const building = Game.ObjectsById[id];
                            if (building && building.locked === 0) {
                                console.log(`🏗️ Buying ${amount} of building ${id}: ${building.name}`);
                                for (let i = 0; i < amount; i++) {
                                    if (Game.cookies >= building.price) {
                                        building.buy(1);
                                    } else {
                                        break;
                                    }
                                }
                            }
                        }
                    });
                } catch (err) {
                    console.error("❌ Error fetching or executing recommendation:", err);
                    console.warn("⚠️ Running fallback strategy due to error...");
                    runFallbackStrategy();
                }
            };

            const runFallbackStrategy = () => {
                // Step 1: Buy all affordable unlocked upgrades
                Object.values(Game.UpgradesById).forEach(upg => {
                    if (upg.unlocked && !upg.bought && Game.cookies >= upg.basePrice) {
                        console.log(`🛠️ Fallback: Buying upgrade ${upg.id}: ${upg.name}`);
                        upg.buy();
                    }
                });

                // Step 2: Buy one of each newly unlocked building
                Object.values(Game.ObjectsById).forEach(building => {
                    if (building.locked === 0 && building.amount === 0 && Game.cookies >= building.price) {
                        console.log(`🏗️ Fallback: Buying first unit of building ${building.id}: ${building.name}`);
                        building.buy(1);
                    }
                });

                // Step 3: Spend remaining cookies on efficient buildings
                Object.values(Game.ObjectsById).forEach(building => {
                    while (Game.cookies >= building.price && building.locked === 0) {
                        console.log(`🏗️ Fallback: Buying more of building ${building.id}: ${building.name}`);
                        building.buy(1);
                    }
                });
            };

            // Run immediately
            sendGameState();

            // Repeat every 30 seconds
            setInterval(() => {
                sendGameState();
            }, 30000);
        } else {
            console.log("⏳ Waiting for Game to be ready...");
        }
    }, 1000);
})();
