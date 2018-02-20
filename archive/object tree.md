# Object tree
Resource
	Gas
		Air(Gas)
	Solid
		Ore(Solid)
		Metal(Solid)
			Uranuim(Metal)
			Steel(Metal)
	Liquid
		Water(Liquid)
	Plasma
	Exotic
		Antimatter(Exotic)
	
Component
	Container
		FuelTank(Container)
		Hopper(Container)
	Drive
		ChemicalDrive(Drive)
		FissionDrive(Drive)
		AntimatterDrive(Drive)
	MiningTool
		MiningDrill(MiningTool)
		MiningLaser(MiningTool, Weapon)
	Generator
		ElectricalGenerator(Generator)
	AICore
	CollectionTool
		CollectionArm(CollectionTool)
		TractorBeam(CollectionTool)
	Weapon

Assembly
	Ship
		Drive
		FuelTank(Container)
		AICore
		
	Miner(Ship)
		Generator
		MiningTool
		CollectionTool
		Hopper(Container)
		
	
