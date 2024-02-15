(define (domain deposit)
(:requirements :strips :typing :fluents :durative-actions :universal-preconditions :equality)


; Types definition
(:types
  location
  robot
  item
)

(:constants
  Large-deposit - location
)

(:predicates
  (robot_at ?r - robot ?l - location)
  (item_at ?it - item ?l - location)
  (gripper_free ?r - robot)
  (robot_carry ?r - robot ?it - item)
  (robot_store ?r - robot ?it - item)
  (in_trash ?it - item)
; Predicados añadidos
  (connected ?from ?to - location)
)

(:functions
  (distance ?l1 ?l2 - location)
  (weight ?it - item)
  (max-load ?r - robot)
  (current-load ?r - robot)
)

; Move action. The robot moves from one location (A) to another (B).
; The only precondition is that the robot must be in the initial location.
; Consequence: The robot is now at B and not at A.
(:durative-action move
  :parameters (?r - robot ?from ?to - location)
  :duration (= ?duration (distance ?from ?to))
  :condition
    (and 
      (at start (robot_at ?r ?from))
      (over all (connected ?from ?to))
      ; Need to check if the to location is not Large-deposit
      (at start (not (= ?to Large-deposit)))
    )
  :effect
    (and
      (at end (robot_at ?r ?to))
      (at start (not (robot_at ?r ?from)))
    )
)

; Pick-up action. The robot picks an object at a location.
; Both the robot and the object must be in that location.
; The robot's gripper must be free.
; Consequences:
;     - The item is no longer at the given location.
;     - The robot is now carrying the object and its gripper is not free.
(:durative-action  pick
  :parameters (?it - item ?l - location ?r - robot)
  :duration (= ?duration 2)
  :condition 
    (and
      (at start (item_at ?it ?l))
      (at start (robot_at ?r ?l))
      (at start (gripper_free ?r))
    )
:effect
  (and
    (at end (robot_carry ?r ?it))
    (at start (not (item_at ?it ?l)))
    (at start (not (gripper_free ?r))))
  )

; Drop-off action. The robot drops an object at a location.
; The robot must be in that location and must be carrying that object.
; Consequences:
;     - The item is now at the given location.
;     - The robot is no longer carrying the object and its gripper is free.
(:durative-action  drop
:parameters (?it - item ?l - location ?r - robot)
:duration (= ?duration 2)
:condition
  (and 
    (at start (robot_at ?r ?l))
    (at start (robot_carry ?r ?it))
  )
:effect 
  (and 
    (at end (item_at ?it ?l))
    (at end (gripper_free ?r))
    (at start (not (robot_carry ?r ?it)))
  )
)


; Load action. The robot picks an object that is in the storage.
; The robot's gripper must be free.
(:durative-action  load
  :parameters (?it - item ?r - robot)
  :duration (= ?duration 1)
  :condition 
    (and
      (at start (> (max-load ?r) (+ (current-load ?r) (weight ?it))))
      (at start (robot_carry ?r ?it))
    )
:effect
  (and
    (at end (increase (current-load ?r) (weight ?it)))
    (at end (gripper_free ?r))
    (at end (robot_store ?r ?it))
    (at start (not (robot_carry ?r ?it)))
  )
)

; Unload action. The robot picks an object that is in the storage.
; The robot's gripper must be free.
(:durative-action  unload
  :parameters (?it - item ?r - robot)
  :duration (= ?duration 1)
  :condition 
    (and
      (at start (robot_store ?r ?it))
      (at start (robot_at ?r Large-deposit))
    )
:effect
  (and
    (at end (decrease (current-load ?r) (weight ?it)))
    (at end (in_trash ?it))
    (at start (not (robot_store ?r ?it)))
  )
)

; Move action. The robot moves from one location (A) to another (B).
; The only precondition is that the robot must be in the initial location.
; Consequence: The robot is now at B and not at A.
(:durative-action move-to-unload
  :parameters (?r - robot ?from ?to - location)
  :duration (= ?duration (distance ?from ?to))
  :condition
    (and 
      (at start (robot_at ?r ?from))
      (over all (connected ?from ?to))
      (at start (forall (?it - item) (robot_store ?r ?it)))
      (at start (= ?to Large-deposit))
    )
  :effect
    (and
      (at end (robot_at ?r ?to))
      (at start (not (robot_at ?r ?from)))
    )
)

)