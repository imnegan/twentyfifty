fromState,toState,condition,action
unloading,fossicking,isEmpty,cycle
fossicking,mining,foundOre,mine
mining,mining,isNotFull,mine
mining,returning,isFull
returning,unloading,isHome,unload
unloading,unloading,isNotEmpty,unload
