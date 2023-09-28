import pandas as pd
import matplotlib.pyplot as plt
import os

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

        return (
            (partial_e_vi**2 * sigma_vi**2)
            + (partial_e_vf**2 * sigma_vf**2)
        ) ** 0.5

    def process_all_trials(self):
        """Process all trials in the data."""
        self.data["e_calculated"] = self.data.apply(
            lambda row: self.calculate_coefficient(
                row["v initial"], row["v final"]
            ),
            axis=1,
        )
        self.data["e_uncertainty"] = self.data.apply(
            lambda row: self.calculate_uncertainty(
                row["v initial"],
                row["uncertainty vi"],
                row["v final"],
                row["uncertainty vf"],
            ),
            axis=1,
        )

        # Calculate unweighted mean and standard error on the mean
        self.e_mean = self.data["e_calculated"].mean()
        self.sigma = self.data["e_calculated"].std()  # standard deviation
        self.N = len(self.data)
        self.sigma_mean = self.sigma / (self.N**0.5)

        # Calculate weighted mean and its standard error
        weights = 1 / self.data["e_uncertainty"] ** 2
        self.e_weighted_mean = sum(self.data["e_calculated"] * weights) / sum(weights)
        self.sigma_weighted_mean = (sum(weights)) ** -0.5

    def display_results(self):
        """Display the results for all trials."""
        print("Trial-wise results:")
        print(self.data)
        print("\nUnweighted mean (ē):", self.e_mean)
        print("Standard deviation (σ):", self.sigma)
        print("Standard error on the mean (σ̄e):", self.sigma_mean)
        print("\nWeighted mean (ē_w):", self.e_weighted_mean)
        print("Standard error on the weighted mean (σ̄_ew):", self.sigma_weighted_mean)

    def plot_e_vs_vi(self):
        """Plot e against v_initial and save the figure in the 'figures' folder."""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.data["v initial"], self.data["e_calculated"], marker='o', color='blue', label="e values")
        plt.axhline(y=self.e_mean, color='r', linestyle='--', label=f"Unweighted mean $\\bar{{e}}$ = {self.e_mean:.4f}")
        plt.axhline(y=self.e_weighted_mean, color='g', linestyle='-.', label=f"Weighted mean $\\bar{{e}}_w$ = {self.e_weighted_mean:.4f}")
        plt.xlabel("Initial Velocity ($v_i$)")
        plt.ylabel("Coefficient of Restitution (e)")
        plt.title("Distribution of Coefficient of Restitution values")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Create 'figures' directory if not exists
        if not os.path.exists('figures'):
            os.makedirs('figures')

        # Save the plot
        plt.savefig('experiment1/figures/e_vs_vi_plot.png')
        plt.show()

    def plot_histogram(self):
            """Plot a histogram of e values and overlay vertical lines for e_bar and e_w_bar."""
            plt.figure(figsize=(10, 6))
            plt.hist(self.data["e_calculated"], bins=10, color='lightblue', edgecolor='black', alpha=0.7, label="Frequency of e values")
            plt.axvline(x=self.e_mean, color='r', linestyle='--', label=f"Unweighted mean $\\bar{{e}}$ = {self.e_mean:.4f}")
            plt.axvline(x=self.e_weighted_mean, color='g', linestyle='-.', label=f"Weighted mean $\\bar{{e}}_w$ = {self.e_weighted_mean:.4f}")
            plt.xlabel("Coefficient of Restitution (e)")
            plt.ylabel("Frequency")
            plt.title("Frequency Distribution of Coefficient of Restitution values")
            plt.legend()
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.tight_layout()

            # Save the plot in 'figures' directory
            plt.savefig('experiment1/figures/e_histogram.png')
            plt.show()

analyzer = CoefficientAnalyzer("experiment1/data.csv")  # Adjust the file path
analyzer.process_all_trials()
analyzer.display_results()
analyzer.plot_e_vs_vi()
analyzer.plot_histogram()
