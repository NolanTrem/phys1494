import pandas as pd

class CoefficientAnalyzer:
    def __init__(self, data_file):
        """
        Initialize the CoefficientAnalyzer class.
        """
        # Load the data for all trials from the CSV
        self.data = pd.read_csv(data_file)

    def calculate_coefficient(self, v_initial, v_final):
        """
        Calculate the coefficient of restitution 'e'.
        """
        return abs(v_final) / abs(v_initial)
    
    def calculate_uncertainty(self, v_initial, sigma_vi, v_final, sigma_vf):
        """
        Calculate the uncertainty in the coefficient of restitution 'e' using the error propagation formula.
        """
        partial_e_vi = -v_final / v_initial**2
        partial_e_vf = 1 / v_initial
        
        return ((partial_e_vi**2 * sigma_vi**2) + (partial_e_vf**2 * sigma_vf**2))**0.5

    def process_all_trials(self):
        """Process all trials in the data."""
        self.data['e_calculated'] = self.data.apply(lambda row: self.calculate_coefficient(row['v initial'], row['v final']), axis=1)
        
        self.data['e_uncertainty'] = self.data.apply(lambda row: self.calculate_uncertainty(row['v initial'], row['uncertainty vi'], row['v final'], row['uncertainty vf']), axis=1)

    def display_results(self):
        """Display the results for all trials."""
        print(self.data)

# Usage
analyzer = CoefficientAnalyzer("experiment1/data.csv")
analyzer.process_all_trials()
analyzer.display_results()
