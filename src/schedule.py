from collections import defaultdict

from mesa.time import RandomActivation


# class RandomActivationByBreed(RandomActivation):
#     '''
#     A scheduler which activates each type of agent once per step, in random
#     order, with the order reshuffled every step.

#     This is equivalent to the NetLogo 'ask breed...' and is generally the
#     default behavior for an ABM.

#     Assumes that all agents have a step() method.
#     '''

#     def __init__(self, model):
#         super().__init__(model)
#         self.agents_by_breed = defaultdict(dict)

#     def add(self, agent):
#         '''
#         Add an Agent object to the schedule

#         Args:
#             agent: An Agent to be added to the schedule.
#         '''

#         self._agents[agent.unique_id] = agent
#         agent_class = type(agent)
#         self.agents_by_breed[agent_class][agent.unique_id] = agent

#     def remove(self, agent):
#         '''
#         Remove all instances of a given agent from the schedule.
#         '''

#         del self._agents[agent.unique_id]

#         agent_class = type(agent)
#         del self.agents_by_breed[agent_class][agent.unique_id]

#     def step(self, by_breed=True):
#         '''
#         Executes the step of each agent breed, one at a time, in random order.

#         Args:
#             by_breed: If True, run all agents of a single breed before running
#                       the next one.
#         '''
#         if by_breed:
#             for agent_class in self.agents_by_breed:
#                 # if agent_class.__name__ == "Household": # Households need seperate treatment
#                 self.step_breed(agent_class)
#             self.steps += 1
#             self.time += 1
#         else:
#             super().step()

#     def step_breed(self, breed):
#         '''
#         Shuffle order and run all agents of a given breed.

#         Args:
#             breed: Class object of the breed to run.
#         '''
#         agent_keys = list(self.agents_by_breed[breed].keys())
#         self.model.random.shuffle(agent_keys)
#         for agent_key in agent_keys:
#             self.agents_by_breed[breed][agent_key].step()

#     def get_breed_count(self, breed_class):
#         '''
#         Returns the current number of agents of certain breed in the queue.
#         '''
#         return len(self.agents_by_breed[breed_class].values())

class EgyptSchedule(RandomActivation):
    '''
    A scheduler which activates each type of agent once per step, in a sequence defined by the original NetLogo implementation

    Modifies a default scheduler by calling functions in a specific order "breed" (class) by breed in a random order.

    Does not require a step function due to specificity of ordering for household methods
    '''

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(dict)

    def add(self, agent):
        '''
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        '''

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        '''
        Executes the step of each agent breed, one at a time.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        '''
        if by_breed:
            for agent_class in self.agents_by_breed:
                if agent_class.__name__ == "Household": # Households need seperate treatment for ordering of changeover and rental after farming has occured
                    self.step_Households(agent_class)
                else:
                    self.step_breed(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_breed(self, breed):
        '''
        Shuffle order and run all agents of a given breed.

        Args:
            breed: Class object of the breed to run.
        '''
        agent_keys = list(self.agents_by_breed[breed].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_breed[breed][agent_key].step()

    def step_Households(self, breed):
        '''
        Shuffle order and run all agents of a given household.

        Args:
            breed: Class object of the breed to run.
        '''
        # Sorting functor
        def wealth(key):
            return self.agents_by_breed[breed][key].grain

        agent_keys = list(self.agents_by_breed[breed].keys())
        # self.model.random.shuffle(agent_keys)

        agent_keys.sort(key = wealth) # Sort agents on wealth as in NetLogo ver. Simulates the increased "buying power" of the more wealthy households.
        for agent_key in agent_keys:
            self.agents_by_breed[breed][agent_key].stepFarm()

        for agent_key in agent_keys:
            self.agents_by_breed[breed][agent_key].stepRentConsumeChangeover()

    def get_breed_count(self, breed_class):
        '''
        Returns the current number of agents of certain breed in the queue.
        '''
        return len(self.agents_by_breed[breed_class].values())
