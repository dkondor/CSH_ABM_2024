import random
import scipy.special as sp
import pandas as pd
# from household import Household
import household
import itertools

vec1 = pd.read_csv('demog_vectors.csv')

class Vec1:
    def __init__(self):
        self.phi = vec1.phi
        self.rho = vec1.rho
        self.pstar = vec1.pstar
        self.mstar = vec1.mstar
        self.mortscale = vec1.mortscale[0]
        self.mortparms = vec1.mortparms
        self.fertparm = vec1.fertparm[0]
        self.fertscale = vec1.fertscale[0]
        

class Agent:
    _id_iter = itertools.count(start = 1)
    def __init__(self, age, gender, household_id, vec1, fertility):
        self.id = next(Agent._id_iter)
        self.age = age
        self.gender = gender
        self.household_id = household_id
        self.vec1 = vec1  
        self.is_alive = True  
        self.newborn_agents = []
        self.fertility = fertility
        self.marital_status = 'single'
        self.partner_id = None
        # self.children_ids = []

    def get_age_group_index(self):
        """Determine the age group index for the agent."""
        
        if self.age >= len(self.vec1.phi):
            return len(self.vec1.phi) - 1
        return self.age

    def consume_resources(self):
        """Simulate resource consumption based on effectiveness and consumption parameters."""
        if self.is_alive:
            age_index = self.get_age_group_index()
            phi = self.vec1.phi[age_index]
            rho = self.vec1.rho[age_index]
            consumption_amount = rho * 10

    def work(self):
        """Simulate work done by the agent based on effectiveness parameter."""
        work_output = 0
        if self.is_alive:
            age_index = self.get_age_group_index()
            phi = self.vec1.phi[age_index]
            work_output = phi 
            return work_output
        return work_output
    
    def age_and_die(self, household, village):

        """Simulate aging, survival, and reproduction based on probabilities."""
        if not self.is_alive:
            return
        
        self.age += 1
        # Get z
        
        total_food = sum(i for (i, j) in household.food_storage)
        personal_portion = self.age/sum(agent.age for agent in household.members)
        z = personal_portion/total_food if total_food > 0 else 0

        p0 = self.vec1.pstar * sp.gdtr(1.0 / self.vec1.mortscale, self.vec1.mortparms, z)
        m0 = self.vec1.mstar * sp.gdtr(1.0 / self.vec1.fertscale, self.vec1.fertparm, z)
        
        age_index = self.get_age_group_index()
        survival_probability = p0[age_index]  # survival probability
        if random.random() > survival_probability:
            self.is_alive = False
            partner = village.get_agent_by_id(self.partner_id)
            if partner:
                partner.marital_status = 'single'
                # partner.partner_id = None
            return
        
        fertility_probability = m0[age_index]
        self.fertility = fertility_probability
        if random.random() < fertility_probability and self.gender == 'female' and self.marital_status == 'married':
            if len(household.members) < 5 or village.is_land_available():
        # if random.random() < fertility_probability and self.gender == 'female':
            # print(f"Agent {self.household_id} reproduces at age {self.age}.")
                self.reproduce()
    
    def reproduce(self):
        """Simulate reproduction by adding new agents to the household."""
        new_agent = Agent(
        age = 0, 
        gender=random.choice(['male', 'female']),  
        household_id=self.household_id,
        vec1=self.vec1,
        fertility = 0
        )
        print(f"Newborn Agent added to Household {self.household_id}.")
        self.newborn_agents.append(new_agent)
    
    def marry(self, partner):
        """Marry another agent."""
        self.marital_status = 'married'
        self.partner_id = partner.id
        partner.marital_status = 'married'
        partner.partner_id = self.id



