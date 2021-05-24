from simulation.Simulation import SatelliteSim

def Reward_v1(new_state, state, action):
    """
    First version of the reward function. The structure is define as:
        +10 Dumps analyzed image
        -10 per big fails (takes image over non valid zone, dumps image over non valid zone)
    
    Input: 
        - new_state = [t, theta, busy, used_memory, images_vec, memory_analyzed, target_loc, groundstation]
        - state = [t, theta, busy, images_vector, binary_analysed_picture] 
        - action = integer representing each action
        - sim = curreent satellite simulation
    """ 
    R = 0
    if action!=3 and state[2]==1:
        R -= 50
    else:
        if action == SatelliteSim.ACTION_TAKE_IMAGE:
            # Picture were correctly taken
            if state[3]<new_state[3]:
                R+=0.01*(new_state[3]-state[3])
            else:
                R-=10

        if action == SatelliteSim.ACTION_DUMP:
            # Files have been correctly dumped
            if state[4] > new_state[4]:
                R+=10*(new_state[4]-state[4])
            else:
                R-=10
    if all([state[i]==new_state[i] for i in range(len(state))]):
        # So the spacecraft does something
        R -= 0.001 
    return R