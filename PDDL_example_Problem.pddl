(:define (problem Problem_1)
(:domain Simple_rover)
(:requirements :fluents :typing)
    (:objects 
        r - rover
        s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 - sample
        Land - starting
		c1 c2 c3 c4 c5 c6 c7 c8 - connection
        Depo - deposit
		sl1 sl2 sl3 sl4 sl5 sl6 sl7 sl8 sl9 sl10 - sample_location
		z1 z2 z3 z4 - Zone
    )
    
    (:init
        (at r Land)
        (at s1 sl1)
        (at s2 sl2)
        (at s3 sl3)
		(at s4 sl4)
		(at s5 sl5)
		(at s6 sl6)
		(at s7 sl7)
		(at s8 sl8)
		(at s9 sl9)
        (at s10 sl10)
		(inside r z1)
		
        ;; Package
        (at pack1 wp2)
        (at pack2 wp3)
        (at pack3 wp5)
        (at pack4 wp11)

        (connected Land Depo)
        (connected Depo Land)

    )
    (:goal (and

        )
    
    )
)