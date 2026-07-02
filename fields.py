FIELDS = [
    ("IsRaceOn", "i"),
    ("TimestampMS", "I"),

    ("EngineMaxRpm", "f"),
    ("EngineIdleRpm", "f"),
    ("CurrentEngineRpm", "f"),

    ("AccelerationX", "f"),
    ("AccelerationY", "f"),
    ("AccelerationZ", "f"),

    ("VelocityX", "f"),
    ("VelocityY", "f"),
    ("VelocityZ", "f"),

    ("AngularVelocityX", "f"),
    ("AngularVelocityY", "f"),
    ("AngularVelocityZ", "f"),

    ("Yaw", "f"),
    ("Pitch", "f"),
    ("Roll", "f"),

    ("NormalizedSuspensionTravelFrontLeft", "f"),
    ("NormalizedSuspensionTravelFrontRight", "f"),
    ("NormalizedSuspensionTravelRearLeft", "f"),
    ("NormalizedSuspensionTravelRearRight", "f"),

    ("TireSlipRatioFrontLeft", "f"),
    ("TireSlipRatioFrontRight", "f"),
    ("TireSlipRatioRearLeft", "f"),
    ("TireSlipRatioRearRight", "f"),

    ("WheelRotationSpeedFrontLeft", "f"),
    ("WheelRotationSpeedFrontRight", "f"),
    ("WheelRotationSpeedRearLeft", "f"),
    ("WheelRotationSpeedRearRight", "f"),

    ("WheelOnRumbleStripFrontLeft", "i"),
    ("WheelOnRumbleStripFrontRight", "i"),
    ("WheelOnRumbleStripRearLeft", "i"),
    ("WheelOnRumbleStripRearRight", "i"),

    ("WheelInPuddleFrontLeft", "i"),
    ("WheelInPuddleFrontRight", "i"),
    ("WheelInPuddleRearLeft", "i"),
    ("WheelInPuddleRearRight", "i"),

    ("SurfaceRumbleFrontLeft", "f"),
    ("SurfaceRumbleFrontRight", "f"),
    ("SurfaceRumbleRearLeft", "f"),
    ("SurfaceRumbleRearRight", "f"),

    ("TireSlipAngleFrontLeft", "f"),
    ("TireSlipAngleFrontRight", "f"),
    ("TireSlipAngleRearLeft", "f"),
    ("TireSlipAngleRearRight", "f"),

    ("TireCombinedSlipFrontLeft", "f"),
    ("TireCombinedSlipFrontRight", "f"),
    ("TireCombinedSlipRearLeft", "f"),
    ("TireCombinedSlipRearRight", "f"),

    ("SuspensionTravelMetersFrontLeft", "f"),
    ("SuspensionTravelMetersFrontRight", "f"),
    ("SuspensionTravelMetersRearLeft", "f"),
    ("SuspensionTravelMetersRearRight", "f"),

    ("CarOrdinal", "i"),
    ("CarClass", "i"),
    ("CarPerformanceIndex", "i"),
    ("DrivetrainType", "i"),
    ("NumCylinders", "i"),
    ("CarGroup", "I"),

    ("SmashableVelDiff", "f"),
    ("SmashableMass", "f"),

    ("PositionX", "f"),
    ("PositionY", "f"),
    ("PositionZ", "f"),

    ("Speed", "f"),
    ("Power", "f"),
    ("Torque", "f"),

    ("TireTempFrontLeft", "f"),
    ("TireTempFrontRight", "f"),
    ("TireTempRearLeft", "f"),
    ("TireTempRearRight", "f"),

    ("Boost", "f"),
    ("Fuel", "f"),
    ("DistanceTraveled", "f"),

    ("BestLap", "f"),
    ("LastLap", "f"),
    ("CurrentLap", "f"),
    ("CurrentRaceTime", "f"),

    ("LapNumber", "H"),

    ("RacePosition", "B"),
    ("Accel", "B"),
    ("Brake", "B"),
    ("Clutch", "B"),
    ("HandBrake", "B"),
    ("Gear", "B"),

    ("Steer", "b"),
    ("NormalizedDrivingLine", "b"),
    ("NormalizedAIBrakeDifference", "b"),
]