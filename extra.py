# Import all the shortcuts, an handy way of using the unified_planning framework
from unified_planning.shortcuts import *

# Declaring types
Location = UserType("Location")
Robot = UserType("Robot")
Item = UserType("Item")

# Creating problem predicates
robot_at = Fluent("robot_at", BoolType(), r=Robot, l=Location)
item_at = Fluent("item_at", BoolType(), it=Item, l=Location)
gripper_free = Fluent("gripper_free", BoolType(), r=Robot)
robot_carry = Fluent("robot_carry", BoolType(), r=Robot, it=Item)
robot_store = Fluent("robot_store", BoolType(), r=Robot, it=Item)
in_trash = Fluent("in_trash", BoolType(), it=Item)
connected = Fluent("connected", BoolType(), fr=Location, to=Location)

distance = Fluent('distance', IntType(), fr=Location, to=Location)
weight = Fluent('weight', IntType(), it=Item)
max_load = Fluent('max_load', IntType(), r=Robot)
current_load = Fluent('current_load', IntType(), r=Robot)

# Creating constants
Large_deposit = Object("Large_deposit", Location)

# Creating move actions
move = DurativeAction("move", r=Robot, fr=Location, to=Location)

r = move.parameter("r")
fr = move.parameter("fr")
to = move.parameter("to")

move.set_fixed_duration(distance(fr, to))

move.add_condition(StartTiming(), robot_at(r, fr))
move.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), connected(fr, to))
move.add_condition(StartTiming(), to != Large_deposit)

move.add_effect(EndTiming(), robot_at(r, to), True)
move.add_effect(StartTiming(), robot_at(r, fr), False)

# Creating pick actions
pick = DurativeAction("pick", it=Item, l=Location, r=Robot)

it = pick.parameter("it")
l = pick.parameter("l")
r = pick.parameter("r")

pick.set_fixed_duration(2)

pick.add_condition(StartTiming(), item_at(it, l))
pick.add_condition(StartTiming(), robot_at(r, l))
pick.add_condition(StartTiming(), gripper_free(r))

pick.add_effect(EndTiming(), robot_carry(r, it), True)
pick.add_effect(StartTiming(), item_at(it, l), False)
pick.add_effect(StartTiming(), gripper_free(r), False)

# Creating drop actions
drop = DurativeAction("drop", it=Item, l=Location, r=Robot)

it = drop.parameter("it")
l = drop.parameter("l")
r = drop.parameter("r")

drop.set_fixed_duration(2)

drop.add_condition(StartTiming(), robot_carry(r, it))
drop.add_condition(StartTiming(), robot_at(r, l))

drop.add_effect(EndTiming(), item_at(it, l), True)
drop.add_effect(EndTiming(), gripper_free(r), True)
drop.add_effect(StartTiming(), robot_carry(r, it), False)


# Creating load actions
load = DurativeAction("load", it=Item, r=Robot)

it = load.parameter("it")
r = load.parameter("r")

load.set_fixed_duration(1)

load.add_condition(StartTiming(), robot_carry(r, it))
load.add_condition(StartTiming(), GE(max_load(r), Plus(current_load(r), weight(it))))

load.add_increase_effect(timing=EndTiming(), fluent=current_load(r), value=1)
load.add_effect(EndTiming(), robot_store(r, it), True)
load.add_effect(EndTiming(), gripper_free(r), True)
load.add_effect(StartTiming(), robot_carry(r, it), False)

# Creating unload actions
unload = DurativeAction("unload", it=Item, r=Robot)

it = unload.parameter("it")
r = unload.parameter("r")

unload.set_fixed_duration(1)

unload.add_condition(StartTiming(), robot_store(r, it))
unload.add_condition(StartTiming(), robot_at(r, Large_deposit))

unload.add_decrease_effect(EndTiming(), current_load(r), weight(it))
unload.add_effect(EndTiming(), in_trash(it), True)
unload.add_effect(StartTiming(), robot_store(r, it), False)

################################################################################
# Declaring objects
table = Object("table", Location)
floor = Object("floor", Location)
bottle = Object("bottle", Item)
newspaper = Object("newspaper", Item)
rotten_apple = Object("rotten_apple", Item)
walle = Object("walle", Robot)

# Populating the problem with initial state and goals
problem = Problem("deposit")

problem.add_fluent(robot_at, default_initial_value=False)
problem.add_fluent(item_at, default_initial_value=False)
problem.add_fluent(gripper_free, default_initial_value=False)
problem.add_fluent(robot_carry, default_initial_value=False)
problem.add_fluent(robot_store, default_initial_value=False)
problem.add_fluent(in_trash, default_initial_value=False)
problem.add_fluent(connected, default_initial_value=False)

problem.add_fluent(distance, default_initial_value=0)
problem.add_fluent(weight, default_initial_value=0)
problem.add_fluent(max_load, default_initial_value=0)
problem.add_fluent(current_load, default_initial_value=0)

problem.add_action(move)
problem.add_action(pick)
problem.add_action(drop)
problem.add_action(load)
problem.add_action(unload)

problem.add_object(table)
problem.add_object(Large_deposit)
problem.add_object(floor)
problem.add_object(bottle)
problem.add_object(newspaper)
problem.add_object(rotten_apple)
problem.add_object(walle)

problem.set_initial_value(weight(bottle), 2)
problem.set_initial_value(weight(newspaper), 1)
problem.set_initial_value(weight(rotten_apple), 1)

problem.set_initial_value(max_load(walle), 6)
problem.set_initial_value(current_load(walle), 0)

problem.set_initial_value(distance(floor, table), 10)
problem.set_initial_value(distance(table, floor), 10)
problem.set_initial_value(distance(floor, Large_deposit), 50)
problem.set_initial_value(distance(Large_deposit, floor), 50)
problem.set_initial_value(distance(table, Large_deposit), 40)
problem.set_initial_value(distance(Large_deposit, table), 40)

problem.set_initial_value(connected(floor, table), True)
problem.set_initial_value(connected(table, floor), True)
problem.set_initial_value(connected(floor, Large_deposit), True)
problem.set_initial_value(connected(Large_deposit, floor), True)
problem.set_initial_value(connected(table, Large_deposit), True)
problem.set_initial_value(connected(Large_deposit, table), True)

problem.set_initial_value(robot_at(walle, table), True)

problem.set_initial_value(gripper_free(walle), True)

problem.set_initial_value(item_at(bottle, floor), True)
problem.set_initial_value(item_at(newspaper, floor), True)
problem.set_initial_value(item_at(rotten_apple, floor), True)

problem.add_goal(in_trash(bottle))
problem.add_goal(in_trash(newspaper))
problem.add_goal(in_trash(rotten_apple))

with OneshotPlanner(name='aries', problem_kind=problem.kind) as planner:
    result = planner.solve(problem)
    if result.status in unified_planning.engines.results.POSITIVE_OUTCOMES:
        print(f"{planner.name} found this plan: {result.plan}")
    else:
        print("No plan found.")