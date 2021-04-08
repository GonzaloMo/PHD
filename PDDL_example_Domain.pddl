(define (domain Simple_rover)
(:requirements :fluents :typing :durative-actions )
(:types 
	rover sample - moveable
	zone - Zone
	starting connection zone sample_location deposit - location
)
(:predicates
	(inside ?r - rover ?z - Zone)
	(connected ?from ?to - location)
	(at ?m - moveable ?l - location)
	(in ?r - rover ?s - sample)
)
(:functions
	(distance ?l1 ?l2 - location)
	(Dt_zone_change ?z1 ?z2 - Zone)
	(pickup-time)
	(Drop-time)
	(speed ?r - rover)
)

(:durative-action move_to_location
	:parameters (?r - rover ?from ?to - location)
	:duration (= ?duration (/ (distance ?from ?to) (speed ?r)))
	:condition (and 
		(at start (at ?r ?from))
		(over all (connected ?from ?to))
	)
	:effect (and 
		(at start (not (at ?d ?from)))
		(at end (at ?d ?to))
	)
)

(:durative-action move_to_zone
	:parameters (?r - rover ?from ?to - connection ?z1 ?z2 - Zone)
	:duration (= ?duration Dt_zone_change ?z1 ?z2)
	:condition (and 
		(at start (at ?r ?from))
		(at start (inside ?r ?z1))
		(over all (connected ?from ?to))
	)
	:effect (and 
		(at start (not (at ?r ?from)))
		(at start (not (inside ?r ?z1)))
		(at end (at ?d ?to))
		(at end (inside ?r ?z2))
	)
)
(:durative-action pickup_sample 
        :parameters (?r - rover ?s - sample ?l - location)
        :duration (= ?duration (pickup-time))
        :condition (and
            (at start (at ?s ?l))
            (at start (at ?r ?l))
        )
        :effect (and 
            (at end (not (at ?s ?l)))
            (at end (in ?r ?s)
        )
)
(:durative-action drop_sample 
        :parameters (?r - rover ?s - sample ?l - location)
        :duration (= ?duration (drop-time))
        :condition (and
            (at start (in ?r ?s))
            (at start (at ?r ?l))
        )
        :effect (and 
            (at end (at ?s ?l))
            (at end (not (in ?r ?s))
        )
)

	
	
