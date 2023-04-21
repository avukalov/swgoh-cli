db.getCollection('guilds').aggregate([
    { $match: { 'profile.id': '3ORoPEETQ2CdOCEn9JHlOA' } },
    //{ $match: { 'profile.id': { $in : ['jrl9Q-_CRDGdMyNjTQH1rQ', 'Tv_j9nhRTgufvH7C7oUYAA', '3ORoPEETQ2CdOCEn9JHlOA']} } },
    { $project: { member: 1, profile: 1 } },
    { $unwind: "$member" },
    {
        $lookup: {
            from: "players",
            localField: "member.playerId",
            foreignField: "playerId",
            pipeline: [
                {
                    $project: {
                        profileStat: 1,
                        rosterUnit: {
                            $let: {
                                vars: { gls: ["JABBATHEHUTT:SEVEN_STAR", "JEDIMASTERKENOBI:SEVEN_STAR", "GRANDMASTERLUKE:SEVEN_STAR", "LORDVADER:SEVEN_STAR", "GLREY:SEVEN_STAR", "SITHPALPATINE:SEVEN_STAR", "SUPREMELEADERKYLOREN:SEVEN_STAR"], },
                                in: {
                                    $reduce: {
                                        input: "$rosterUnit",
                                        initialValue: [],
                                        in: {
                                            $cond: {
                                                if: { $gt: [{ $indexOfArray: ["$$gls", "$$this.definitionId"] }, -1] },
                                                then: { $concatArrays: ["$$value", ["$$this.definitionId"]] },
                                                else: { $concatArrays: ["$$value", []] }
                                            }
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            ],
            as: "member"
        }
    },
    {
        $addFields: {
            member: { $arrayElemAt: ["$member", 0] },
            gpStats: {
                $let: {
                    // member is array, we need object
                    vars: { member: { $arrayElemAt: ["$member", 0] } },
                    in: {
                        $reduce: {
                            input: "$$member.profileStat",
                            initialValue: {},
                            in: {
                                memberGp: {
                                    $arrayElemAt: [
                                        "$$member.profileStat.value",
                                        {
                                            $indexOfArray: [
                                                "$$member.profileStat.nameKey",
                                                "STAT_GALACTIC_POWER_ACQUIRED_NAME"
                                            ]
                                        }
                                    ]
                                },
                                characterGp: {
                                    $arrayElemAt: [
                                        "$$member.profileStat.value",
                                        {
                                            $indexOfArray: [
                                                "$$member.profileStat.nameKey",
                                                "STAT_CHARACTER_GALACTIC_POWER_ACQUIRED_NAME"
                                            ]
                                        }
                                    ]
                                },
                                shipGp: {
                                    $arrayElemAt: [
                                        "$$member.profileStat.value",
                                        {
                                            $indexOfArray: [
                                                "$$member.profileStat.nameKey",
                                                "STAT_SHIP_GALACTIC_POWER_ACQUIRED_NAME"
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    { 
        $match: { "member.rosterUnit": { $elemMatch: { $ne: null } } } 
    },
    {
        $group: {
            _id: "$profile.id",
            guildName: { $first: "$profile.name" },
            memberCount: { $first: "$profile.memberCount" },
            guildGp: { $first: "$profile.guildGalacticPower" },
            totalGP: { $sum: { $toInt: "$gpStats.memberGp" } },
            avgTotalGp: { $avg: { $sum: [{ $toInt: "$gpStats.characterGp" }, { $toInt: "$gpStats.shipGp" }] } },
            characterGp: { $sum: { $toInt: "$gpStats.characterGp" } },
            shipGp: { $sum: { $toInt: "$gpStats.shipGp" } },
            JABBATHEHUTT: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'JABBATHEHUTT:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
            JEDIMASTERKENOBI: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'JEDIMASTERKENOBI:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
            GRANDMASTERLUKE: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'GRANDMASTERLUKE:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
            LORDVADER: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'LORDVADER:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
            GLREY: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'GLREY:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
            SITHPALPATINE: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'SITHPALPATINE:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
            SUPREMELEADERKYLOREN: {
                $sum: {
                    $cond: [
                        {
                            $in: [
                                'SUPREMELEADERKYLOREN:SEVEN_STAR',
                                '$member.rosterUnit'
                            ]
                        },
                        1,
                        0
                    ]
                }
            },
        }
    },
    
    
    

])
