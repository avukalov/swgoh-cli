db.getCollection('players').aggregate([
    { $match: { 'guildId': 'jrl9Q-_CRDGdMyNjTQH1rQ' } },
    {
        $addFields: {
            gpStats: {
                $reduce: {
                    input: "$profileStat",
                    initialValue: {},
                    in: {
                        characterGp: {
                            $arrayElemAt: [
                                "$profileStat.value",
                                {
                                    $indexOfArray: [
                                        "$profileStat.nameKey",
                                        "STAT_CHARACTER_GALACTIC_POWER_ACQUIRED_NAME"
                                    ]
                                }
                            ]
                        },
                        shipGp: {
                            $arrayElemAt: [
                                "$profileStat.value",
                                {
                                    $indexOfArray: [
                                        "$profileStat.nameKey",
                                        "STAT_SHIP_GALACTIC_POWER_ACQUIRED_NAME"
                                    ]
                                }
                            ]
                        }
                    }
                }
            },
        },
    },
    {
        $group: {
            _id: "$guildId",
            totalGp: { $sum: { $sum: [{ $toInt: "$gpStats.characterGp" }, { $toInt: "$gpStats.shipGp" }]} },
            characterGp: { $sum: { $toInt: "$gpStats.characterGp" } },
            shipGp: { $sum: { $toInt: "$gpStats.shipGp" } },
        }
    }

])