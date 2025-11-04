"""
Murène Empathic Engine
Complete source code for empathic intelligence framework
Louis Leprieur & Grok (xAI)
November 2, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

class Agent:
    def __init__(self, utility: float, is_political: bool = False, action: float = 0.0):
        self.utility = utility
        self.is_political = is_political
        self.action = action

class MureneSystem:
    def __init__(self, num_agents: int = 4):
        self.N = num_agents
        self.params = self.default_params()
        self.agents = [Agent(1.0) for _ in range(self.N)]  # Default agents
        self.W = np.ones((self.N, self.N)) * 0.5
        np.fill_diagonal(self.W, 0)
        self.D = 5.0
        self.Dm = 1000.0
        self.reparations = 0.0
        self.step_count = 0
        self.history = {'B': [], 'Dm': [], 'U': [], 'D': [], 'R': []}
    
    def default_params(self) -> Dict[str, float]:
        return {
            'H': 10.0, 'gamma_0': 0.8, 'I': 5.0, 'k_stress': 2.0,
            'beta': 0.80, 'delta': 1.20, 'epsilon': 0.18, 
            'lambda_debt': 0.0005, 'zeta': 0.20, 'lambda_cog': 0.7,
            'r_int': 0.1, 'mu': 0.05, 'eta_global': 0.1,
            'rho': 0.40, 'gamma_ext': 1.0, 'P_ext': 10.0
        }
    
    def empathy_field(self, i: int) -> float:
        """Calculate empathy field for agent i"""
        E_i = 0.0
        for j in range(self.N):
            if i != j:
                # Simplified empathy field calculation
                loss_gradient = (10 - self.agents[j].utility) * 1.5
                prediction = self.agents[j].utility * 0.1
                E_i += self.W[i,j] * (loss_gradient + self.params['lambda_cog'] * prediction)
        return -E_i
    
    def update_action(self, i: int, E_i: float):
        """Update agent action based on empathy field"""
        self.agents[i].action += self.params['r_int'] * E_i
    
    def update_links(self, E: np.array):
        """Update connection weights through emotional contagion"""
        mu = self.params['mu']
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    self.W[i,j] += mu * (E[j] - E[i])
        self.W = np.clip(self.W, 0.01, 1.0)
    
    def global_dynamics(self, E: np.array) -> float:
        grad_D = np.array([abs(a.action) for a in self.agents])
        dD_dt = -self.params['eta_global'] * np.sum(E * grad_D)
        xi = np.random.normal(0, 0.1)
        return dD_dt + xi
    
    def safe_sacrifice_term(self) -> float:
        political_utils = [a.utility for a in self.agents if a.is_political]
        if not political_utils:
            return 0.0
        min_U = min(political_utils)
        if min_U >= 0:
            return 0.0
        if any(a.utility < 0 and not a.is_political for a in self.agents):
            return 0.0
        return min_U
    
    def beauty(self, dD_dt: float, M: float, avg_U: float, E_ext: float) -> float:
        sacrifice = 0.0
        if self.params['epsilon'] <= 0.3:
            sacrifice = self.params['epsilon'] * self.safe_sacrifice_term()
        return (-dD_dt +  # Fixed: removed ~ operator
                self.params['beta'] * M**2 +
                self.params['delta'] * avg_U -
                sacrifice -
                self.params['lambda_debt'] * self.Dm -
                self.params['zeta'] * E_ext)
    
    def update_debt(self, R_step: float):
        self.Dm = (self.Dm * (1 - self.params['rho'] * R_step) + 
                  self.params['gamma_ext'] * self.params['P_ext'])
    
    def mirror_resonance(self) -> float:
        U = np.array([a.utility for a in self.agents])
        return np.mean(np.exp(-np.abs(U[:, None] - U[None, :])))
    
    def step(self):
        self.step_count += 1
        E = np.array([self.empathy_field(i) for i in range(self.N)])
        dD_dt = self.global_dynamics(E)
        self.D += dD_dt * 0.1

        for i, E_i in enumerate(E): 
            self.update_action(i, E_i)
        self.update_links(E)

        R_step = 0.4 * self.Dm
        self.reparations += R_step
        self.update_debt(R_step)

        M = self.mirror_resonance()
        avg_U = np.mean([a.utility for a in self.agents])
        B = self.beauty(-dD_dt, M, avg_U, 0.0)

        for a in self.agents:
            delta = 0.01 * a.action + 0.005 * np.mean(E)
            a.utility += delta
            if not a.is_political:
                a.utility = np.clip(a.utility, 0, 10)
            else:
                a.utility = np.clip(a.utility, -5, 10)

        self.history['B'].append(B)
        self.history['Dm'].append(self.Dm)
        self.history['U'].append([a.utility for a in self.agents])
        self.history['D'].append(self.D)  # Fixed: removed extra parenthesis
        self.history['R'].append(self.reparations)
    
    def run(self, steps: int = 3000):
        for _ in range(steps):
            self.step()
        return self.history
    
    def plot(self):
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1); plt.plot(self.history['B']); plt.title('Moral Beauty B')
        plt.subplot(2, 2, 2); plt.plot(self.history['Dm']); plt.title('Moral Debt Dm')  # Fixed: changed to subplot 2
        plt.subplot(2, 2, 3); plt.plot([np.mean(u) for u in self.history['U']]); plt.title('Average Utility')
        plt.subplot(2, 2, 4); plt.plot(self.history['R']); plt.title('Reparations')
        plt.tight_layout()
        plt.show()

# Default parameters
PARAMS = {
    'H': 10.0, 'gamma_0': 0.8, 'I': 5.0, 'k_stress': 2.0,
    'beta': 0.80, 'delta': 1.20, 'epsilon': 0.18, 'lambda_debt': 0.0005, 'zeta': 0.20,
    'lambda_cog': 0.7, 'r_int': 0.1, 'mu': 0.05, 'eta_global': 0.1,
    'rho': 0.40, 'gamma_ext': 1.0, 'P_ext': 10.0
}

if __name__ == "__main__":
    print("Murène Empathic Engine - Complete Implementation")
    system = MureneSystem()
    results = system.run(steps=500)  # Shorter for demo
    system.plot()
